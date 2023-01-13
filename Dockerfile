FROM nvidia/cuda:11.5.2-cudnn8-devel-ubuntu20.04

RUN apt-get update \
      && apt-get install -y libffi-dev gcc git curl python3-pip default-jdk\
      && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN pip --no-cache-dir install --upgrade pip \
    && pip --no-cache-dir install "jax[cuda11_cudnn82]==0.3.22" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html \
    && python3 -c "import jax; print(jax.devices())" \
    && pip --no-cache-dir install basicpy aicsimageio[bfio] scikit-image
COPY ./main.py /opt/
