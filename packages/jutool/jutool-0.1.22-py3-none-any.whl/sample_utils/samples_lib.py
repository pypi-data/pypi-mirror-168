import abc
import time, progressbar
from code_utils.structures import func_check, iter_idx
from code_utils.log import log_error, log
from sample_utils.NLSampleSource import NLSampleSourceBase


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

    def transform_to_new_set(self, from_name: str, new_name: str, description: str, lables: [str], transform_func):
        meta_data = self._sample_source.get_metadata_keys(from_name)
        new_set_name = f"{from_name}_{new_name}"

        if lables is None:
            lables = meta_data['label_keys']

        try:

            if not self._sample_source.has_set(new_set_name):
                self._sample_source.create_new_set(new_name, meta_data['des'], meta_data['tags'], lables
                                                   , base_set=from_name, base_set_process=description)
            else:
                log_error("已存在同名的set")

            from_count = self._sample_source.get_set_count(from_name)
            bar = progressbar.ProgressBar(0, from_count)

            index = 0
            for row_list in self._sample_source.iter_data(from_name):
                index += 1
                bar.update(index)
                row_dic = {key: value for key, value in zip(meta_data['label_keys'], row_list)}
                new_row_data = transform_func(row_dic)
                # new_row_data = [new_row_data[key] for key in lables]
                self.import_one_data(new_set_name, new_row_data)

            log(f"Transform Completed. {self._sample_source.get_set_count(new_set_name)} rows")
        except :
            self._sample_source.delete_set(new_set_name)
