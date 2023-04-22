docker run --rm -v $(pwd)/testdata:/data --gpus=all yfukai/basicpy-docker-mcmicro:0.2.1-cuda -d gpu /data/exemplar-001-cycle-06.ome.tiff /data/
docker run --rm -v $(pwd)/testdata:/data --gpus=all yfukai/basicpy-docker-mcmicro:latest-cuda -d gpu /data/exemplar-001-cycle-06.ome.tiff /data/
