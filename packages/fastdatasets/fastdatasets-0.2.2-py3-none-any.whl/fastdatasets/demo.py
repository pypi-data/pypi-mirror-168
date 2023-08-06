# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 16:30
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

def test_write_featrue():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)
    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                val1 = data_serialize.Int64List(value=[1, 2, 3] * 20)
                val2 = data_serialize.FloatList(value=[1, 2, 3] * 20)
                val3 = data_serialize.BytesList(value=[b'The china', b'boy'])
                featrue = data_serialize.Features(feature=
                {
                    "item_0": data_serialize.Feature(int64_list=val1),
                    "item_1": data_serialize.Feature(float_list=val2),
                    "item_2": data_serialize.Feature(bytes_list=val3)
                }
                )
                example = data_serialize.Example(features=featrue)
                file_writer.write(example.SerializeToString())

    test_write('d:/example.tfrecords0',3,'file0')
    test_write('d:/example.tfrecords1',10,'file1')
    test_write('d:/example.tfrecords2',12,'file2')

def test_write_string():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)
    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                # x, y = np.random.random(), np.random.random()
                file_writer.write(context + '____' + str(_))

    test_write('d:/example.tfrecords0',3,'file0')
    test_write('d:/example.tfrecords1',10,'file1')
    test_write('d:/example.tfrecords2',12,'file2')

# test_write_string()

data_path = gfile.glob('d:/example.tfrecords*')
print(data_path)
options = TFRecordOptions(compression_type=None)
base_dataset = RecordLoader.IterableDataset(data_path_or_data_iterator=data_path,cycle_length=1,block_length=1,buffer_size=128,options=options)

print(type(base_dataset))
num = 0
for d in base_dataset:
    num +=1
print('base_dataset num',num)
base_dataset.reset()



def test_batch():
    global base_dataset
    base_dataset.reset()
    ds = base_dataset.repeat(2).repeat(2).repeat(3).map(lambda x: x + bytes('_aaaaaaaaaaaaaa', encoding='utf-8'))
    i = 0
    for _ in ds:
        i += 1
    print('repeat(2).repeat(2).repeat(3) num ', num)

    def filter_fn(x):
        if x != b'file2____2':
            return True
        return False
    base_dataset.reset()

    print('filter....')
    dataset = base_dataset.filter(filter_fn)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)


    print('batch...')
    base_dataset.reset()
    dataset = base_dataset.batch(7)
    dataset = dataset.cache(11000)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)
    print('unbatch...')
    base_dataset.reset()
    dataset = dataset.unbatch().cache(2).repeat(2).choice(10,[0,1,2]).repeat(3)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)


def test_mutiprocess():
    print('mutiprocess...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(3,0)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)

    print('mutiprocess...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(3,1)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)

    print('mutiprocess...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(3,2)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)


test_batch()

#test_mutiprocess()