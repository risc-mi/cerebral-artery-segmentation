import sys

import numpy as np
import SimpleITK as sitk

from miua2024b.source.colors import default_palette
from miua2024b.source.util import as_list, native


def downsample_points(points, radius: float=1):
    """
    resamples the point clouds to the specified radius using the method in "Parallel Poisson Disk Sampling with Spectrum Analysis on Surface"
    (http://graphics.cs.umass.edu/pubs/sa_2010.pdf)
    :param points: ndarray
    :param radius: radius to downsample to
    :return: resampled point cloud
    """
    import point_cloud_utils as pcu
    points = np.asarray(points)
    mask = pcu.downsample_point_cloud_poisson_disk(points, target_num_samples=-1, radius=radius)
    return points[mask]


def show_pointclouds(pcls: list, palette=None):
    """
    shows a list of point clouds in individual colors
    :param pcls: list of 3d pointclouds, which can be open3d pointclouds or numpy arrays
    :param palette: optional custom palette to assign colors to each point cloud
    """
    pcls = as_list(pcls)
    if palette is None:
        palette = default_palette(len(pcls))

    import open3d as o3d
    geos = list()
    for rgb, pcl in zip(palette, pcls):
        if not isinstance(pcl, o3d.geometry.PointCloud):
            if not isinstance(pcl, o3d.utility.Vector3dVector):
                pcl = o3d.utility.Vector3dVector(pcl)
            pcl = o3d.geometry.PointCloud(pcl)
            pcl.paint_uniform_color(np.divide(rgb, 255))
        geos.append(pcl)
    o3d.visualization.draw_geometries(geos)


def transform_points(points, tf):
    """
    generic method to transform a list/array of points, support different transform types
    :returns transformed points
    """

    if all(hasattr(tf, attr) for attr in ['dtype', 'shape', 'ndim']):
        tf = np.asarray(tf)
        if tf.ndim != 2:
            RuntimeError("Invalid transform matrix dimension: {}".format(tf.ndim))
        if tf.shape[0] != tf.shape[1]:
            RuntimeError("Invalid transform matrix shape: {}".format(tf.shape))
        mat = tf[:-1, :-1].flatten().tolist()
        trans = tf[:-1, -1].tolist()

        import SimpleITK as sitk
        tf = sitk.AffineTransform(mat, trans)

    if 'SimpleITK' in sys.modules:
        import SimpleITK as sitk
        if isinstance(tf, sitk.Transform):
            return np.asarray(list(tf.TransformPoint(p) for p in points))

    raise RuntimeError("Invalid transform type: {}".format(type(tf).__name__))


def mask_to_points(mask: sitk.Image, method='numpy'):
    """
    Converts a binary mask image to a point cloud
    The numpy method (default) should >10x faster than the simpleitk method (the actual calculation by >100x)
    The SimpleITK method is the reference implementation to check when in doubt concerning the results
    The maximum difference between methods for tested images was below 1e-9
    :param mask: mask image to convert
    :param method: which method to use for conversion, 'numpy' or 'sitk'
    :return: point coordinates
    """
    coords = np.asarray(sitk.GetArrayViewFromImage(mask).T.nonzero()).T

    method = method.lower()
    if method in ('itk', 'sitk', 'simpleitk'):
        points = list(mask.TransformIndexToPhysicalPoint(native(c)) for c in coords)
    elif method in ('np', 'numpy'):
        dims = mask.GetDimension()
        origin = mask.GetOrigin()
        spacing = mask.GetSpacing()
        m_dir = np.asarray(mask.GetDirection()).reshape([dims] * 2)
        m_scl = np.multiply(spacing, np.eye(dims))
        points = np.add(origin, (m_dir @ m_scl @ coords.T).T)
    else:
        raise RuntimeError("Unknown method for mask to points conversion: {}".format(method))
    return np.asarray(points)


def downsample(points, radius=1):
    import point_cloud_utils as pcu
    mask = pcu.downsample_point_cloud_poisson_disk(points, -1, radius=radius)
    return points[mask]
