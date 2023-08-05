import  numpy as np
from typing import Sized


def _get_all_dimensions(batch, level: int = 0, res = None):
    """Return all presented element sizes of each dimension.

    Args:
        batch: Data array.
        level: Recursion level.
        res: List containing element sizes of each dimension.

    Return:
        List, i-th element of which is list containing all presented sized of batch's i-th dimension.

    Examples:
        >>> x = [[[1], [2, 3]], [[4], [5, 6, 7], [8, 9]]]
        >>> _get_all_dimensions(x)
        [[2], [2, 3], [1, 2, 1, 3, 2]]

    """
    if not level:
        res = [[len(batch)]]
    if len(batch) and isinstance(batch[0], Sized) and not isinstance(batch[0], str):
        level += 1
        if len(res) <= level:
            res.append([])
        for item in batch:
            res[level].append(len(item))
            _get_all_dimensions(item, level, res)
    return res



def get_dimensions(batch):
    """Return maximal size of each batch dimension."""
    return list(map(max, _get_all_dimensions(batch)))


def pad(batch,zp_batch= None, dtype = np.float32, padding = 0):
    """Fills the end of each array item to make its length maximal along each dimension.

    Args:
        batch: Initial array.
        zp_batch: Padded array.
        dtype = Type of padded array.
        padding = Number to will initial array with.

    Returns:
        Padded array.

    Examples:
        >>> x = np.array([[1, 2, 3], [4], [5, 6]])
        >>> zero_pad(x)
        array([[1., 2., 3.],
               [4., 0., 0.],
               [5., 6., 0.]], dtype=float32)

    """
    if zp_batch is None:
        dims = get_dimensions(batch)
        zp_batch = np.ones(dims, dtype=dtype) * padding
    if zp_batch.ndim == 1:
        zp_batch[:len(batch)] = batch
    else:
        for b, zp in zip(batch, zp_batch):
            zero_pad(b, zp)
    return zp_batch
