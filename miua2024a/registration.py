import os
import ants
import tempfile
import SimpleITK as sitk


def registeration_rigid(fixed_path: str, moving_path: str, output_dir: str):
    """ Rigid registration using the ANTSPy package """
    fixed_volume = ants.image_read(fixed_path)
    moving_volume = ants.image_read(moving_path)
    result = ants.registration(
        fixed=fixed_volume,
        moving=moving_volume,
        type_of_transform='DenseRigid'
    )
    output_path = os.path.join(output_dir, f"rigid_{os.path.basename(moving_path)}")
    ants.image_write(result['warpedmovout'], output_path)


def registration_affine(fixed_path: str, moving_path: str, output_dir: str):
    """ Affine registration using the NiftyReg package """
    fixed_volume = sitk.ReadImage(fixed_path)
    moving_volume = sitk.ReadImage(moving_path)
    with tempfile.TemporaryDirectory(dir=output_dir) as temp_dir:
        fixed_temp = os.path.join(temp_dir, f"fixed_volume.nii.gz")
        moving_temp = os.path.join(temp_dir, f"moving_volume.nii.gz")
        sitk.WriteImage(fixed_volume, fixed_temp)
        sitk.WriteImage(moving_volume, moving_temp)
        output_name = os.path.join(output_dir, os.path.basename(fixed_path))
        output_name = f"affine_{output_name}"

        # Perform registration
        os.system(f"niftyreg aladin.exe -ref {fixed_temp} -flo {moving_temp} -res {output_name}")


if __name__ == '__main__':
    fixed = r"path to fixed image"
    moving = r"path to moving image"
    output_folder = r"folder to store output file"
    registeration_rigid(
        fixed_path=fixed,
        moving_path=moving,
        output_dir=output_folder
    )
