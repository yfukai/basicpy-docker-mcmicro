version="0.2.1"

docker pull yfukai/basicpy-docker-mcmicro:${version}-cuda
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:${version}-cuda -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull yfukai/basicpy-docker-mcmicro:latest-cuda
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:latest-cuda -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
