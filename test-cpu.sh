docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:0.2.1 -d cpu /data/exemplar-001-cycle-06.ome.tiff /data/
docker run --rm -v $(pwd)/testdata:/data yfukai/basicpy-docker-mcmicro:latest -d cpu /data/exemplar-001-cycle-06.ome.tiff /data/
