version="0.3.5"

docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:${version}
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:${version} /opt/main.py -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker pull ghcr.io/yfukai/basicpy-docker-mcmicro:latest
docker run --rm -v $(pwd)/testdata:/data ghcr.io/yfukai/basicpy-docker-mcmicro:latest /opt/main.py -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
