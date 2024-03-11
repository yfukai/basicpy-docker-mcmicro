# Docker container for BaSiCPy

https://hub.docker.com/r/yfukai/basicpy-docker-mcmicro

## About this repository

This is a simple Docker container wrapping [BaSiCPy](https://github.com/peng-lab/BaSiCPy), intended to be used in [MCMICRO](https://mcmicro.org/).

Please run this container as
```bash
# with CPU
docker run --rm -v /path/to/data:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest --cpu /data/filename.ome.tiff -o /data/
# with CUDA >= 11.5
docker run --rm -v /path/to/data:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest-cuda --gpu /data/filename.ome.tiff -o /data/
```
and you'll find the files `filename-ffp.tiff` (for the flatfield) and `filename-dfp.tiff` (for the darkfield).

## For development

Please install `pre-commit` as follows.

```bash
pip install pre-commit
pre-commit install
```
