#!/usr/bin/env python
# coding: utf-8
import json
import threading
import time
import traceback
from intelliw.utils.crontab import Crontab
from flask import Flask, jsonify, request
from intelliw.datasets.datasets import get_dataset, get_datasource_writer
from intelliw.core.report import RestReport

from intelliw.core.infer import Infer
import intelliw.utils.message as message
from intelliw.datasets.datasource_base import DataSourceReaderException, DataSourceWriterException
from intelliw.utils.util import get_json_encoder
from intelliw.config import config
from intelliw.utils.logger import _get_framework_logger

logger = _get_framework_logger()

batchjob_infer = "batchjob-infer"


class Request:
    def __init__(self, batch_params={}) -> None:
        self.batch_params = batch_params


def get_batch_msg(issuccess, starttime, msg, data={}):
    """
    批处理上报信息，inferTaskStatus 不为空，会被记录为一次调用，标识一次批处理的状态
    """
    outmsg = [
        {
            'status': 'start' if issuccess else 'end',
            'inferid': config.INFER_ID,
            'instanceid': config.INSTANCE_ID,
            'inferTaskStatus': [
                {
                    "id": config.INFER_ID,
                    "issuccess": issuccess,
                    "starttime": starttime,
                    "endtime": int(time.time() * 1000),
                    "message": msg
                }
            ],
            "respParams": data
        }
    ]
    return json.dumps(outmsg, cls=get_json_encoder(), ensure_ascii=False)


def get_msg(is_success, msg):
    """
    批处理上报信息，inferTaskStatus 为空，不会被记录为一次调用，用于上报和单次调用无关的消息
    """
    return [
        {
            'status': 'start',
            'inferid': config.INFER_ID,
            'instanceid': config.INSTANCE_ID,
            'inferTaskStatus': []
        }
    ]


def validate_batch_job(reporter, path):
    Infer(path, reporter)
    msg = get_msg(True, '定时推理校验通过，上线成功')
    reporter.report(message.CommonResponse(200, batchjob_infer,
                                           '定时推理校验通过，上线成功',
                                           json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))


def infer_job(reporter, path, src, dst, rownumaddr, params={}):
    def input(s, r):
        datasets = get_dataset(s, r)
        return datasets.read_all_data()

    def output(t, r):
        out_result = {
            'meta': str(type(r)),
            'result': r
        }
        writer = get_datasource_writer(dst)
        res_data = writer.write(out_result, t)
        if res_data['status'] != 1:
            raise DataSourceWriterException(res_data['msg'])

    try:
        start_time = int(time.time() * 1000)

        # 输入
        alldata = input(src, rownumaddr)

        # 批处理
        req = Request(params)
        result, err = Infer(path, reporter).infer(alldata, req)
        if err is not None:
            raise Exception(err)
        else:
            logger.info('批处理处理结果 {}'.format(result))

        # 输出
        output(start_time, result)
    except DataSourceReaderException as e:
        info = f"批处理输入数据错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    except DataSourceWriterException as e:
        info = f"批处理输出数据错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    except Exception as e:
        info = f"批处理执行错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    else:
        info = "批处理输出数据成功"
        stack_info = None
    finally:
        if stack_info is None:
            status_code, msg = 200, get_batch_msg(
                True, start_time, info, req.batch_params)
        else:
            logger.error(stack_info)
            status_code, msg = 500, get_batch_msg(
                False, start_time, info, params)
        reporter.report(message.CommonResponse(
            status_code, batchjob_infer, info, msg))


class JobServer:
    @staticmethod
    def healthcheck():
        resp = message.HealthCheckResponse(200, "api", 'ok', "")
        return jsonify(resp())

    @staticmethod
    def run(reporter, path, src, dst, rownumaddr):
        msg = "server job start"
        logger.info(msg)
        threading.Thread(
            target=infer_job,
            args=(reporter, path, src, dst, rownumaddr, request.json)
        ).start()
        return jsonify({"code": "1", "msg": msg})


class BatchService:
    def __init__(self, format, path, src, dst, rownumaddr, response_addr=None, task='infer'):
        if task != 'infer':
            msg = get_msg(False, '批处理任务任务错误，TASK环境变量必须为infer')
            self.reporter.report(message.CommonResponse(500, batchjob_infer,
                                                        '批处理任务任务错误, TASK环境变量必须为infer',
                                                        json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))

        # 按照crontab的格式给出format就可以
        self.format = format
        self.only_server = True if self.format is None or self.format == '' else False
        self.src = src
        self.dst = dst
        self.response_addr = response_addr
        self.path = path
        self.reporter = RestReport(response_addr)
        self.rownumaddr = rownumaddr

    def _format_parse(self, _format: str):
        format_list = []
        _format = _format.split("|")
        for f in _format:
            format_list.append(
                {
                    'crontab': f.strip(),
                    'func': infer_job,
                    'args': (self.reporter, self.path, self.src, self.dst,
                             self.rownumaddr)
                }
            )
        return format_list

    def _cronjob(self):
        # def inner(reporter, path, format):
        #     validate_batch_job(reporter, path)
        #     job_list = self._format_parse(format)
        #     crontab = Crontab(job_list)
        #     while True:
        #         try:
        #             crontab.start()
        #         except:
        #             logger.info(traceback.format_exc())
        # timer = threading.Timer(
        #     5, inner, (self.reporter, self.path, self.format)
        # )
        # timer.daemon = True
        # timer.start()
        validate_batch_job(self.reporter, self.path)
        job_list = self._format_parse(self.format)
        crontab = Crontab(job_list, True)
        crontab.start()
        logger.info("Start cronjob")

    def _server(self):
        app = Flask(__name__)
        args = {"reporter": self.reporter, "path": self.path,
                "src": self.src, "dst": self.dst,
                "rownumaddr": self.rownumaddr}
        app.add_url_rule("/batch-predict", view_func=JobServer.run,
                         methods=["POST"], defaults=args)
        app.add_url_rule(
            "/healthcheck", view_func=JobServer.healthcheck, methods=["POST", "GET"])
        logger.info(
            "Server Start: \n\033[33m[POST] /batch-predict\n[POST, GET] /healthcheck\033[0m"
        )

        try:
            from gevent.pywsgi import WSGIServer
            WSGIServer(('0.0.0.0', 8888), app).serve_forever()
        except ImportError:
            logger.warn(
                "\033[31mIf want use a production WSGI server, you need: pip install gevent\033[0m")
            app.run('0.0.0.0', 8888, threaded=True)

    def run(self):
        if self.only_server:
            logger.info(
                "\033[33mCronjob Format is Empty, Only Server Mode\033[0m")
            self._server()
        else:
            logger.info(
                f"\033[33mCronjob Format is {self.format}, Cronjob and Server Mode\033[0m")
            self._cronjob()
            self._server()
