# @Time    : 2022/9/18 10:49
# @Author  : tk
# @FileName: __init__.py.py

import typing
import os
from typing import List
import warnings
import tfrecords
from .utils import RandomDatasetBase
import pickle
from collections.abc import Sized
import copy

#import hashlib
# def md5_for_file(f, block_size=16 * 16 * 1024):
#     md5 = hashlib.md5()
#     while True:
#         data = f.read(block_size)
#         if not data:
#             break
#         md5.update(data)
#     return md5.digest()
#
# def md5sum(filename, blocksize=16 * 16 * 1024):
#     hash = hashlib.md5()
#     with open(filename, "r+b") as f:
#         for block in iter(lambda: f.read(blocksize), ""):
#             hash.update(block)
#     return hash.hexdigest()

class SingleRandomRecordDataset(RandomDatasetBase):
    def __init__(self,
                 data_path_or_data_list: typing.Union[typing.AnyStr,typing.Sized],
                 index_path: str = None,
                 force_overwrite_index=False,
                 options=tfrecords.TFRecordOptions(tfrecords.TFRecordCompressionType.NONE)
                 ):
        super(SingleRandomRecordDataset, self).__init__()

        if isinstance(data_path_or_data_list,str):
            self.is_file = True
        else:
            self.is_file = False
            assert isinstance(data_path_or_data_list,Sized)


        if self.is_file:
            if index_path is None:
                index_path = os.path.join(os.path.dirname(data_path_or_data_list), '.' + os.path.basename(data_path_or_data_list)+ '.INDEX')
            else:
                index_path = os.path.join(index_path, '.' + os.path.basename(data_path_or_data_list)+ '.INDEX')

        self.data_path_or_data_list = data_path_or_data_list
        self.index_path = index_path
        self.options = options

        self.file_reader_ = None
        self.reset()

        self.file_size = -1
        if self.is_file:
            is_need_update_idx = False
            file_size = 0
            if not force_overwrite_index and os.path.exists(self.index_path):
                if os.path.exists(self.data_path_or_data_list):
                    file_size = os.stat(self.data_path_or_data_list).st_size

                with open(self.index_path, mode='rb') as f:
                    filemeta = pickle.load(f)

                if not isinstance(filemeta,tuple):
                    is_need_update_idx = True
                else:
                    self.indexes, self.file_size = filemeta

                if self.file_size != file_size:
                    is_need_update_idx = True
                    self.file_size = file_size
            else:
                is_need_update_idx = True

            if is_need_update_idx:
                if os.path.exists(self.data_path_or_data_list):
                    self.file_size = os.stat(self.data_path_or_data_list).st_size

                self.indexes = []
                pos = 0
                try:

                    while self.file_reader_ is not None:
                        _,pos_ = self.file_reader_.read(pos)
                        self.indexes.append((pos,pos_ - pos))
                        pos = pos_

                except Exception as e:
                    pass
                if len(self.indexes):
                    with open(self.index_path, mode='wb') as f:
                        pickle.dump((self.indexes,self.file_size),f)
        else:
            self.indexes = self.data_path_or_data_list
        self.length = len(self.indexes)
    def __del__(self):
       self.close()

    def reset(self):
        self.repeat_done_num = 0
        self.__reopen__()

    def close(self):
        if self.is_file:
            if self.file_reader_:
                self.file_reader_.close()
                self.file_reader_ = None
        else:
            self.file_reader_ = None

    def __reopen__(self):
        self.block_id = -1
        self.close()
        if self.is_file:
            if os.path.exists(self.data_path_or_data_list):
                self.file_reader_ = tfrecords.tf_record_random_reader(self.data_path_or_data_list, options=self.options)
            else:
                self.file_reader_ = None
        else:
            self.file_reader_ = self.data_path_or_data_list
        self.repeat_done_num += 1
        return True

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        if self.file_reader_ is None:
            raise OverflowError

        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        if self.is_file:
            pos_inf = self.indexes[item]
            x, _ = self.file_reader_.read(pos_inf[0])
        else:
            x = self.data_path_or_data_list[item]
        return x


class MultiRandomRecordDataset(RandomDatasetBase):
    def __init__(self,
                 data_path_data_list: List[typing.Union[typing.AnyStr,typing.Sized]],
                 index_path = None,
                 force_overwrite_index=False,
                 options = tfrecords.TFRecordOptions(tfrecords.TFRecordCompressionType.NONE)
                 ) -> None:
        super(MultiRandomRecordDataset, self).__init__()

        self.options = options
        self.data_path_data_list = data_path_data_list
        self.index_path = index_path
        self.force_overwrite_index = force_overwrite_index
        self.reset()

    def reset(self):
        self.iterators_ = [{"valid": False,"file": self.data_path_data_list[i]} for i in range(len(self.data_path_data_list))]
        self.cicle_iterators_ = []
        self.fresh_iter_ids = False
        self.cur_id = 0
        self.__reopen__()

    def close(self):
        for iter_obj in self.iterators_:
            if iter_obj["valid"] and "instance" in iter_obj and iter_obj["instance"]:
                iter_obj["instance"].close()
                iter_obj["valid"] = False
                iter_obj["instance"] = None

    def __reopen__(self):
        for it_obj in self.iterators_:
            it_obj['inst'] = SingleRandomRecordDataset(it_obj["file"],index_path=self.index_path,force_overwrite_index=self.force_overwrite_index,options=self.options)

    def __len__(self):
        total_len = 0
        for it_obj in self.iterators_:
            total_len += len(it_obj['inst'])
        return total_len

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        cur_len = 0
        obj = None
        for i,it_obj in enumerate(self.iterators_):
            tmp_obj = it_obj['inst']
            if item < cur_len + len(tmp_obj):
                obj = tmp_obj
                break
            cur_len += len(tmp_obj)
        if obj is None:
            raise tfrecords.OutOfRangeError
        real_index =  item - cur_len
        return obj[real_index]
