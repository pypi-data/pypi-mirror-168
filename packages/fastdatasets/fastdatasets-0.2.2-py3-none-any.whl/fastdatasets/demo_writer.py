# @Time    : 2022/9/18 23:27
# @Author  : tk
# @FileName: demo_writer.py

import pickle
import data_serialize
from fastdatasets import RecordLoader,FeatrueWriter,StringWriter,PickleWriter,DataType,gfile

def test_string(filename=r'd:\\example_writer.record0'):
    print('test_string ...')
    with StringWriter(filename) as writer:
        for i in range(2):
            writer.write(b'123' )


    datasets = RecordLoader.IterableDataset(filename)
    for i,d in enumerate(datasets):
        print(i, d)

def test_pickle(filename=r'd:\\example_writer.record1'):
    print('test_pickle ...')

    with PickleWriter(filename) as writer:
        for i in range(2):
            writer.write(b'test_pickle' + b'123')
    datasets = RecordLoader.RandomDataset(filename)
    datasets = datasets.map(lambda x: pickle.loads(x))
    for i in range(len(datasets)):
        print(i, datasets[i])

def test_feature(filename=r'd:\\example_writer.record2'):
    print('test_feature ...')
    with FeatrueWriter(filename) as writer:
        for i in range(3):
            feature = {
                'input_ids': {
                    'dtype': DataType.int64_list,
                    'data': list(range(i + 1))
                },
                'seg_ids': {
                    'dtype': DataType.float_list,
                    'data': [i,0,1,2]
                },
                'other':{
                    'dtype': DataType.bytes_list,
                    'data': [b'aaa',b'bbbc1']
                },
            }
            writer.write(feature)


    datasets = RecordLoader.RandomDataset(filename)
    for i in range(len(datasets)):
        example = data_serialize.Example()
        example.ParseFromString(datasets[i])
        feature = example.features.feature
        print(feature)

test_string()
test_pickle()
test_feature()

