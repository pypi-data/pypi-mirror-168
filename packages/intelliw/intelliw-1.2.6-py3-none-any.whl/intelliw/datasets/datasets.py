'''
Author: hexu
Date: 2021-10-14 14:54:05
LastEditTime: 2022-09-16 14:31:12
LastEditors: Hexu
Description: 数据集
FilePath: /iw-algo-fx/intelliw/datasets/datasets.py
'''
from typing import Dict, List, Tuple, overload
from intelliw.datasets.spliter import get_set_spliter
from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceEmpty, AbstractDataSourceWriter, \
    EmptyDataSourceWriter, DataSourceType as DST, DatasetType
from intelliw.utils.logger import _get_framework_logger
from intelliw.config import config
from intelliw.utils.global_val import gl

logger = _get_framework_logger()


def get_datasource(intelliv_src: str, intelliv_row_addr: str) -> AbstractDataSource:
    dt = config.SOURCE_TYPE
    if dt == DST.EMPTY:
        return DataSourceEmpty()
    elif dt == DST.REMOTE_CSV:
        from intelliw.datasets.datasource_remote_csv import DataSourceRemoteCsv
        return DataSourceRemoteCsv(config.DATA_SOURCE_ADDRESS)
    elif dt == DST.LOCAL_CSV:
        from intelliw.datasets.datasource_local_csv import DataSourceLocalCsv
        return DataSourceLocalCsv(config.CSV_PATH)
    elif dt == DST.INTELLIV:
        from intelliw.datasets.datasource_intelliv import DataSourceIntelliv
        return DataSourceIntelliv(intelliv_src, intelliv_row_addr, config.INPUT_MODEL_ID)
    elif dt == DST.IW_IMAGE_DATA:
        from intelliw.datasets.datasource_iwimgdata import DataSourceIwImgData
        return DataSourceIwImgData(intelliv_src, intelliv_row_addr, config.INPUT_DATA_SOURCE_ID, config.INPUT_DATA_SOURCE_TRAIN_TYPE)
    elif dt == DST.IW_FACTORY_DATA:
        from intelliw.datasets.datasource_iwfactorydata import DataSourceIwFactoryData
        return DataSourceIwFactoryData(intelliv_src, intelliv_row_addr, config.INPUT_DATA_SOURCE_ID)
    elif dt == DST.NLP_CORPORA:
        from intelliw.datasets.datasource_nlp_corpora import DataSourceNLPCorpora
        return DataSourceNLPCorpora(intelliv_src, config.INPUT_DATA_SOURCE_ID, config.INPUT_DATA_SOURCE_TRAIN_TYPE)
    else:
        err_msg = "数据读取失败，无效的数据源类型: {}".format(dt)
        logger.error(err_msg)
        raise ValueError(err_msg)


def get_datasource_writer(output_addr: str) -> AbstractDataSourceWriter:
    output_datasource_type = config.OUTPUT_SOURCE_TYPE
    if output_datasource_type == DST.EMPTY:
        return EmptyDataSourceWriter()
    elif output_datasource_type == DST.INTELLIV or output_datasource_type == DST.IW_FACTORY_DATA:
        from intelliw.datasets.datasource_intelliv import DataSourceWriter
        return DataSourceWriter(output_addr, config.OUTPUT_DATA_SOURCE_ID, config.INFER_ID, config.TENANT_ID)
    else:
        err_msg = "输出数据源设置失败，无效的数据源类型: {}".format(output_datasource_type)
        logger.error(err_msg)
        raise ValueError(err_msg)


class DataSets:
    def __init__(self, datasource: AbstractDataSource):
        self.datasource = datasource
        self.alldata = list()
        self.column_meta = list()
        self.model_type = gl.get("model_type")  # 分类/回归/ocr/时间序列/文本分类。。。。。

    def empty_reader(self, dataset_type=DatasetType.TRAIN):
        return self.datasource.reader(page_size=1, offset=0, limit=0, transform_function=None, dataset_type=dataset_type)

    def reader(self, page_size=100000, offset=0, limit=0, split_transform_function=None):
        return self.datasource.reader(page_size, offset, limit, split_transform_function)

    @overload
    def data_pipeline(self, split_transform_function, alldata_transform_function, feature_process): pass
    def data_pipeline(self, *args):
        if config.SOURCE_TYPE == DST.NLP_CORPORA:
            return self._nlp_data(config.DATA_SPLIT_MODE)
        elif config.SOURCE_TYPE == DST.IW_IMAGE_DATA:
            return self._images_data(self._data_pipeline(*args))
        else:
            train, validation, test = self._data_pipeline(*args)
            return [[train], [validation], [test]]

    def read_all_data(self, split_transform_function=None):
        reader = self.reader(config.DATA_SOURCE_READ_SIZE, 0,
                             self.datasource.total(), split_transform_function)
        for idx, r in enumerate(reader):
            if config.SOURCE_TYPE != DST.IW_IMAGE_DATA:
                if idx == 0:
                    self.column_meta = reader.meta
                    self.alldata = r
                elif 'result' in r and 'result' in self.alldata:
                    self.alldata['result'].extend(r['result'])
            else:
                self.alldata.extend(r)
        return self.alldata

    def _data_pipeline(self, stf, atf, fp):
        # 获取全部数据(切片数据处理， 列选择和数据筛选)
        alldata = self.read_all_data(stf)

        _data_process_args = [
            alldata, atf, fp
        ]
        _get_set_spliter_args = [
            alldata
        ]
        # 时间序列
        if self.model_type == DST.TIME_SERIES:
            _data_process_args.append(True)
            _get_set_spliter_args.append(True)

        # 数据处理（时间序列，全局函数和特征工程）
        alldata = self._data_process(*_data_process_args)

        # 数据集切分
        spliter = get_set_spliter(*_get_set_spliter_args)

        # 数据集处理 图片下载/语料下载/数据返回
        return spliter.train_reader(), spliter.validation_reader(), spliter.test_reader()

    def _data_process(self, alldata, atf, fp, do_nothing=False):
        if do_nothing is True:
            pass
        elif config.SOURCE_TYPE == DST.IW_IMAGE_DATA:
            pass
        elif atf or fp:
            alldata = atf(alldata) if atf else alldata
            alldata = fp(alldata) if fp else alldata
        return alldata

    def _images_data(self, train, val, test):
        tr = self.datasource.download_images(
            train, dataset_type=DatasetType.TRAIN)
        v = self.datasource.download_images(
            val, dataset_type=DatasetType.VALID)
        te = self.datasource.download_images(
            test, dataset_type=DatasetType.TEST)
        return [tr, v, te]

    def _nlp_data(self, split_mode: int):
        self.datasource.corpora_process(split_mode)
        return [self.datasource()]*3


class MultipleDataSets:
    def __init__(self) -> None:
        self.total = 0
        self.onlyone = True
        self.datasets: List[DataSets] = list()

    def total(self):
        return self.total

    def add(self, dataset: DataSets):
        self.datasets.append(dataset)
        self.total += 1

    def pop(self):
        return self.datasets.pop()


@overload
def get_dataset(src: str, addr: str) -> DataSets: pass
@overload
def get_dataset(info: Dict) -> MultipleDataSets: pass


def get_dataset(*args) -> Tuple[DataSets, MultipleDataSets]:
    arg = args[0]
    if isinstance(arg, Dict):
        mds = MultipleDataSets()
        # TODO
        info = arg
        datasource = get_datasource(info)
        mds.add(datasource)
        return mds
    else:
        datasource = get_datasource(*args)
        return DataSets(datasource)
