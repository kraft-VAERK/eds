#!/bin/bash

# The comment will always refer to the line below the comment.
# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo or as root."
    exit 1
fi

# Specify the username and password
# Check if the script is called with exactly two arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <Usrename> <Password>"
    exit 1
fi

# Assign the arguments to variables
username="$1"
password="$2"
regex="^.*[[:alnum:]].{5,}$"

if [[ ! $password =~ $regex ]]; then
  echo "Password must contain 6 characters or more."
fi
check_user=$(curl -s -o /dev/null -w "%{http_code}" -X 'GET' \
  https://full-enormous-crow.ngrok-free.app/api/v1/users/$username)
if [ $check_user -eq 200 ]; then
  echo "User already exists"
  exit 1
fi

printf "Starting the Script \n \n"
# Start virtual environment
apt install python3.10-venv -qqy > /dev/null 2>&1
python3 -m venv venv
source venv/bin/activate

# Update the System, so curl and jq can be installed.
apt update -qq > /dev/null 2>&1

printf "## 20%% complete.\r"
# Full-upgrade is used to upgrade the system, but it also removes packages if needed.
apt full-upgrade -qqy > /dev/null 2>&1

# Install curl and jq
apt install -qqy curl jq > /dev/null 2>&1

# Install python3, pip3 and requirements for the multiple python calls in the script.
apt install -qqy python3 > /dev/null 2>&1
apt install -qqy python3-pip > /dev/null 2>&1
pip3 install -r requirements.txt > /dev/null 2>&1
printf "### 30%% complete.\r"

# Assign the arguments to variables
length=10

# Specify the length of the random text
random_text=$(openssl rand -base64 $((length * 3 / 4)) | head -c $length)

# In order to push repositories to the Git server, they need to include a .git folder containing repository information. 
# As they're part of a larger Git repository for the project, these repositories are initially stored as 'notgit'.
# During runtime, they undergo changes and revert back to their original state once the script completes execution.
cd ../../
python3 rename.py git
cd -
printf "#### 40%% complete.\r"

# To establish a new user on the Gitea server, the action triggers the dronecasc module, which initiates the user creation process within the Gitea server. 
# The configuration of repositories linked directly to the drone server is managed through the drone.yaml file.
response_users=$(python3 -m dronecasc drone.yaml -u $username -p $password)
if [ $response_users -ne 0 ]; then
    echo "Error creating user. Exiting."
    cd ../../
    python3 rename.py notgit
    rm -rf src/drone/venv
    exit 1
fi
printf "##### 50%% complete.\r"
# Make a post request to the remote Gitea server, that make Oauth for the created user.
# See the Empowering_DevOps_Security/src/requests/request.py file for more information.
response_oauth=$(python3 ../requests/request.py $username $password)
if [ "$response_oauth" == "Error" ]; then
    echo "Failure to create Oauth. Exiting."
    cd ../../
    python3 rename.py notgit
    rm -rf src/drone/venv
    exit 1
fi
# Retrieve the client_id and client_secret from the response, which is a JSON object. 
# Prior to parsing it with jq, the single quotes must be replaced with double quotes. 
# These credentials are essential for authenticating the local instance of Drone with the Gitea server, which is facilitated by Gitea's internal OAuth server.
client_id=$(echo "$response_oauth" | sed "s/'/\"/g" | jq -r .client_id)
client_secret=$(echo "$response_oauth" | sed "s/'/\"/g" | jq -r .client_secret)
if [ -z "$client_id" -o -z "$client_secret" ]; then
    echo "Failure to create Oauth. Exiting."
    cd ../../
    python3 rename.py notgit
    rm -rf src/drone/venv
    exit 1
fi
printf "###### 60%% complete.\r"

# To enable communication among containers, a network is established. 
# If the network doesn't exist, it's created. If it already exists, a message is printed to the console.
# The network is named 'drone-network'.
if [ -n "$(docker network ls -q -f name=drone-network)" ]; then
    echo "Drone Network already exists."
else
    echo "Creating drone-network"
    sudo docker network create drone-network
fi
printf "####### 70%% complete.\r"

org_name=$(awk '/orgs:/ {getline; gsub(/^[[:space:]]+|[[:space:]]+$/, ""); sub(/:$/, ""); print}' drone.yaml)
# This command creates a new container named 'drone-server' and runs the kraftvaerket/kv-drone:latest image.
# The drone server and its settings will not be explained here.
sudo docker run --name drone-server \
    -e DRONE_GITEA_CLIENT_ID=$client_id \
    -e DRONE_GITEA_CLIENT_SECRET=$client_secret \
    -e DRONE_RPC_SECRET=$random_text \
    -e DRONE_SERVER_HOST=localhost:8080 \
    -e DRONE_SERVER=http://localhost:8080 \
    -e DRONE_USER_CREATE=username:morten_jakobsen,admin:true \
    -e DRONE_REPOSITORY_FILTER=$org_name \
    -e DRONE_WEBHOOK_SKIP_VERIFY=true \
    -e DRONE_REPO_BRANCH=* \
    --network=drone-network \
    --publish=8080:80 \
    --detach \
    kraftvaerket/kv-drone:latest
printf "######## 80%% complete.\r"

# The drone runners will need the exact drone-server IP address to connect to it.
# Therefore the drone network is inspected and the IP address of the drone-server container is extracted.
network_info=$(docker network inspect drone-network)

# # Extract the IPv4Address field for the drone-server container dynamically
drone_server_ip=$(echo "$network_info" | jq -r '.[0].Containers | to_entries[] | select(.value.Name == "drone-server") | .value.IPv4Address')

# The IP address are presented in CIDR notation, so the IP address is extracted from the string.
drone_server_ip=$(echo "$drone_server_ip" | cut -d '/' -f 1)

# If the drone server ip is not found, the script will exit.
# Because of this is that the drone server is the essential part of the drone runner.
# The drone runners depend on the server and therefore the server must be running before the runners.
if [ -n "$drone_server_ip" ]; then
    # The drone runner is created and connected to the drone network.
    # The drone runners and settings will not be explained here.
    sudo docker run --detach \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env=DRONE_RPC_HOST=$drone_server_ip:80 \
        --env=DRONE_RPC_SECRET=$random_text \
        --network=drone-network \
        --restart=always \
        --name=runner \
        kraftvaerket/kv-drone-runner:latest
else
    cd ../../
    python3 rename.py notgit
    rm -rf src/drone/venv
    exit 0
fi
printf "######### 90%% complete.\r"


# Create local image registry for image for supply chain attack.

sudo docker run --detach \
    --name registry \
    --publish 6000:6000 \
    registry:2.7.1

# Pull down the start image and then rename 
sudo docker pull kraftvaerket/supply-chain-attack:latest
sudo docker tag kraftvaerket/supply-chain-attack:latest localhost:6000/playwright-supply-image:latest
sudo docker push localhost:6000/playwright-supply-image:latest


# In order for the script to finish, the user must complete the OAuth process for the admin account. 
# This involves visiting the Drone server, logging in with the provided username and password, and then navigating to the account settings to copy the token. 
# Finally, the token should be pasted into the terminal to complete the process.

echo "Enter admin token from Drone"
echo "To activate, go to http://localhost:8080/welcome and login with Username: morten_jakobsen and Password: escrow"
echo "After that go to http://localhost:8080/account and copy the token into here"
echo "Token: "
read admin_token

# When the user adds the token, repositories are activated and secrets are created.
python3 activate.py $admin_token
response_webhooks=$(python3 -m dronecasc drone.yaml -s $admin_token)
if [ $response_webhooks -ne 0 ]; then
    echo "Failure to create webhooks. Exiting."
    cd ../../
    python3 rename.py notgit
    rm -rf src/drone/venv
    exit 1
fi

# Deactivate the virtual environment
deactivate

# Remove the virtual environment
rm -rf venv
cd ../../
# Revert the repositories back to their original state.
python3 rename.py notgit
printf "########## 100%% complete.\r"

# clear
echo "Drone is now ready to use, Open a browser in incognito and go to http://localhost:8080/welcome and login with your credentials you gave to this script."
