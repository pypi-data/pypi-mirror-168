# Copyright 2022 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Union

from enum import Enum, unique
import numpy as np
from sklearn.model_selection import train_test_split as _train_test_split

from secretflow.data.io import util as io_util
from secretflow.device import PYU, PYUObject, reveal
from secretflow.utils.errors import InvalidArgumentError

# 下面的函数是同时支持水平和垂直的。
__ndarray = "__ndarray_type__"


@unique
class PartitionWay(Enum):
    """The partitioning.
    HORIZONTAL: horizontal partitioning.
    VERATICAL: vertical partitioning.
    """

    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


@dataclass
class FedNdarray:
    """Horizontal or vertical partitioned Ndarray.

    Attributes:
        partitions (Dict[PYU, PYUObject]): List of references to
            local numpy.ndarray that makes up federated ndarray.
    """

    partitions: Dict[PYU, PYUObject]
    partition_way: PartitionWay

    @reveal
    def partition_shape(self):
        """Get ndarray shapes of all partitions."""
        return {
            device: device(lambda partition: partition.shape)(partition)
            for device, partition in self.partitions.items()
        }

    @property
    def shape(self) -> Tuple[int, int]:
        """Get shape of united ndarray."""
        shapes = self.partition_shape()

        if len(shapes) == 0:
            return (0, 0)

        # no check shapes. assume arrays are aligned by split axis and has same dimension.
        first_shape = list(shapes.values())[0]
        assert len(first_shape) <= 2, "only support get shape on 1/2-D array"

        if len(first_shape) == 1:
            # 1D-array
            assert (
                len(shapes) == 1
            ), "can not get shape on 1D-array with multiple partitions"
            return first_shape

        if self.partition_way == PartitionWay.VERTICAL:
            rows = first_shape[0]
            cols = sum([shapes[d][1] for d in shapes])
        else:
            rows = sum([shapes[d][0] for d in shapes])
            cols = first_shape[1]

        return (rows, cols)

    def astype(self, dtype, order='K', casting='unsafe', subok=True, copy=True):
        """Cast to a specified type.

        All args are same with :py:meth:`numpy.ndarray.astype`.
        """
        return FedNdarray(
            partitions={
                device: device(
                    lambda a, dtype, order, casting, subok, copy: a.astype(
                        dtype, order=order, casting=casting, subok=subok, copy=copy
                    )
                )(partition, dtype, order, casting, subok, copy)
                for device, partition in self.partitions.items()
            },
            partition_way=self.partition_way,
        )

    def __getitem__(self, item) -> 'FedNdarray':
        return FedNdarray(
            partitions={
                pyu: pyu(np.ndarray.__getitem__)(self.partitions[pyu], item)
                for pyu in self.partitions
            },
            partition_way=self.partition_way,
        )


def load(
    sources: Dict[PYU, Union[str, Callable[[], np.ndarray], PYUObject]],
    partition_way: PartitionWay = PartitionWay.VERTICAL,
    allow_pickle=False,
    encoding='ASCII',
) -> FedNdarray:
    """Load FedNdarray from data source.

    .. warning:: Loading files that contain object arrays uses the ``pickle``
                 module, which is not secure against erroneous or maliciously
                 constructed data. Consider passing ``allow_pickle=False`` to
                 load data that is known not to contain object arrays for the
                 safer handling of untrusted sources.

    Args:
        sources: Data source in each partition. Shall be one of the followings.
            1) Loaded numpy.ndarray.
            2) Local filepath which should be `.npy` or `.npz` file.
            3) Callable function that return numpy.ndarray.
        allow_pickle: Allow loading pickled object arrays stored in npy files.
        encoding: What encoding to use when reading Python 2 strings.

    Raises:
        TypeError: illegal source。

    Returns:
        Return a FedNdarray if source is pyu object or .npy. Or return a dict
        {key: FedNdarray} if source is .npz.

    Examples:
        >>> fed_arr = load({'alice': 'example/alice.csv', 'bob': 'example/alice.csv'})
    """

    def _load(content) -> Tuple[List, List]:
        if isinstance(content, str):
            data = np.load(
                io_util.open(content), allow_pickle=allow_pickle, encoding=encoding
            )
        elif isinstance(content, Callable):
            data = content()
        else:
            raise TypeError(f"Unsupported source with {type(content)}.")
        assert isinstance(data, np.ndarray) or isinstance(data, np.lib.npyio.NpzFile)
        if isinstance(data, np.lib.npyio.NpzFile):
            files = data.files
            data_list = []
            for file in files:
                data_list.append(data[file])
            return files, data_list
        else:
            return [__ndarray], [data]

    def _get_item(file_idx, data):
        return data[file_idx]

    file_list = []
    data_dict = {}
    pyu_parts = {}

    for device, content in sources.items():
        if isinstance(content, PYUObject) and content.device != device:
            raise InvalidArgumentError('Device of source differs with its key.')
        if not isinstance(content, PYUObject):
            files, datas = device(_load)(content)
            file_list.append(reveal(files))
            data_dict[device] = datas
        else:
            pyu_parts[device] = content
    # 处理pyu object
    if pyu_parts:
        return FedNdarray(partitions=pyu_parts, partition_way=partition_way)

    # 检查各方的数据是否一致
    file_list_lens = set([len(file) for file in file_list])
    if len(file_list_lens) != 1:
        raise Exception(
            f"All parties should have same structure,but got file_list = {file_list}"
        )

    file_names = file_list[0]
    result = {}
    for idx, m in enumerate(file_names):
        parts = {}
        for device, data in data_dict.items():
            parts[device] = device(_get_item)(idx, data)
        if m == __ndarray and len(file_names) == 1:
            return FedNdarray(partitions=parts, partition_way=partition_way)
        result[m] = FedNdarray(partitions=parts, partition_way=partition_way)
    return result


def train_test_split(
    data: FedNdarray, ratio: float, random_state: int = None, shuffle=True
) -> Tuple[FedNdarray, FedNdarray]:
    """Split data into train and test dataset.

    Args:
        data: Data to split.
        ratio: Train dataset ratio.
        random_state: Controls the shuffling applied to the data before applying the split.
        shuffle: Whether or not to shuffle the data before splitting.

    Returns:
        Tuple of train and test dataset.
    """
    assert data.partitions, 'Data partitions are None or empty.'
    assert 0 < ratio < 1, f"Invalid split ratio {ratio}, must be in (0, 1)"

    if random_state is None:
        random_state = random.randint(0, 2**32 - 1)

    assert isinstance(random_state, int), f'random_state must be an integer'

    def split(*args, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        if len(args[0].shape) == 0:
            return np.array(None), np.array(None)
        results = _train_test_split(*args, **kwargs)
        return results[0], results[1]

    parts_train, parts_test = {}, {}
    for device, part in data.partitions.items():
        parts_train[device], parts_test[device] = device(split)(
            part, train_size=ratio, random_state=random_state, shuffle=shuffle
        )
    return (
        FedNdarray(parts_train, data.partition_way),
        FedNdarray(parts_test, data.partition_way),
    )


def shuffle(data: FedNdarray):
    """Random shuffle data.

    Args:
        data: data to be shuffled.
    """
    rng = np.random.default_rng()

    if data.partitions is not None:

        def _shuffle(rng: np.random.Generator, part: np.ndarray):
            new_part = deepcopy(part)
            rng.shuffle(new_part)
            return new_part

        for device, part in data.partitions.items():
            device(_shuffle)(rng, part)
