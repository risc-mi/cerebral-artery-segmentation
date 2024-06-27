# Brain Artery Segmentation for Structural MRI

![midl2024-results.svg](..%2Fassets%2Fmidl2024-results.svg)
_Results of our segmentation method for different structural MRI sequences: 
The predictions are illustrated with DSC scores for the full (top) and CoW region (bottom) of an exemplar patient of 
IXI (TOF, PD, T1 and T2) and TubeTK (FL and MPR). Oversegmentation is shown in magenta and undersegmented ground-truth in light-blue._

## About

In this project, we share code and results on our proposed method for the segmentation of brain arteries in structural MR images (sMRI).
The delineation of brain arteries in sMRI poses a significant challenge due to the lack of contrast, which we address through our automatic segmentation method.

Our fully automated strategy leverages two modules:
- Segmentation module: generates pseudo labels from angiographic TOF MR images using model **M<sub>A</sub>** published in [MIUA2024a](..%2Fmiua2024a%2FREADME.md).
- Registration module: pairs these labels with sMRI images using model **M<sub>B</sub>** and a geometric registration method published in [MIUA2024b](..%2Fmiua2024b%2FREADME.md).

The process constructs the dataset used to train the final improved segmentation model **M<sub>C</sub>**. 
In our experiments conducted on data of [IXI](https://brain-development.org/ixi-dataset/) and [TubeTK](https://public.kitware.com/Wiki/TubeTK/Data), our model achieved an average Dice Similarity Coefficient (DSC) of 0.66 across all 
sMRI around the central Circle of Willis structure in a 5-fold cross validation. Out of sMRI sequences which we identified  **PD** with a DSC of 0.7 as the best alternative 
to angiographic images. Please refer to our [publication](#References) if you are interested in the details.

![method.svg](../assets/midl2024-method.svg)

## How to use


Our work fully relies on the nnU-Net framework for training and inference. You can
checkout their [Github](https://github.com/MIC-DKFZ/nnUNet) repository or install the package from [PyPI](https://pypi.org/project/nnunetv2/):
```pip install nnunetv2```. However, be careful to set up Pytorch correctly for your system before installing nnU-Net. 
For more information, check the [nnU-Net Instructions](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md).

### Inference

We provide pretrained weights for model **M<sub>C</sub>** at [Google Drive](https://drive.google.com/drive/folders/10r7tYcAYhvw3ZpFkX6d65oo9U3GK7mpy?usp=sharing).
You can use our models with the nnU-Net framework to generate predictions for your data:

1. First download and extract the models to a folder `<path-to/models>`.
2. Store the images (we recommend using the .nii.gz format) at a folder `<path-to/input>`.\
The filenames should follow the format `<name>_0000.nii.gz`, e.g. 'pat01pd_0000'.\
**Note**: The postfix `_0000` is used by nnU-Net to identify channels and should always be present.
3. Create your output folder `<path-to/output>`.
4. Activate your python environment. Make sure nnU-Net is set up accordingly.
5. In the environment prompt, run ```nnUNetv2_predict_from_modelfolder -m "<path-to/models>" -i "<path-to/input>" -o "<path-to/output>"```

**Note**: It is worth checking the image orientation (as in the cosine orientation matrix), as it is sometimes incorrectly interpreted by nnU-Net. 
The models are not orientation-agnostic and will produce inferior results if the orientation of the input does not match the standard patient orientation. We found preprocessing the images with SimpleITK.DICOMOrient, using 'RAI' as the reference orientation to convert to, to be sufficient.

## References

Our paper is available through [OpenReview](https://openreview.net/forum?id=KXmiNZYuBR). We also share the [poster](poster.pdf) presented at the MIDL 2024 conference in Paris.

If you use our results in your research, we would appreciate you citing the following conference paper:

* `Sabrowsky-Hirsch, B., AlShenoudy, A., Thumfart, S., Giretzlehner, M., & Scharinger, J. (2024). Brain Artery Segmentation for Structural MRI. In Medical Imaging with Deep Learning. OpenReview`

## Acknowledgements

<div style="background-color:white;padding: 1em">
<img src="../assets/risc.svg" height="50px"  />
<img src="../assets/grants.svg" height="50px"  />
</div>

This project is financed by research subsidies granted by the government of Upper Austria. RISC Software GmbH is Member of UAR (Upper Austrian Research) Innovation Network.
