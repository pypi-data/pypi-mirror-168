# @Time    : 2022/9/18 18:13
# @Author  : tk
# @FileName: demo_random.py


import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile


def test_record():
    data_path = gfile.glob('d:/example.tfrecords*')
    print(data_path)
    options = TFRecordOptions(compression_type=None)
    dataset = RecordLoader.RandomDataset(data_path_or_data_list=data_path,options=options)

    # dataset = dataset.map(lambda x: x+  b"adasdasdasd")
    # print(len(dataset))
    #
    for i in range(len(dataset)):
        print(i+1,dataset[i])

    print('batch...')
    dataset = dataset.batch(7,drop_remainder=True)
    for i in range(len(dataset)):
        print(i+1,dataset[i])

    print('unbatch...')
    dataset = dataset.unbatch()
    for i in range(len(dataset)):
        print(i+1,dataset[i])

    print('shuffle...')
    dataset = dataset.shuffle(10)
    for i in range(len(dataset)):
        print(i+1,dataset[i])

    print('map...')
    dataset = dataset.map(transform_fn=lambda x:x + b'aa22222222222222222222222222222')
    for i in range(len(dataset)):
        print(i+1,dataset[i])

    print(dataset[0:3])

    print('torch Dataset...')
    from fastdatasets.torch_dataset import Dataset

    d = Dataset(dataset)
    for i in range(len(d)):
        print(i + 1,d[i])

def test_list():
    data_path = [list(range(15)),list(range(15))]
    options = TFRecordOptions(compression_type=None)
    dataset = RecordLoader.RandomDataset(data_path_or_data_list=data_path, options=options)

    for i in range(len(dataset)):
        print(i + 1, dataset[i])

    dataset = dataset.map(lambda x: str(x) +  "asdsadasaaaaaaaa")
    print(len(dataset))

    for i in range(len(dataset)):
        print(i + 1, dataset[i])

    print('batch...')
    dataset = dataset.batch(7)
    for i in range(len(dataset)):
        print(i + 1, dataset[i])

    print('unbatch...')
    dataset = dataset.unbatch()
    for i in range(len(dataset)):
        print(i + 1, dataset[i])

    print('shuffle...')
    dataset = dataset.shuffle(10)
    for i in range(len(dataset)):
        print(i + 1, dataset[i])



    #
    # print('map...')
    # dataset = dataset.map(transform_fn=lambda x: x + b'aa22222222222222222222222222222')
    # for i in range(len(dataset)):
    #     print(i + 1, dataset[i])

    print('torch Dataset...')
    from fastdatasets.torch_dataset import Dataset

    d = Dataset(dataset)
    for i in range(len(d)):
        print(i + 1, d[i])

test_record()
#test_list()