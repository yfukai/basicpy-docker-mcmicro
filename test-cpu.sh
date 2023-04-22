docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:0.2.1 -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:latest -d=cpu -i /data/exemplar-001-cycle-06.ome.tiff -o /data/
