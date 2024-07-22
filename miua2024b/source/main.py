import argparse
import sys
from time import time
from typing import Optional

import SimpleITK as sitk

from miua2024b.source.points import mask_to_points
from miua2024b.source.registration import register_points_affine
from miua2024b.source.transform import evaluate_transforms
from miua2024b.source.util import transform_from_affine, get_center, format_array


def run(fixed_img_path: str, moving_img_path: str, dest_path: str,
        truth_path: Optional[str]=None, warped_path: Optional[str]=None,
        show=False, binary=False, search_mm:float=1.0, fine_mm=1.5):
    """
    Runs the registration method for vessels using segmentation images of target structures
    :param fixed_img_path: segmentation of the fixed image
    :param moving_img_path: segmentation of the moving image
    :param dest_path: output path for the resulting transform, must have an extension supported by SimpleITK, e.g., .tfm
    :param truth_path: path to the truth transform to evaluate against, must have an extension supported by SimpleITK, e.g., .tfm or .hdf
    :param warped_path: path to the truth transform to evaluate against, must have an extension supported by SimpleITK, e.g., .tfm or .hdf
    :param show: whether to visualize the registered point clouds
    :param binary: whether to mask all labels instead of extracting the left and right labels predicted by model theta m
    :param search_mm: resolution for the global RANSAC registration (in mm for the poison disk radius)
    :param fine_mm: resolution for the fine ICP registration (in mm for the poison disk radius)
    :return: affine transformation resulting aligning the fixed and moving image.
    """

    # read the segmentation images
    print(f"Reading fixed image: {fixed_img_path}")
    fixed_img = sitk.ReadImage(fixed_img_path)
    fixed_mask = fixed_img != 1 if binary else sitk.Or(fixed_img == 4, fixed_img == 5)
    fixed_mask.CopyInformation(fixed_img)

    print(f"Reading moving image: {moving_img_path}")
    moving_img = sitk.ReadImage(moving_img_path)
    moving_mask = moving_img != 1 if binary else sitk.Or(moving_img == 4, moving_img == 5)
    moving_mask.CopyInformation(moving_img)

    # convert the masks to point-clouds
    fixed = mask_to_points(fixed_mask)
    moving = mask_to_points(moving_mask)

    # perform the registration
    print("Running registration...", end='')
    t0 = time()
    tf = register_points_affine(fixed, moving, show=show, spacing_search=search_mm, spacing_refine=fine_mm)
    print("\rFinished registration in {:.2f} seconds!".format(time()-t0))

    # write the result
    tf = transform_from_affine(tf)
    sitk.WriteTransform(tf, dest_path)
    print(f"Finished writing results to: {dest_path}")

    if truth_path:
        # evaluate result
        print(f"Reading truth transform: {truth_path}")
        tf_truth = sitk.ReadTransform(truth_path)
        ref_pos = get_center(fixed_img)
        n_diff, r_diff = evaluate_transforms(pred=tf, truth=tf_truth, ref=ref_pos)
        print("Results:\n"
              "* translation error: n: {:0.2f} mm\n"
              "* rotation error: {:0.1f}°"
              "".format(n_diff, r_diff))

    if warped_path:
        # write warped image
        warped = sitk.Resample(moving_img, fixed_img, tf)
        sitk.WriteImage(warped, warped_path)

def entry_point():
    parser = argparse.ArgumentParser(description='Registration method for cerebral vasculature.')
    parser.add_argument('--fixed', dest='fixed', type=str, required=True, help="Segmentation of vessels in the fixed image")
    parser.add_argument('--moving', dest='moving', type=str, required=True, help="Segmentation of vessels in the moving image")
    parser.add_argument('--output', dest='output', type=str, required=True, help="Output path for the resulting transform, must have an extension supported by SimpleITK, e.g., .tfm or .hdf")
    parser.add_argument('--truth', dest='truth', type=str, default="", help="Truth transform to evaluate against, must have an extension supported by SimpleITK, e.g., .tfm or .hdf")
    parser.add_argument('--warped', dest='warped', type=str, default="", help="Warped image to write, must have an extension supported by SimpleITK, e.g., .nrrd")
    parser.add_argument('--show', dest='show', action='store_true', help="Whether to visualize the registered point-clouds")
    parser.add_argument('--binary', dest='binary', action='store_true', help="Whether to mask all lables instead of extracting the left and right labels predicted by model theta m")
    parser.add_argument('--search', dest='search', type=float, default='1.5', help="Resolution for the global RANSAC registration (in mm for the poison disk radius)")
    parser.add_argument('--fine', dest='fine', type=float, default='1.0', help="Resolution for the fine ICP registration (in mm for the poison disk radius)")
    args, _ = parser.parse_known_args(args=sys.argv)

    run(fixed_img_path=args.fixed,
        moving_img_path=args.moving,
        dest_path=args.output,
        truth_path=args.truth,
        warped_path=args.warped,
        show=args.show,
        binary=args.binary,
        search_mm=args.search,
        fine_mm=args.fine)


if __name__ == '__main__':
    entry_point()
