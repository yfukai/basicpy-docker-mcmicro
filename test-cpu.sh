version="0.2.1"

docker pull yfukai/basicpy-docker-mcmicro:${version}
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:${version} -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull yfukai/basicpy-docker-mcmicro:latest
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:latest -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
