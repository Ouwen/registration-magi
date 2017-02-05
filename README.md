# registration-magi
Automated registration of nii images using fsl based on the [vistalab neurodebian:trusty docker image](https://github.com/vistalab/docker/tree/master/fsl/fsl-v5.0).

## Pre-reqs
Ensure that [docker engine](https://docs.docker.com/engine/installation/) is properly installed. Follow installation instructions on their website.

## Get the image
To use the image, simply pull it from docker hub using the following command. You can also opt to build the image from the provided dockerfile.
```
docker pull ouwen/registration-magi
```

## Usage Examples

### Command Line Usage:

General format to use fsl commands.
```
docker run --rm -it \
    -v </path/to/input/data>:/input \
    -v </path/to/output>:/output \
    ouwen/registration-magi <command>
```

Using sample images to align a post-contrast MRI with a pre-contrast MRI as the reference point.
`$PWD` prints the path of the current working directory. Docker -v must take absolute paths.

```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    ouwen/registration-magi flirt \
    -in /input/TCGA_GBM_06_0133_post.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_post_r
```

Using sample images to align a FLAIR MRI with a pre-contrast MRI as the reference point.
```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    ouwen/registration-magi flirt \
    -in /input/TCGA_GBM_06_0133_flair.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_flair_r
```

### Changing the default output:

To change output type simple add the environmental variable `FSLOUTPUTTYPE` default is `NIFTI_GZ`.
Options are: `NIFTI_GZ`, `NIFTI`, `NIFTI_PAIR`, `NIFTI_PAIR_GZ`, `ANALYZE`, `ANALYZETM`, `ANALYZE_GZ`
```
docker run --rm -it \
    -v $PWD/sample_data/input:/input \
    -v $PWD/sample_data/output:/output \
    -e FSLOUTPUTTYPE=NIFTI \
    ouwen/registration-magi flirt \
    -in /input/TCGA_GBM_06_0133_post.nii \
    -ref /input/TCGA_GBM_06_0133_pre.nii \
    -out /output/TCGA_GBM_06_0133_post_r
```

### Generate a batch file from csv.
Magi can generate a batch file of docker commands if you have a csv with the following format.

| pre-contrast filepath                       | post-contrast filepath                       | FLAIR filepath                                | output filepath     | output base filename   |
|---------------------------------------------|----------------------------------------------|-----------------------------------------------|---------------------| -----------------------|
| /sample_data/input/TCGA_GBM_06_0133_pre.nii | /sample_data/input/TCGA_GBM_06_0133_post.nii | /sample_data/input/TCGA_GBM_06_0133_flair.nii | /sample_data/output | TCGA_GBM_06_0133       |
| ...                                         | ...                                          | ...                                           | ...                 | ...                    |


The batch file created will register MRIs to the MRI with the least number of slices.
In the case of a tie, the order of precedence is: pre-contrast, post-contrast, FLAIR.

Run the following command to generate a batch script in `<output_location>`
```
docker run -rm -it \
    -v <input_location>:/input
    -v <output_location>:/output \
    ouwen/registration-magi
    python batch_generator /input/imagelist.csv
```

## Build image from source (optional)
You can either build the image by running the following commands:
```
docker build --no-cache --tag registration-magi`
```

## License MIT

Copyright (c) 2016 Ouwen Huang, contributors

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
