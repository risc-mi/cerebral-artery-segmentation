import numpy as np

from miua2024b.source.points import downsample_points, show_pointclouds, transform_points
from miua2024b.source.util import default



def register_points_affine(moving, fixed, spacing_search: float = 1.0, spacing_refine: float = 0.5, show=False):
    """
    uses a two-step global (ransac) and local (ICP) method to register two point clouds
    :param moving: moving point cloud
    :param fixed: fixed point cloud
    :param spacing: fixed spacing to use during registration
    :return: affine registration matrix
    """
    moving_down = downsample_points(moving, spacing_search)
    fixed_down = downsample_points(fixed, spacing_search)
    tm1 = register_points_ransac_open3d(moving_down, fixed_down, spacing=spacing_search)

    moving_down = downsample_points(moving, spacing_refine)
    fixed_down = downsample_points(fixed, spacing_refine)
    tm2 = register_points_icp(moving_down, fixed_down, tm1, t_bounds=(5 * spacing_refine, 0.5 * spacing_refine), t_steps=1000)

    if show:
        show_pointclouds([moving_down, transform_points(moving_down, tm2), fixed_down])
    return tm2


def register_points_icp(moving, fixed, t_init=None, t_bounds=None, t_steps=None, max_its=100):
    """
    uses the open3d implementation of ICP to register two point clouds
    :param moving: moving point cloud
    :param fixed: destination point cloud
    :param t_init: initial transformation
    :param t_bounds: the upper and lower bound for the ICP threshold
    :param t_steps: the number of ICP runs to execute
    :param max_its: the maximum number of iterations per ICP run
    :return: affine registration matrix
    """
    import open3d as o3d
    import open3d.pipelines.registration as o3r

    t_bounds = default(t_bounds, (1, 1))
    t_steps = default(t_steps, 1)
    t_init = default(t_init, np.eye(4))

    moving = moving if isinstance(moving, o3d.geometry.PointCloud) else o3d.geometry.PointCloud(o3d.utility.Vector3dVector(moving))
    fixed = fixed if isinstance(fixed, o3d.geometry.PointCloud) else o3d.geometry.PointCloud(o3d.utility.Vector3dVector(fixed))

    t_curr = t_init
    for i in range(t_steps):
        t_fac = np.power((t_steps - i) / t_steps, 3)
        threshold = t_bounds[0] * t_fac + t_bounds[1] * (1 - t_fac)

        est = o3r.TransformationEstimationPointToPoint()
        crit = o3r.ICPConvergenceCriteria()
        crit.max_iteration = max_its
        res = o3r.registration_icp(moving, fixed, threshold, t_curr, est, crit)
        t_curr = res.transformation

    return res.transformation


def register_points_ransac_open3d(moving, fixed, maxit=1000000, spacing:float =3, max_nn=30):
    """
    uses the open3d implementation of RANSAC to perform global registration of two point clouds
    :param moving: moving point cloud
    :param fixed: destination point cloud
    :param t_init: initial transformation
    :param t_bounds: the upper and lower bound for the ICP threshold
    :param t_steps: the number of ICP runs to execute
    :param max_its: the maximum number of iterations per ICP run
    :return: affine registration matrix
    """

    import open3d as o3d
    import open3d.pipelines.registration as o3r
    kdtype = o3d.geometry.KDTreeSearchParamHybrid

    moving = moving if isinstance(moving, o3d.geometry.PointCloud) else o3d.geometry.PointCloud(o3d.utility.Vector3dVector(moving))
    fixed = fixed if isinstance(fixed, o3d.geometry.PointCloud) else o3d.geometry.PointCloud(o3d.utility.Vector3dVector(fixed))

    def _preprocess(pcd, voxel_size):
        pcd_down = pcd.voxel_down_sample(voxel_size)
        pcd_down.normals = o3d.utility.Vector3dVector(np.repeat((0, 1, 0), len(pcd_down.points)).reshape((3, -1)).T)
        pcd_fpfh = o3r.compute_fpfh_feature(pcd_down, kdtype(radius=voxel_size * 5, max_nn=3*max_nn))
        return pcd_down, pcd_fpfh

    distance_threshold = spacing * 1.5
    moving_down, moving_fpfh = _preprocess(moving, spacing)
    fixed_down, fixed_fpfh = _preprocess(fixed, spacing)
    res = o3r.registration_ransac_based_on_feature_matching(
        moving_down, fixed_down, moving_fpfh, fixed_fpfh, True,
        distance_threshold,
        o3r.TransformationEstimationPointToPoint(False), 3,
        [o3r.CorrespondenceCheckerBasedOnDistance(distance_threshold)], o3r.RANSACConvergenceCriteria(maxit, 0.999))
    return res.transformation
