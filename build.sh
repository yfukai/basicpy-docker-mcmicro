VERSION=0.1.2
docker buildx build \
    --push \
    --platform linux/amd64,linux/arm64/v8 \
    -t yfukai/basicpy-docker-mcmicro:$VERSION \
    -t yfukai/basicpy-docker-mcmicro:latest \
    "."

docker buildx build \
    --push \
    --platform linux/amd64 \
    --build-arg BASE_IMAGE="nvidia/cuda:11.5.2-cudnn8-devel-ubuntu20.04" \
    --build-arg JAX_VERSION_EXTRA="cuda11_cudnn82" \
    -t yfukai/basicpy-docker-mcmicro:$VERSION-cuda \
    -t yfukai/basicpy-docker-mcmicro:latest-cuda \
    "."

docker push yfukai/basicpy-docker-mcmicro --all-tags