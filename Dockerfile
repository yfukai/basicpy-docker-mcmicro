FROM nvidia/cuda:11.5.2-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN sed -i.bak -e 's%http://[^ ]\+%mirror://mirrors.ubuntu.com/mirrors.txt%g' /etc/apt/sources.list
RUN apt-get update \
      && apt-get install -y tzdata\
      && apt-get install -y libffi-dev gcc git curl python3-pip default-jdk\
      && rm -rf /var/lib/apt/lists/*
RUN pip --no-cache-dir install --upgrade pip \
    && pip --no-cache-dir install "jax[cuda11_cudnn82]==0.3.22" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html \
    && pip --no-cache-dir install basicpy aicsimageio[bfio] bfio[bioformats] scikit-image
COPY ./main.py /opt/
