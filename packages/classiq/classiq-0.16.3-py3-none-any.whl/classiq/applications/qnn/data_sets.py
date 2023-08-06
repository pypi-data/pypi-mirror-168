from typing import Callable, Optional, Tuple

import numpy as np
from torch import Tensor, tensor
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import Lambda

from classiq.exceptions import ClassiqIndexError

Transform = Callable[[Tensor], Tensor]


#
# Utils for `DatasetNot`
#
def all_bits_to_one(n: int) -> int:
    """
    Return an integer of length `n` bits, where all the bits are `1`
    """
    return (2**n) - 1


def all_bits_to_zero(n: int) -> int:
    """
    Return an integer of length `n` bits, where all the bits are `0`
    """
    return 0


#
# Transformers for `DatasetNot`
#
def state_to_weights(pure_state: Tensor) -> Tensor:
    """
    input: a `Tensor` of binary numbers (0 or 1)
    output: the required angle of rotation for `Rx`
    (in other words, |0> translates to no rotation, and |1> translates to `pi`)
    """
    # |0> requires a rotation by 0
    # |1> requires a rotation by pi
    return pure_state.bool().int() * np.pi


def state_to_label(pure_state: Tensor) -> Tensor:
    """
    input: a `Tensor` of binary numbers (0 or 1) - the return value of a measurement
    output: probability (from that measurement) of measuring 0
    (in other words,
        |0> translates to 100% chance for measuring |0> ==> return value is 1.0
        |1> translates to   0% chance for measuring |0> ==> return value is 0.0
    )
    """
    # |0> means 100% chance to get |0> ==> 100% == 1.0
    # |1> means   0% chance to get |0> ==>   0% == 0.0

    # This line basically does `1 - bool(pure_state)`
    return 1 - pure_state.bool().int()


class DatasetNot(Dataset):
    def __init__(
        self,
        n: int = 2,
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        self._n = n
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor]:
        if index == 0:
            the_data = all_bits_to_zero(self._n)
            the_label = all_bits_to_one(self._n)
        elif index == 1:
            the_data = all_bits_to_one(self._n)
            the_label = all_bits_to_zero(self._n)
        else:
            raise ClassiqIndexError(f"{self.__class__.__name__} out of range")

        data = tensor([the_data])
        if self.transform:
            data = self.transform(data)

        label = tensor([the_label])
        if self.target_transform:
            label = self.target_transform(label)

        return data.float(), label.float()


class DatasetXor(Dataset):
    def __init__(
        self,
        n: int = 2,
        transform: Optional[Transform] = None,
        target_transform: Optional[Transform] = None,
    ):
        self._n = n
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self) -> int:
        return 2**self._n

    def __getitem__(self, index: int) -> Tuple[Tensor, Tensor]:
        if index < 0 or index >= len(self):
            raise ClassiqIndexError(f"{self.__class__.__name__} out of range")

        bin_str = bin(index)[2:].zfill(self._n)
        data_value = map(int, reversed(bin_str))

        label_value = bin_str.count("1") % 2

        data = tensor(list(data_value))
        if self.transform:
            data = self.transform(data)

        label = tensor(int(label_value))
        if self.target_transform:
            label = self.target_transform(label)

        return data.float(), label.float()


DATASET_NOT = DatasetNot(
    1, transform=Lambda(state_to_weights), target_transform=Lambda(state_to_label)
)
DATALOADER_NOT = DataLoader(DATASET_NOT, batch_size=2, shuffle=True)

DATASET_XOR = DatasetXor()
DATALOADER_XOR = DataLoader(DATASET_XOR, batch_size=4, shuffle=True)
