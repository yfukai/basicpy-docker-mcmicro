version="pr-13"

docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:${version}
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:${version} -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:latest
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
