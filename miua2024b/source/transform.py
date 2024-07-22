import SimpleITK as sitk
import numpy as np

from miua2024b.source.util import unit_vector


def evaluate_transforms(pred: sitk.Transform, truth: sitk.Transform, ref: tuple):
    """
    returns a dictionary of metrics comparing two transforms, pred and truth
    :param pred: predicted transform
    :param truth: expected transform
    :param ref: reference coordinate
    :return: a dictionary of evaluation metrics
        'angle.diff': the angle difference in radians
        'angle.diff.deg': the angle difference in degrees
        'trans.diff': the difference vector (x, y, z)
        'trans.diff.norm': the length of the difference vector
    """
    t_diff = np.abs(np.subtract(pred.TransformPoint(ref), truth.TransformPoint(ref)))
    n_diff = np.linalg.norm(t_diff)

    r_diffs = list()
    for axis_idx in range(3):
        v_axis = [0] * 3
        v_axis[axis_idx] = 1
        v_axis = tuple(v_axis)
        v_pred = np.squeeze(unit_vector(pred.TransformVector(v_axis, ref)))
        v_truth = np.squeeze(unit_vector(truth.TransformVector(v_axis, ref)))
        r_diff = np.arccos(np.clip(np.dot(v_pred, v_truth), a_min=0.0, a_max=1.0))
        r_diffs.append(r_diff)
    r_diff = np.mean(r_diffs)
    return n_diff, np.rad2deg(r_diff)