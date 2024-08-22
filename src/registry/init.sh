#!/bin/bash
set -m
./entrypoint.sh /etc/docker/registry/config.yml &
while true
do
    health=$(curl -k --write-out %{http_code} --silent --output /dev/null https://$REGISTRY_HTTPS_ADDR)
    if [ "$health" -eq 200 ]; then
        echo "Registry is ready. Continue with setup..."
        break
    else 
        echo "Registry is not ready. Waiting 5 seconds..."
        sleep 5
    fi
done

# Define the tar archive and the output directory for extracted images
tar_archive="/tmp/docker_images.tar.gz"
output_dir="/tmp/docker_images_extracted"

# Create the directory if it doesn't exist
mkdir -p $output_dir

# Extract the tar archive
tar -xzvf $tar_archive -C $output_dir

# Loop through the extracted tar files and load them into Docker
for image_tar in $output_dir/*.tar; do
  # Load the image from the tar file
  docker load -i $image_tar
  
  # Optionally, extract the image name from the tar file name
  image_name=$(basename $image_tar .tar)
done

images=(
  "python:buster"
  "docker:latest"
  "ubuntu:20.04"
  "drone/git"
  "mysql:5.7"
  "postgres:13.2"
)

for image in "${images[@]}"; do
    echo $image
    if [  "$image" == "docker:latest"  ]; then
      docker tag docker:latest registry.devops.hkn/docker:1
      docker push registry.devops.hkn/docker:1
    else 
      x=$(echo "registry.devops.hkn/$image")
      docker tag $image $x > /dev/null 2>&1
      docker push $x > /dev/null 2>&1
    fi
done


echo "All images have been loaded and pushed to the registry."


fg # Bring the registry process back to the foreground
