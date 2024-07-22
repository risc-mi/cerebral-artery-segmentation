# Towards Segmenting Cerebral Arteries from Structural MRI
<img src="title_figure.png" alt="cerebral arteries predicted for structural scans" height="300">

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

### Trained Models
You can download our TOF-MRA model from [here](https://drive.google.com/file/d/1DYSbiD0wlUb8q0BLDtZK094yIl34Xi3K/view?usp=sharing)
and use it to predict pseudo-labels for IXI/TubeTK or possibly a different dataset. On the other hand, you can download 
our structural MRI model from [here](https://drive.google.com/file/d/1uydOFTlT5S5-E427prpNt4mlx5y0IEjb/view?usp=sharing).


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
