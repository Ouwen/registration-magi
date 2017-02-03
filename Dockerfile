FROM neurodebian:trusty

# Run apt-get calls
COPY sources /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-get update \
    && apt-get install -y fsl-5.0-core

# Configure environment
ENV FSLDIR=/usr/lib/fsl/5.0
ENV FSLOUTPUTTYPE=NIFTI_GZ
ENV PATH=$PATH:$FSLDIR
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$FSLDIR

# Install utils
RUN apt-get install -y python-pip python-numpy python-scipy libboost-python-dev build-essential
RUN pip install nibabel pydicom medpy

# Run configuration script for normal usage
RUN echo ". /etc/fsl/5.0/fsl.sh" >> /root/.bashrc
