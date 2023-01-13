# Docker container for BaSiCPy

## About this repository

This is a simple Docker container wrapping [BaSiCPy](https://github.com/peng-lab/BaSiCPy), intended to be used in [MCMICRO](https://mcmicro.org/).

Please run this container as
```bash
docker run -it --rm -v /path/to/data:/data @@@ python3 /opt/basicpy /data/filename.ome.tiff /data
```
and you'll find the files `filename-ffp.tiff` (for the flatfield) and `filename-dfp.tiff` (for the darkfield).

## For development

Please install `pre-commit` as follows.

```bash
pip install pre-commit
pre-commit install
```
