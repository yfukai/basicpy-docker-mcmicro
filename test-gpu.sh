version="0.3.3"

docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:${version}-cuda
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:${version}-cuda /opt/main.py -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:latest-cuda
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest-cuda /opt/main.py -d=gpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
