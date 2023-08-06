# @Time    : 2022/9/18 19:34
# @Author  : tk
# @FileName: utils.py
import math
import typing
import numpy as np
class RandomDatasetBase:
    _opq_data_ = None
    def set_custom_data(self, data):
        self._opq_data_ = data

    @property
    def custom_data(self):
        return self._opq_data_

    def concat(self,dataset_list: typing.List):
        cls = ConcatRandomDataset(self, dataset_list)
        return cls

    def apply(self, transform_fn: typing.Callable):
        cls = MapRandomDataset(self, transform_fn)
        return cls
    def map(self, transform_fn: typing.Callable):
        cls = MapRandomDataset(self, transform_fn)
        return cls

    def choice(self,size: int,seed = None):
        cls = ShuffleRandomDataset(self, buffer_size=-1,size=size, seed=seed)
        return cls
    def batch(self,batch_size : int,drop_remainder:bool=False):
        cls = BatchRandomDataset(self, batch_size,drop_remainder)
        return cls

    def limit(self,n: int):
        cls = TopRandomDataset(self, n)
        return cls
    def top(self,n:int):
        cls = TopRandomDataset(self, n)
        return cls
    def skip(self,n:int):
        cls = SkipRandomDataset(self, n)
        return cls
    def unbatch(self):
        cls = UnBatchRandomDataset(self)
        return cls

    def shuffle(self, buffer_size, seed=None):
        cls = ShuffleRandomDataset(self, buffer_size=buffer_size, seed=seed)
        return cls
    def reset(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError
    def __getitem__(self, item):
        raise NotImplementedError
    def __getitem_slice__(self, item):
        length = len(self)
        idxs = list(range(length))[item]
        data = []
        for idx in idxs:
            data.append(self[idx])
        return data


class ConcatRandomDataset(RandomDatasetBase):
    def __init__(self, dataset, other_datast_list: typing.List[RandomDatasetBase]):
        self.dataset = dataset
        self.other_datast_list = other_datast_list
        self.all_dataset_list = [self.dataset] +  self.other_datast_list

        self.length = sum([len(_) for _ in self.all_dataset_list])

        self.len_arr = [len(_) for _ in self.all_dataset_list]
        accumlate_int = 0
        for i in range(len(self.len_arr)):
            self.len_arr[i] += accumlate_int
            accumlate_int += self.len_arr[i]
    def reset(self):
        for dataset in self.all_dataset_list:
            if hasattr(dataset,'reset'):
                dataset.reset()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        for i,accumlate_total_length in enumerate(self.len_arr):
            if item < accumlate_total_length:
                cur_dataset = self.all_dataset_list[i]
                return cur_dataset[item-(accumlate_total_length - len(cur_dataset))]

        raise OverflowError

    def __len__(self):
        return self.length


class TopRandomDataset(RandomDatasetBase):
    def __init__(self, dataset, n):
        assert n >= 0
        self.dataset = dataset
        self.length = min(n,len(dataset))

    def reset(self):
        if self.dataset:
            self.dataset.close()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)
        return self.dataset[item]
    def __len__(self):
        return self.length
class SkipRandomDataset(RandomDatasetBase):
    def __init__(self, dataset, n):
        self.dataset = dataset
        self.n = n

    def reset(self):
        if self.dataset:
            self.dataset.close()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)
        return self.dataset[item + self.n]

    def __len__(self):
        return min(len(self.dataset) - self.n,0)

class MapRandomDataset(RandomDatasetBase):
    def __init__(self,dataset,transform_fn: typing.Callable):
        self.dataset = dataset
        self.transform_fn = transform_fn

    def reset(self):
        if self.dataset:
            self.dataset.close()

    def __getitem__(self, item):
        if isinstance(item,slice):
            return self.__getitem_slice__(item)

        if self.transform_fn:
            return self.transform_fn(self.dataset[item])
        return self.dataset[item]

    def __len__(self):
        return len(self.dataset)

class BatchRandomDataset(RandomDatasetBase):
    def __init__(self,dataset,batch_size: int,drop_remainder:bool=False):
        assert batch_size > 0
        self.dataset = dataset
        self.batch_size_ = batch_size
        self.drop_remainder = drop_remainder

        self.length = math.floor(len(self.dataset) / batch_size) if self.drop_remainder else math.ceil(len(self.dataset) / batch_size)

    @property
    def batch_size(self):
        return self.batch_size_

    def reset(self):
        if self.dataset:
            self.dataset.close()
    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        buffer = []
        if not self.drop_remainder and item == self.length -1 :
            for i in range(min(self.batch_size_,len(self.dataset) % self.batch_size_)):
                buffer.append(self.dataset[item * self.batch_size_ + i])
        else:
            for i in range(self.batch_size_):
                buffer.append(self.dataset[item * self.batch_size_ + i])
        return buffer

    def __len__(self):
        return self.length

class UnBatchRandomDataset(RandomDatasetBase):
    def __init__(self,dataset):
        d = dataset
        is_ok = False
        while True:
            if hasattr(d, 'dataset'):
                if isinstance(d, BatchRandomDataset):
                    is_ok = True
                    break
            else:
                break
            d = d.dataset

        assert is_ok, 'dataset must be BatchDataset'

        self.dataset = dataset
        self.length = len(d.dataset) if not d.drop_remainder else len(d.dataset) - (len(d.dataset)  % d.batch_size)

        print('*' * 30,self.length,len(d.dataset),(len(d.dataset)  % d.batch_size))
        self.batch_size = d.batch_size

    def reset(self):
        if self.dataset:
            self.dataset.close()
    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        batch_id = item // self.batch_size
        id = item % self.batch_size
        d = self.dataset[batch_id][id]
        return d

    def __len__(self):
        return self.length


class ShuffleRandomDataset(RandomDatasetBase):
    def __init__(self, dataset,buffer_size,seed=None,size=-1):
        self.dataset = dataset

        if size < 0:
            size = len(self.dataset)
        size = min(size,len(self.dataset))
        self.length = size

        if buffer_size < 0:
            buffer_size = len(dataset)
        self.buffer_size = buffer_size

        assert self.buffer_size > 0

        self.seed = seed

        self.buffer = list(range(self.buffer_size))
        np.random.shuffle(self.buffer)

        self.last_buffer_id =  math.floor(self.length / self.buffer_size)
    def reset(self):
        if self.dataset:
            self.dataset.close()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__getitem_slice__(item)

        start = item // self.buffer_size
        offset = item % self.buffer_size
        if start != self.last_buffer_id:
            offset = self.buffer[offset]
            item = start * self.buffer_size + offset
        d = self.dataset[item]
        return d
    def __len__(self):
        return self.length