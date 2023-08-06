from sample_util.NLSampleSource import NLSampleSourceBase
from code_util.structures import iter_idx
import random


class SampleSet:
    def __init__(self, source_base: NLSampleSourceBase,
                 set_name: str,
                 ):
        self._sample_source = source_base
        self._set_name = set_name
        self._shuffle = False

        self._data_keys = source_base.get_metadata_keys(set_name)

        self._iter_map = {}
        self._iter_keys = []

        self._func = [self._base_iter]

    def __iter__(self):
        return self._func[-1]()

    @property
    def sample_source(self):
        return self._sample_source

    @property
    def set_name(self):
        return self._set_name

    def count(self):
        return self._sample_source.get_set_count(self._set_name)

    def _base_iter(self):
        totle_count = 0
        for file_index, seek_p in self._sample_source.iter_pointer(self._set_name):
            if file_index not in self._iter_map:
                self._iter_map[file_index] = []
                self._iter_keys.append(file_index)
            self._iter_map[file_index].append(seek_p)
            totle_count += 1

        if self._shuffle:
            random.shuffle(self._iter_keys)
            for key in self._iter_map.keys():
                random.shuffle(self._iter_map[key])

        for key_list in self._iter_keys:
            for p in self._iter_map[key_list]:
                yield self._sample_source.load_pointer_data(self._set_name,
                                                            (key_list, p))

    def shuffle(self):
        self._shuffle = True
        return self

    def take(self, count):
        fun_index = len(self._func) - 1

        def take_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    yield _item
                else:
                    break

        self._func.append(take_func)
        return self

    def skip(self, count):
        fun_index = len(self._func) - 1

        def skip_func():
            kcount = count
            for _item in self._func[fun_index]():
                kcount -= 1
                if kcount >= 0:
                    continue
                else:
                    yield _item

        self._func.append(skip_func)
        return self

    def batch(self, batch_count):
        fun_index = len(self._func) - 1

        def batch_func():
            batch_list = [[] for _ in self._data_keys['label_keys']]

            b_batch_c = 0
            for _item in self._func[fun_index]():
                for key, _idx in iter_idx(self._data_keys['label_keys']):
                    batch_list[_idx].append(_item[_idx])
                b_batch_c += 1

                if b_batch_c == batch_count:
                    yield batch_list
                    b_batch_c = 0
                    batch_list = [[] for _ in self._data_keys['label_keys']]

            if b_batch_c > 0:
                yield batch_list

        self._func.append(batch_func)
        return self
