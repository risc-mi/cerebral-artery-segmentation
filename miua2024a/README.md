# Towards Segmenting Cerebral Arteries from Structural MRI
<img src="figures/title_figure.png" alt="cerebral arteries predicted for structural scans" height="300">

## About

In this project, we share our models and code for our proposed method to segment cerebral arteries from structural MRI.
The assessment of cerebral arteries and the Circle of Willis structure is crucial for diagnosing various cerebrovascular
pathologies.
While angiographic sequences such as time-of-flight magnetic resonance angiography (TOF-MRA) are indispensable
tools for the assessment of cerebral arteries, extending segmentation methods to include structural MRI holds significant clinical promise.

To address this, we propose a three-step method, in which the core idea behind it is to train a segmentation model on 
structural scans in a supervised setting.
To achieve this, we map structural scans to their corresponding TOF-MRA scan
and use labels either generated or directly annotated from TOF-MRA with structural scans for training.
This can be summarized below:
1. Generate pseudo-labels for TOF-MRA
2. Intra-patient registration from structural space to TOF-MRA space
3. Training of structural MRIs with pseudo-labels in a supervised setting

![method.svg](figures/method.svg)
_Overview of our proposed three-step method._

## How to use

Our work fully relies on the nnU-Net framework for training and inference. 
You can check out their [GitHub](https://github.com/MIC-DKFZ/nnUNet) repository or install the package from [PyPI](https://pypi.org/project/nnunetv2/):
```pip install nnunetv2```. However, be careful to set up Pytorch correctly for your system before installing nnU-Net. 
For more information, check the [nnU-Net Instructions](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md).

For registration, we use both the ANTsPy and the NiftiReg frameworks. For `ANTsPy` you can check out their 
[GitHub](https://github.com/ANTsX/ANTsPy) repository
or install the package from [PyPI](https://pypi.org/project/antspyx/): ```pip install antspyx```.
For NiftyReg you can check out their [GitHub](https://github.com/KCL-BMEIS/niftyreg) for instructions and how to use.

All of our models are trained in a 5-fold cross-validation setting,
in which they are trained on a combined database of IXI and TubeTK subjects.
### Registration
We perform intra-patient registration to map structural MRI to the space of TOF-MRA.
First, we employ ANTsPy to perform a `DenseRigid` transformation that is followed by an affine transformation step based 
on the Block matching algorithm for global registration implemented in NiftyReg.
We found that this yields better results on IXI and TubeTK data than the `Affine` setting in ANTsPy.
Refer to `registration.py` on how to use each step on a sample input.

### Trained Models
We provide pretrained weights for models **M<sub>A</sub>** and **M<sub>S</sub>** at [Google Drive](https://drive.google.com/drive/folders/1BnIQ0HtvWwciwVwIAMXPkUBqjow9hQdn?usp=sharing).
You can use our models with the nnU-Net framework to generate predictions for your data:

1. First download and extract the models to a folder `<path-to/models>`.
2. Store the images (we recommend using the .nii.gz format) at a folder `<path-to/input>`.\
The filenames should follow the format `<name>_0000.nii.gz`, e.g. 'pat01pd_0000'.\
**Note**: The postfix `_0000` is used by nnU-Net to identify channels and should always be present.
3. Create your output folder `<path-to/output>`.
4. Activate your python environment. Make sure nnU-Net is set up accordingly.
5. In the environment prompt, run ```nnUNetv2_predict_from_modelfolder -m "<path-to/models>" -i "<path-to/input>" -o "<path-to/output>"```

**Note**: It is worth checking the image orientation (as in the cosine orientation matrix), as it is sometimes 
incorrectly interpreted by nnU-Net. The models are not orientation-agnostic and will produce inferior results if the 
orientation of the input does not match the standard patient orientation. We found preprocessing the images with 
`SimpleITK.DICOMOrient()`, using 'RAI' as the reference orientation to convert to, to be sufficient.



## References

Our paper will be published in the 2024 Conference [proceedings](https://link.springer.com/conference/miua) of the Medical Image Understanding and Analysis (MIUA) through Springer Nature.

If you use our results in your research, we would appreciate you citing the following conference paper:

* `Alshenoudy, A., Sabrowsky-Hirsch, B., Scharinger, J., Thumfart, S., Giretzlehner, M.. (2024). Towards Segmenting Cerebral Arteries from Structural MRI. 28th UK Conference on Medical Image Understanding
and Analysis (MIUA 2024). Springer Nature.`

## Acknowledgements

<div style="background-color:white;padding: 1em">
<img src="../assets/risc.svg" height="50px"  />
<img src="../assets/grants.svg" height="50px"  />
</div>

This project is financed by research subsidies granted by the government of Upper Austria. RISC Software GmbH is Member of UAR (Upper Austrian Research) Innovation Network.
