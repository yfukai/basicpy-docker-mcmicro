docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:0.2.1-cuda -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:latest-cuda -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
