# -*- coding: utf-8 -*-
# @Time    : 2022/8/20 4:13 下午
# @Author  : ZiUNO
# @Email   : ziunocao@126.com
# @File    : py_seeds.py
# @Software: PyCharm
import logging
import os
import random
import warnings
from collections import OrderedDict
from functools import wraps
from typing import Optional, Callable, Any

import numpy as np
import torch
from torch.cuda import device_count

log = logging.getLogger(__name__)


# TODO: this should be part of the cluster environment
def _get_rank() -> int:
    rank_keys = ("RANK", "SLURM_PROCID", "LOCAL_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)
    return 0


def rank_zero_only(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapped_fn(*args: Any, **kwargs: Any) -> Optional[Any]:
        if rank_zero_only.rank == 0:
            return fn(*args, **kwargs)
        return None

    return wrapped_fn


rank_zero_only.rank = getattr(rank_zero_only, "rank", _get_rank())


@rank_zero_only
def rank_zero_warn(*args, stacklevel: int = 4, **kwargs):
    warnings.warn(*args, stacklevel=stacklevel, **kwargs)


def _select_seed_randomly(min_seed_value: int = 0, max_seed_value: int = 255) -> int:
    return random.randint(min_seed_value, max_seed_value)


def seed_everything(seed: Optional[int] = None) -> int:
    """Function that sets seed for pseudo-random number generators in: pytorch, numpy, python.random In addition,
    sets the following environment variables:

    - `GLOBAL_SEED`: will be passed to spawned subprocesses (e.g. ddp_spawn backend).

    Args:
        seed: the integer value seed for global random state.
            If `None`, will read seed from `GLOBAL_SEED` env variable
            or select it randomly.
    """
    max_seed_value = np.iinfo(np.uint32).max
    min_seed_value = np.iinfo(np.uint32).min

    if seed is None:
        env_seed = os.environ.get("GLOBAL_SEED")
        if env_seed is None:
            seed = _select_seed_randomly(min_seed_value, max_seed_value)
            rank_zero_warn(f"No seed found, seed set to {seed}")
        else:
            try:
                seed = int(env_seed)
            except ValueError:
                seed = _select_seed_randomly(min_seed_value, max_seed_value)
                rank_zero_warn(f"Invalid seed found: {repr(env_seed)}, seed set to {seed}")
    elif not isinstance(seed, int):
        seed = int(seed)

    if not (min_seed_value <= seed <= max_seed_value):
        rank_zero_warn(f"{seed} is not in bounds, numpy accepts from {min_seed_value} to {max_seed_value}")
        seed = _select_seed_randomly(min_seed_value, max_seed_value)

    # using `log.info` instead of `rank_zero_info`,
    # so users can verify the seed is properly set in distributed training.
    log.info(f"Global seed set to {seed}")
    os.environ["GLOBAL_SEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    return seed


def get_seed_state():
    random_state = random.getstate()
    np_state = np.random.get_state()
    torch_state = torch.random.get_rng_state()
    torch_cuda_state = torch.cuda.get_rng_state_all()
    return OrderedDict(random=random_state, numpy=np_state, torch=torch_state, torch_cuda=torch_cuda_state)


def set_seed_state(state: OrderedDict):
    random_state = state["random"]
    np_state = state["numpy"]
    torch_state = state["torch"]
    torch_cuda_state = state["torch_cuda"]

    random.setstate(random_state)
    np.random.set_state(np_state)
    torch.set_rng_state(torch_state)
    for i in range(device_count()):
        torch.cuda.set_rng_state(torch_cuda_state[i], i)
