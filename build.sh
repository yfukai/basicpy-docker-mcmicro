VERSION=0.2.1
docker buildx build \
    --push \
    --build-arg BASE_IMAGE="yfukai/conda-jax:latest" \
    --platform linux/amd64,linux/arm64/v8 \
    -t yfukai/basicpy-docker-mcmicro:$VERSION \
    -t yfukai/basicpy-docker-mcmicro:latest \
    "."

docker buildx build \
    --push \
    --platform linux/amd64 \
    --build-arg BASE_IMAGE="yfukai/conda-jax:latest-cuda" \
    -t yfukai/basicpy-docker-mcmicro:$VERSION-cuda \
    -t yfukai/basicpy-docker-mcmicro:latest-cuda \
    "."

docker push yfukai/basicpy-docker-mcmicro --all-tags
