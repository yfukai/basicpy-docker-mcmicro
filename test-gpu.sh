version="0.3.1"

docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:${version}-cuda
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:${version}-cuda -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:latest-cuda
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
