# registration-magi
Automated registration of nii images using fsl based on the [vistalab neurodebian:trusty docker image](https://github.com/vistalab/docker/tree/master/fsl/fsl-v5.0).

## Pre-reqs
Ensure that [docker engine](https://docs.docker.com/engine/installation/) is properly installed. Follow installation instructions on their website.

## Building/Pulling the image
You can either build the image by running the following commands:
`docker build --no-cache --tag registration-magi`

Or you can pull the image by running
`docker pull ouwen/registration-magi`

## Usage Examples

### Single use case:

General format to use fsl commands.
```
docker run --rm -it \
    -v </path/to/input/data>:/input \
    -v </path/to/output>:/output \
    vistalab/fsl-v5.0 <command>
```

Using sample images to align a post-contrast MRI with a pre-contrast MRI as the reference point.
```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    vistalab/fsl-v5.0 flirt \
    -in /input/TCGA_GBM_06_0133_post.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_post_r
```

Using sample images to align a FLAIR MRI with a pre-contrast MRI as the reference point.
```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    vistalab/fsl-v5.0 flirt \
    -in /input/TCGA_GBM_06_0133_flair.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_flair_r
```
To change output type simple add the environmental variable `FSLOUTPUTTYPE` default is `NIFTI_GZ`.
Options are: `NIFTI_GZ`, `NIFTI`, `NIFTI_PAIR`, `NIFTI_PAIR_GZ`, `ANALYZE`, `ANALYZETM`, `ANALYZE_GZ`
```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    -e FSLOUTPUTTYPE=NIFTI \
    vistalab/fsl-v5.0 flirt \
    -in /input/TCGA_GBM_06_0133_post.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_post_r
```
