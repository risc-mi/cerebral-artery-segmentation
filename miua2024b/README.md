# Robust Multi-Modal Registration of Cerebral Vasculature

![overview.png](resource%2Foverview.png)
Figure 1: Overview of our  method for TOF to MR registration.

## About

In this project, we present our code and results on a novel method for registering brain arteries in angiographic and structural MR images (sMRI). Aligning vasculature from angiographic images to sMRI is particularly challenging due to the low contrast in structural sMRI and the sparse nature of vascular structures, which often result in poor alignment when using traditional image-based registration methods. We overcome these challenges through our automatic segmentation method.

Our fully automated method is outlined for the TOF-MR registration in Figure 1. 
We tested our method the data of the public [IXI](https://brain-development.org/ixi-dataset/) and [TubeTK](https://public.kitware.com/Wiki/TubeTK/Data) datasets.
Using our method, we achieved a 100% alignment success at an average of 1.7 mm translation error and 0.7 degrees rotation error.
In our paper, we also evaluated DSA-MR registration, however, on a private dataset.

Please refer to our [publication](#References) if you are interested in the details.

## How to use

The code in this repository offers our registration method and evaluation utilities in a compact command-line tool. With this tool, you can automatically register a floating (TOF) image and a reference (sMRI) image, then save the resulting transform and warped image. Additionally, the tool can visualize the alignment using point clouds and calculate error metrics when a ground-truth transform is provided.


### Preparing the vessel segmentations

Before running the registration method, the cerebral vessels need to be extracted from the fixed and moving images. This can be done using the segmentation method &#952;<sub>M</sub>, which we previously published in [repository](https://github.com/risc-mi/cerebral-artery-annotation). Please refer to the repository for details on how to use segmentation method. To exemplar segmentations for testing can be found in the folder `./resource`.

### Registering cerebral vessels

Our registration method &#952;<sub>R</sub> is implemented in /source and can be used as a commandline tool by executing 
[main.py](source%2Fmain.py). Make sure to run ```pip install -r requirements.txt``` within the `/source` folder to install the dependencies within your python environment.

The commandline tool can be executed with test data: ```python -m source.main --fixed ./resource/ixi002-pd.seg.nrrd --moving ./resource/ixi002-tof.seg.nrrd --output result.tfm --warped warped.seg.nrrd --truth ./resource/ixi002-truth.tfm --show```. Parameters:
* `--fixed`: segmentation of vessels in the fixed image (I<sub>float</sub>)
* `--moving`: segmentation of vessels in the moving image (I<sub>ref</sub>)
* `--output`: output path for the resulting transform, must have an extension supported by SimpleITK, e.g., `.tfm` or `.hdf`. (T<sub>R</sub>)
* `--truth`: (optional) truth transform to evaluate against, must have an extension supported by SimpleITK, e.g., `.tfm` or `.hdf`
* `--warped`: (optional) warped image to write, must have an extension supported by SimpleITK, e.g., `.tnrrd`
* `--show`: (optional) whether to visualize the registered point-clouds using Open3D.
* `--binary`: (optional) whether to mask any foreground label instead of extracting the left and right labels predicted by model &#952;<sub>M</sub>

After registration, our method will output the translation and rotation errors if --truth was specified.
Our ground-truth transform for IXI and TubeTK are shared via our [Google Drive](https://drive.google.com/open?id=1QKeT1asXAswLx67GKCcpGCGba-hXU1Vv&usp=drive_fs). For each image pair, there is a `*.zip` file mapping the sMRI to the TOF, e.g., for `IXI002-Guys-0828` there is a file `IXI002-Guys-0828_PD.zip` mapping the TOF to the PD sequence. Note: the contained forward.hdf needs to be inverted to yield the ground-truth transform.

When using --show, the moving vessels of I<sub>float</sub> will be shown in red, the transformed moving vessels in green and the fixed vessels of I<sub>ref</sub> in blue.

## References

Our paper will be published in the 2024 Conference [proceedings](https://link.springer.com/conference/miua) of the Medical Image Understanding and Analysis (MIUA) through Springer Nature.

If you use our results in your research, we would appreciate you citing the following conference paper:

* `Sabrowsky-Hirsch, B., Alshenoudy, A., Scharinger, J., Gmeiner, M., Thumfart, S., Giretzlehner, M.. (2024). Robust Multi-Modal Registration of Cerebral Vasculature. 28th UK Conference on Medical Image Understanding
and Analysis (MIUA 2024). Springer Nature.`

## Acknowledgements

<div style="background-color:white;padding: 1em">
<img src="../assets/risc.svg" height="50px"  />
<img src="../assets/grants.svg" height="50px"  />
</div>

This project is financed by research subsidies granted by the government of Upper Austria. RISC Software GmbH is Member of UAR (Upper Austrian Research) Innovation Network.
