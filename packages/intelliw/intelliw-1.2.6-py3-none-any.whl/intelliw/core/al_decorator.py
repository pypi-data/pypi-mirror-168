#!/usr/bin/env python
# coding: utf-8

import inspect
import json
import time
import errno
import shutil
import os
import zipfile
import traceback
from functools import wraps
import intelliw.utils.message as message
from intelliw.utils.logger import _get_framework_logger, Logger
from intelliw.config import config

logger = _get_framework_logger()


def zipdir(mpath):
    outpath = '/tmp/model.zip'
    with zipfile.ZipFile(outpath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(mpath):
            for root, dirs, files in os.walk(mpath):
                relative_path = root.replace(mpath, "")
                for file in files:
                    logger.info("压缩文件 {}".format(os.path.join(root, file)))
                    zipf.write(os.path.join(root, file),
                               os.path.join(relative_path, file))
        elif os.path.isfile(mpath):
            zipf.write(mpath, os.path.basename(mpath))
    return outpath


def decorator_report_train_info(function, reporter=None):
    from intelliw.utils.util import get_json_encoder

    @wraps(function)
    def wrapper(loss, lr, iter, batchsize, **kwargs):
        if reporter is not None:
            info = json.dumps({
                "loss": loss,
                "lr": lr,
                "iter": iter,
                "batchsize": batchsize,
                "timestamp": int(time.time() * 1000),
                "other": kwargs
            }, cls=get_json_encoder())
            reporter.report(message.CommonResponse(
                200, 'report_train_info', '', str(info)))
        return function(loss, lr, iter, batchsize, **kwargs)
    return wrapper


def decorator_report_val_info(function, reporter=None):
    from intelliw.utils.util import get_json_encoder

    @wraps(function)
    def wrapper(*args, **kwargs):
        if reporter is not None:
            val = {}

            # process args
            varnames = function.__code__.co_varnames
            offset = 0
            for i in range(len(varnames)):
                if varnames[i] == 'self' or varnames[i] == 'args' or varnames[i] == 'kwargs':
                    offset = offset - 1
                    continue
                if i + offset < len(args):
                    val[varnames[i]] = args[i + offset]
                else:
                    val[varnames[i]] = None

            # process kwargs
            for k, v in kwargs.items():
                val[k] = v

            data = {
                "modelInstanceId": config.INSTANCE_ID,
                "tenantId": config.TENANT_ID,
                "valuationResult": val
            }
            reporter.report(message.CommonResponse(200, 'report_val_info', '', json.dumps(
                data, cls=get_json_encoder(), ensure_ascii=False)))
        return function(*args, **kwargs)
    return wrapper


# decorator_save 存储模型文件到云存储
def decorator_save(function, reporter=None):
    from intelliw.utils.util import generate_random_str

    @wraps(function)
    def wrapper(*args, **kwargs):
        # 分布式训练 slave不需要保存模型
        if config.FRAMEWORK_MODE == 'distributedtrain' and not config.DIST_IS_MASTER:
            logger.info("分布式训练slave服务不需要保存模型文件")
            return None

        # 如果用户输入的是绝对路径，就使用输入的路径
        user_path = args[0]
        if os.path.isabs(user_path):
            mpath = user_path
        else:
            hpath = os.path.join('/tmp', generate_random_str(16))
            os.makedirs(hpath)
            mpath = os.path.join(hpath, user_path)

        abs_path = os.path.abspath(mpath)
        # 如传入的是目录，则拼接上路径分隔符，以保证获取 dir_path 时包括末级路径
        if mpath.endswith('/') or mpath.endswith('\\'):
            abs_path = abs_path + os.sep
        dir_path = os.path.dirname(abs_path)
        if not os.path.exists(dir_path):
            logger.info("目录不存在， 自动创建 {}".format(dir_path))
            try:
                os.makedirs(dir_path)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(dir_path):
                    pass
                else:
                    logger.error("保存模型错误:  创建目录失败")
                    reporter.report(str(message.CommonResponse(500, "train_save",
                                                               "保存模型错误:  创建目录失败 {}".format(dir_path))))
        result = function(mpath)
        if reporter is not None:
            from intelliw.utils.storage_service import StorageService
            try:
                outpath = zipdir(os.path.abspath(mpath))
                curkey = os.path.join(
                    config.STORAGE_SERVICE_PATH, generate_random_str(32))
                env_val = os.environ.get("FILE_UP_TYPE").upper()
                if env_val == "MINIO":
                    client_type = "Minio"
                elif env_val == "ALIOSS":
                    client_type = "AliOss"
                elif env_val == "HWOBS":
                    client_type = "HWObs"
                else:
                    raise TypeError(f"FILE_UP_TYPE err: {env_val}")
                uploader = StorageService(curkey, client_type, "upload")
                logger.info(f"上传模型文件到{client_type}")
                try:
                    uploader.upload(outpath)
                    logger.info(f"上传模型文件到{client_type}成功： {curkey}")
                    reporter.report(message.CommonResponse(
                        200, 'train_save', 'success', [curkey]))
                except:
                    err_info = traceback.format_exc()
                    logger.info(f"上传模型文件到{client_type}失败: {err_info}")
                    reporter.report(str(message.CommonResponse(
                        500, "train_save", f"保存模型错误 {err_info}")))
                try:
                    os.remove(outpath)
                    shutil.rmtree(hpath, ignore_errors=True)
                except:
                    pass
            except Exception as e:
                stack_info = traceback.format_exc()
                reporter.report(str(message.CommonResponse(500, "train_save",
                                                           "保存模型错误 {}, stack: \n {}".format(e, stack_info))))
        else:
            logger.info("保存模型错误:  reporter is  None")
        return result
    return wrapper


def make_decorators_server(instance, reporter=None):
    # report_train_info
    if (hasattr(instance, 'report_train_info')) and inspect.ismethod(instance.report_train_info):
        instance.report_train_info = decorator_report_train_info(
            instance.report_train_info, reporter)

    # report_val_info
    if (hasattr(instance, 'report_val_info')) and inspect.ismethod(instance.report_val_info):
        instance.report_val_info = decorator_report_val_info(
            instance.report_val_info, reporter)

    # save model
    if (hasattr(instance, 'save')) and inspect.ismethod(instance.save):
        instance.save = decorator_save(instance.save, reporter)


def make_decorators_local(instance):
    if (hasattr(instance, 'get_user_logger')) and inspect.isfunction(instance.get_user_logger):
        instance.get_user_logger = Logger()._get_logger
