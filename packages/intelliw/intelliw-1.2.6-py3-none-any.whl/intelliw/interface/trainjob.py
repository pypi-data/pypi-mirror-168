'''
Author: Hexu
Date: 2022-08-24 16:52:17
LastEditors: Hexu
LastEditTime: 2022-08-25 10:12:52
FilePath: /iw-algo-fx/intelliw/interface/trainjob.py
Description: Train entrypoint
'''
import traceback
from intelliw.core.trainer import Trainer
from intelliw.core.report import RestReport
from intelliw.datasets.datasets import get_dataset
import intelliw.utils.message as message
from intelliw.utils.logger import _get_framework_logger

logger = _get_framework_logger()


class TrainServer:
    def __init__(self, path, src, rownumaddr, response_addr=None):
        self.src = src
        self.response_addr = response_addr
        self.path = path
        self.reporter = RestReport(response_addr)
        self.rownumaddr = rownumaddr

    def run(self):
        try:
            trainer = Trainer(self.path, self.reporter)
            datasets = get_dataset(self.src, self.rownumaddr)
            trainer.train(datasets)
        except Exception as e:
            stack_info = traceback.format_exc()
            logger.error("训练执行错误 {}, stack:\n{}".format(e, stack_info))
            self.reporter.report(
                message.CommonResponse(500, "train_fail", "训练执行错误 {}, stack:\n{}".format(e, stack_info)))
