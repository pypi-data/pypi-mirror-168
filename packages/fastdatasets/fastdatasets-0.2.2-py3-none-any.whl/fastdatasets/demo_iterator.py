# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 11:20
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

options = TFRecordOptions(compression_type=None)
data = [iter(range(10)),iter(range(10))]

base_dataset = RecordLoader.IterableDataset(data_path_or_data_iterator=data,
                                           cycle_length=1,block_length=1,buffer_size=128,options=options)

for i,d in enumerate(base_dataset):
    print(i,d)
print('shuffle...')
base_dataset.reset()
base_dataset = base_dataset.shuffle(10)
for i,d in enumerate(base_dataset):
    print(i,d)