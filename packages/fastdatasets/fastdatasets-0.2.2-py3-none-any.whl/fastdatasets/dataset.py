# @Time    : 2022/9/20 21:55
# @Author  : tk
# @FileName: dataset.py

import typing
import os
import warnings
from tfrecords.python.io import gfile
from tfrecords.python.io.tf_record import *
from collections.abc import Iterator,Sized
from typing import Union,List,AnyStr

from .iterable_dataset import SingleRecordIterableDataset,MultiRecordIterableDataset,IterableDatasetBase
from .random_dataset import SingleRandomRecordDataset,MultiRandomRecordDataset,RandomDatasetBase
import copy


def RecordIterableDatasetLoader(data_path_or_data_iterator: Union[List[Union[AnyStr,typing.Iterator]],AnyStr,typing.Iterator],
                     buffer_size: typing.Optional[int] = 128,
                     cycle_length=1,
                     block_length=1,
                     options=TFRecordOptions(TFRecordCompressionType.NONE)):
    if isinstance(data_path_or_data_iterator, list):
        if len(data_path_or_data_iterator) == 1:
            cls = SingleRecordIterableDataset(
                data_path_or_data_iterator[0], buffer_size, block_length, options
            )
        else:
            cls = MultiRecordIterableDataset(data_path_or_data_iterator, buffer_size, cycle_length, block_length, options)
    elif isinstance(data_path_or_data_iterator, str) or isinstance(data_path_or_data_iterator, Iterator):
        cls = SingleRecordIterableDataset(
            data_path_or_data_iterator, buffer_size, block_length, options
        )
    else:
        raise Exception('data_path must be list or single string')
    return cls

def RecordRandomDatasetLoader(data_path_or_data_list: typing.Union[typing.List,typing.AnyStr,typing.Sized],
                            index_path=None,
                            force_overwrite_index=False,
                            options=TFRecordOptions(TFRecordCompressionType.NONE)):
    if isinstance(data_path_or_data_list, list):
        if len(data_path_or_data_list) == 1:
            cls = SingleRandomRecordDataset(
                data_path_or_data_list[0],index_path=index_path,force_overwrite_index=force_overwrite_index, options=options
            )
        else:
            cls = MultiRandomRecordDataset(data_path_or_data_list,index_path=index_path,force_overwrite_index=force_overwrite_index,options=options)
    elif isinstance(data_path_or_data_list, str) or isinstance(data_path_or_data_list, Sized):
        cls = SingleRandomRecordDataset(data_path_or_data_list, index_path=index_path,force_overwrite_index=force_overwrite_index,options=options)
    else:
        raise Exception('data_path must be list or single string')
    return cls

class RecordLoader:
    class IterableDataset(Iterator,IterableDatasetBase):
        def __new__(cls, *args, **kwargs) ->  SingleRecordIterableDataset or MultiRecordIterableDataset:
            return RecordIterableDatasetLoader(*args, **kwargs)

        def __init__(self,data_path_or_data_iterator: Union[List[Union[AnyStr,typing.Iterator]],AnyStr,typing.Iterator],
                     buffer_size: typing.Optional[int] = 128,
                     cycle_length=1,
                     block_length=1,
                     options=TFRecordOptions(TFRecordCompressionType.NONE)):
            pass
    class SingleIterableDataset(IterableDataset):
        def __new__(cls, *args, **kwargs) -> SingleRecordIterableDataset:
            return SingleRecordIterableDataset(*args, **kwargs)

    class MultiIterableDataset(IterableDataset):
        def __new__(cls, *args, **kwargs) -> MultiRecordIterableDataset:
            return MultiRecordIterableDataset(*args, **kwargs)



    class RandomDataset(Sized,RandomDatasetBase):
        def __new__(cls, *args, **kwargs) -> SingleRandomRecordDataset or MultiRandomRecordDataset:
            return RecordRandomDatasetLoader(*args, **kwargs)
        def __init__(self,data_path_or_data_list: typing.Union[typing.List,typing.AnyStr,typing.Sized],
                              index_path=None,
                              force_overwrite_index=False,
                              options=TFRecordOptions(TFRecordCompressionType.NONE)):
            pass

        def __len__(self):
            raise NotImplementedError

        def __getitem__(self, item):
            raise NotImplementedError

    class SingleRandomDataset(RandomDataset):
        def __new__(cls, *args, **kwargs) -> SingleRandomRecordDataset:
            return SingleRandomRecordDataset(*args, **kwargs)

    class MutiRandomDataset(RandomDataset):
        def __new__(cls, *args, **kwargs) -> MultiRandomRecordDataset:
            return MultiRandomRecordDataset(*args, **kwargs)