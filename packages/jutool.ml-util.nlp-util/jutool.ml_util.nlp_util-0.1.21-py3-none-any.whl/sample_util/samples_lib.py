import abc
import time
from code_util.structures import func_check, iter_idx
from code_util.log import log_error, log
from sample_util.NLSampleSource import NLSampleSourceBase


class NLSampleLib(metaclass=abc.ABCMeta):
    def __init__(self, sample_source: NLSampleSourceBase):
        self._sample_source = sample_source

    def list(self, print=True):
        self._sample_source.arrange_dir_list(self._sample_source.get_dir_list())

    def create_set(self, name: str, description: str, tags: [str], lables: [str]):
        if not self._sample_source.has_set(name):
            self._sample_source.create_new_set(name, description, tags, lables)
        else:
            log_error("已存在同名的set")

    def import_one_data(self, name: str, data: {}):
        """
        data format: { key1: data, key2:data}
        :param name:
        :param data:
        :return:
        """
        lables_key = self._sample_source.get_metadata_keys(name)['label_keys']
        row_data = [data[key] for key in lables_key]
        if not self._sample_source.add_row(name, row_data):
            raise Exception("写入失败")

    def get_count(self, name: str):
        return self._sample_source.get_set_count(name)

