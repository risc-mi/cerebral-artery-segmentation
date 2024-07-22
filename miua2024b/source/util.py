from typing import Optional, Any
import numpy as np
import SimpleITK as sitk


def native(val, dtype=None, force=False):
    """
    Converts value from a numpy to native python type if applicable, otherwise pass through.
    :param val: value to convert
    :param dtype: optional dtype to cast to
    :param force: convert also if val is not a numpy type
    :return: 'native' python value
    """
    if hasattr(val, 'dtype'):
        if np.isscalar(val):
            return val.item() if dtype is None else val.astype(dtype).item()
        return np.asarray(val, dtype=dtype).tolist()
    elif force:
        return native(np.asarray(val, dtype=dtype))
    return val


def default(val: Optional[Any], d: Any):
    """
    returns a default value if val is not set (None) or otherwise val
    :param val: value to check
    :param d: default value
    """
    return d if val is None else val


def as_list(a) -> list:
    """
    Convert an item which may be a container or a scalar to a list
    """
    if hasattr(a, '__iter__') and not isinstance(a, str):
        return list(a)
    return [a] if a is not None else []


def as_tuple(a) -> tuple:
    """
    Convert an item which may be a container or a scalar to a tuple
    """
    if hasattr(a, '__iter__') and not isinstance(a, str):
        return tuple(a)
    return (a, ) if a is not None else tuple()


def transform_from_affine(m):
    """
    converts a affine matrix to a simpleITK affine transformation
    :param m: 2d affine matrix
    :return: corresponding sitk.AffineTransform
    """
    t = sitk.AffineTransform(3)
    t.SetMatrix(m[:3, :3].flatten())
    t.SetTranslation(m[:3, 3])
    return t


def get_center(img: sitk.Image):
    """
    returns the center of an image as an absolute position
    """
    center = get_center_index(img, round=False)
    return img.TransformContinuousIndexToPhysicalPoint(center)


def get_center_index(img: sitk.Image, round=True):
    """
    returns the center of an image as an index
    :param round: whether to round the index to an integer
    """
    c = np.divide(img.GetSize(), 2)
    if round:
        c = np.round(c).astype(int)
    return native(c)


def unit_vector(v, axis=-1, div0=np.NAN):
    """
    converts a vector or vector matrix to convert to unit vectors
    :param v: vector or vector matrix to convert
    :param axis: axis to normalize, defaults to the last axis
    :param div0: value to return where the unit length is zero
    :return: normalized unit vector result
    """
    v = np.asanyarray(v, dtype=float)
    n = np.linalg.norm(v, axis=axis)
    reorder = axis != 0
    if reorder:
        v = np.moveaxis(v, axis, 0)
    v = np.divide(v, n, out=np.full_like(v, div0), where=n!=0)
    if reorder:
        v = np.moveaxis(v, 0, axis)
    return v


def format_array(a, p=3, sep=", "):
    """
    converts an array or scalar to a string
    :param a: array to convert
    :param p: precision to use, applies if any of the values has decimals
    :param sep: separator to use
    """
    a = as_tuple(a)
    use_precision = any(int(v) != v for v in a)
    a = list(np.format_float_positional(v, precision=p, unique=False)
             if use_precision else str(v)
             for v in a)
    return sep.join(a)

