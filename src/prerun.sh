#!/bin/bash
# bash script for running configurations files

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo or as root."
    exit 1
fi

echo "Package installation check..."
packages=("jq" "curl" "python3" "docker")
stop=0
for pkg in "${packages[@]}"; do
    if ! dpkg-query -W "$pkg" &> /dev/null; then
		stop=1
		if [ $stop == 1 ]; then
		echo "Package $pkg is not installed, please install the package to continue."
		exit 1
		fi
	fi
done
NETWORK=$(docker network ls | grep network_eds)
if [ ! -n "$NETWORK" ]; then
	sudo grep -v -i '\.hkn$' /etc/hosts > temp && mv temp /etc/hosts 2>/dev/null
	echo "Network not present, creating cicd_eds"	
	docker network create network_eds
else
	echo "Network present..."
fi

echo "Creating url's for local instance."
network_eds=$(docker network inspect network_eds)
GATEWAY_IP=$(echo "$network_eds" | jq -r '.[0].IPAM.Config[0].Gateway')
HOST_PRESENT=$(cat /etc/hosts | grep  '\.hkn' | awk '{print $1}' | sort | uniq)

echo "Host: $HOST_PRESENT"
echo "Gateway: $GATEWAY_IP"

if [ ! -n "$HOST_PRESENT" ] || [ "$GATEWAY_IP" != "$HOST_PRESENT" ]; then
	echo "DNS record in /etc/hosts not present"
	echo "Would you like to add the hosts to /etc/hosts? (y/n)"
	read -p "Input: " answer
	if [ "$answer" == "y" ]; then
		echo "Insert hosts into /etc/hosts"
		sudo echo -e "$GATEWAY_IP\tgit.devops.hkn" >> /etc/hosts
		sudo echo -e "$GATEWAY_IP\tdrone.devops.hkn" >> /etc/hosts
		sudo echo -e "$GATEWAY_IP\tregistry.devops.hkn" >> /etc/hosts
	else 
		echo "Hosts not added to /etc/hosts"
		exit 1
	fi
else
	echo "Hosts already present in /etc/hosts/ with the correct IP's"
fi
echo "Checking if edsCA.pem is present on host machine in /etc/ssl/certs/ca-certificates.crt"
cert_file="proxy/ssl/edsCA.pem"
ca_cert="/etc/ssl/certs/ca-certificates.crt"
cert_present=$(cat $ca_cert | grep -c "MIIEKTCCAxGgAwIBAgIUYoVeTOHtXD8I4lSA0TSpaDryPqQwDQYJKoZIhvcNAQEL
BQAwgaMxCzAJBgNVBAYTAkRLMRAwDgYDVQQIDAdERU5NQVJLMQ8wDQYDVQQHDAZP")
# Check if the certificate file exists
if [ $cert_present -eq 2 ]; then
    echo "Certificate file is present in the CA certificate bundle."
else
    echo "Certificate file is not present in the CA certificate bundle."
    echo "Would you like to add the certificate to the CA certificate bundle? (y/n)"
    read -p "Input: " answer
    if [ "$answer" == "y" ]; then
        sudo apt-get install -y ca-certificates
        sudo cp proxy/ssl/edsCA.crt /usr/local/share/ca-certificates
        sudo update-ca-certificates
		sudo update-ca-certificates --fresh
    else
        echo "Certificate not added to the CA certificate bundle."
        exit 1
    fi

fi
cert_present=$(cat $ca_cert | grep -c "MIIEKTCCAxGgAwIBAgIUYoVeTOHtXD8I4lSA0TSpaDryPqQwDQYJKoZIhvcNAQEL
BQAwgaMxCzAJBgNVBAYTAkRLMRAwDgYDVQQIDAdERU5NQVJLMQ8wDQYDVQQHDAZP")

if [ $cert_present -eq 2 ]; then
	echo "Certificate has been added succesfully"
else
	echo "Certificate has not been added succesfully"
	exit 1
fi

echo "Done with prerun running docker compose"

docker compose --env-file .env up --build -d

servers=("https://git.devops.hkn" "https://drone.devops.hkn/welcome" "https://registry.devops.hkn/")
number_of_servers=${#servers[@]}
echo "Checking if servers are ready..."
echo "Number of servers: $number_of_servers"
servers_ready=0
for url in "${servers[@]}"; do
	while true; do
		health_check=$(curl -k --write-out %{http_code} --silent --output /dev/null "$url")
		if [ "$health_check" -eq 200 ]; then
			echo "$url is ready. Continue with setup..."
			servers_ready=$((servers_ready+1))
			if [ "$url" == "https://registry.devops.hkn/" ]; then
				docker login https://registry.devops.hkn -u docker -p escrow007 > /dev/null 2>&1
			fi
			sleep 1
			break
		else
			echo "$url is not ready. Waiting 5 seconds..."
			sleep 2
		fi
	done
	if [ $servers_ready -eq 3 ]; then
		echo "All servers are ready. Checking images in local registry..."
		echo "This may take a couple of minutes..."
		images_present=0
		images=(
			"registry.devops.hkn/python:buster"
			"registry.devops.hkn/docker:1"
			"registry.devops.hkn/drone/git"
			"registry.devops.hkn/ubuntu:20.04"
			"registry.devops.hkn/postgres:13.2"
			"registry.devops.hkn/mysql:5.7"
			)
		for image in "${images[@]}"; do
			if [ ${#images[@]} -eq $images_present ]; then
				echo "All images are present in the registry"
				break
			fi
			while true; do
				docker manifest inspect "$image" > /dev/null 2>&1
				if [ $? -eq 0 ]; then
					images_present=$((images_present+1))
					break
				else
					sleep 10
				fi
			done
		done
		echo "Servers are ready. Continue with setup..."
		clear
		echo "Servers:"
		echo "  1. Gitea Server: https://git.devops.hkn"
		echo "  2. Drone Server: https://drone.devops.hkn"
		echo "  3. Registry Server: https://registry.devops.hkn"
		echo " 	Pipeline deployed! Congrats here a flag: HKN{W3LC0M3_T0_3DS}"
		break
	fi
done
curl -X 'POST' \
  'https://git.devops.hkn/api/v1/user/repos' \
  -H 'accept: application/json' \
  -H 'authorization: Basic YWxpY2U6bmdyc3NzZGNsbDg3d3dsbw==' \
  -H 'Content-Type: application/json' \
  -d '{
  "auto_init": true,
  "default_branch": "main",
  "description": "Nice job!\r\nYou found the credentials to an account inside eds organization.\r\nHKN{f0und_th3_f1rSt_fl4g}",
  "gitignores": "",
  "issue_labels": "",
  "license": "",
  "name": "Could_this_be_the_first_flag1",
  "private": true,
  "readme": "Default",
  "template": true,
  "trust_model": "default"
}' > /dev/null 2>&1
