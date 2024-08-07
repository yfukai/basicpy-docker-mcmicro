ARG MINIFORGE_NAME="Miniforge3"
ARG MINIFORGE_VERSION="22.9.0-3"
ARG BASE_IMAGE="ubuntu:20.04"
ARG JAX_VERSION_EXTRA="cpu"
ARG JAX_VERSION="0.4.23"

FROM ${BASE_IMAGE}
#https://stackoverflow.com/questions/44438637/arg-substitution-in-run-command-not-working-for-dockerfile
ARG MINIFORGE_NAME
ARG MINIFORGE_VERSION
ARG BASE_IMAGE
ARG JAX_VERSION
ARG JAX_VERSION_EXTRA

ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Installing necessary packages

RUN apt-get update \
      && apt-get install -y ca-certificates \
      && apt-get install -y tzdata \
      && apt-get install --no-install-recommends -y wget bzip2 git tini g++ \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# Installing Miniforge
# modified from https://hub.docker.com/layers/condaforge/miniforge3/latest/images/sha256-1a4710bbb61c9de8b9293c3f9cbc1223bb8ede21e74942a71a6c1c7d5eb54b2e?context=explore
RUN wget --no-hsts --quiet https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${MINIFORGE_NAME}-${MINIFORGE_VERSION}-Linux-$(uname -m).sh -O /tmp/miniforge.sh \
    && /bin/bash /tmp/miniforge.sh -b -p ${CONDA_DIR} \
    && rm /tmp/miniforge.sh \
    && conda clean --tarballs --index-cache --packages --yes \
    && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
    && conda clean --force-pkgs-dirs --all --yes  \
    && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
    && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc # buildkit

# Installing or building Jax
RUN conda install -c conda-forge mamba \
    && mamba install -c conda-forge aicsimageio pip numpy wheel scikit-image maven openjdk=11.0.1\
    && pip --no-cache-dir install bfio[bioformats]

RUN pip --no-cache-dir install "jax[${JAX_VERSION_EXTRA}]==${JAX_VERSION}" jaxlib || \
    pip --no-cache-dir install "jax[${JAX_VERSION_EXTRA}]==${JAX_VERSION}" jaxlib -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html || \
    ( git clone https://github.com/google/jax \
    && cd jax \
    && git checkout jaxlib-v${JAX_VERSION}\
    && python build/build.py \
    && pip install dist/*.whl \
    && cd .. \
    && rm -rf jax )
