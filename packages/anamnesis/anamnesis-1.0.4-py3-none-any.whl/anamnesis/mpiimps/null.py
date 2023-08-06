#!/usr/bin/python3

# vim: set expandtab ts=4 sw=4:

"""Null (non-available) MPI implementation"""

from typing import Any, List, Optional, Tuple

import numpy as np

__all__ = []


class NullMPIImplementor(object):
    """
    Singleton fake MPI Class which doesn't even depend on the MPI module being
    available
    """

    __shared_state = {}

    def __init__(self, *args, **kwargs):
        # Quick way of implementing a singleton
        self.__dict__ = self.__shared_state

        if not getattr(self, "initialised", False):
            self.initialised = True
            self.setup(*args, **kwargs)

    def setup(self, use_mpi: bool = False) -> None:
        self.rank = 0
        self.size = 1
        self.master = True

    def recv(
        self,
        obj: Optional[np.ndarray] = None,
        source: int = 0,
        tag: int = 0,
        status: Optional[Any] = None,
    ) -> np.ndarray:
        return obj

    def send(
        self, obj: Optional[np.ndarray] = None, dest: int = 0, tag: int = 0
    ) -> np.ndarray:
        return obj

    def bcast(self, data_in: Optional[np.ndarray] = None, root: int = 0) -> np.ndarray:
        return data_in

    def get_scatter_indices(self, num_pts: int) -> List[Tuple[int, int]]:
        return [
            (
                0,
                num_pts,
            )
        ]

    def scatter_array(
        self, data_in: Optional[np.ndarray] = None, root: int = 0
    ) -> np.ndarray:
        return data_in

    def scatter_list(
        self, data_in: Optional[List[Any]] = None, root: int = 0
    ) -> List[Any]:
        return data_in

    def gather(self, data_in: Optional[np.ndarray], root: int = 0) -> np.ndarray:
        return data_in

    def allgather(self, data_in: Optional[np.ndarray], root: int = 0) -> np.ndarray:
        return data_in

    def gather_list(
        self, data_in: Optional[List[Any]], total_trials: int, return_all: bool = False
    ) -> List[Any]:
        return data_in

    def abort(self) -> None:
        return


__all__.append("NullMPIImplementor")
