# Empowering DevOps Security: Capture the Flag Challenge in Development and Operations

This repository contains the necessary artifacts to deploy a virtualized CI/CD pipeline
that is meant to be used as an exploration to develop DevOps CTF challenges.

The pipeline is composed of a source control version server (Gitea) and a continuous integration server DroneCI.
Gitea supports the creation of GitHub-like actions that can be executed in DroneCI runners.

The deployment is not trivial and the full deployment automation is almost impossible due to the authentication requirements of DroneCI (using oAuth).

To simplify things, we have deployed for you an instance of Gitea running at `https://full-enormous-crow.ngrok-free.app`. This is where the source of the challenges is going to be.
DroneCI is meant instead to be run by the user. The user can deploy by downloading the repository and execute the instrucitons as indicated in the following section. Since to deploy DroneCI admin privileges are needed, we provide
a VM in which you can safely run the commands. By executing an SSH tunnel the drone server will therefore be available from `http://localhost:8080`.

## How to run the project

<!-- ### Pre-requisites
- Docker (See [Docker installation guide](https://docs.docker.com/get-docker/))
- Python3 (See [Python installation guide](https://www.python.org/downloads/))
- Git (See [Git installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))
- SSH (See [SSH installation guide](https://www.ssh.com/ssh/)) -->

<!-- ### Running the project
Disclaimer: This project will only be able to run on already setup machines by the creator. Contact `mojak1996@gmail.com` if you dont have access
and would like access. -->


<!-- ### Connection to Remote machine -->

### Deploying the drone server

For this exercise, you will be provided access to a virtual machine in which the droneCI should be deployed.
Then, by using a ssh port forward you will be able to access the droneCI as a localhost application.

To play the challenge we assume that the player has the possibility to use SSH and have a browser installed.


<!-- #### Step 1 - Clone the repository
```bash
git clone https://git.imada.sdu.dk/mojak18/Empowering_DevOps_Security.git
cd Empowering_DevOps_Security
``` -->
#### Key creation and Config file.

You will receive a private key necessary to connect to the remote machine and an IP.
You will need to connect to the machine via SSH and establish a port forwarding.
Whenever a connection is made to this port, the connection is forwarded over the secure channel.
To create a port forwarding to this machine you should run something like the following.

```bash
ssh -L 8080:localhost:8080 -i `$KEY_PATH` ucloud@$`IP`
```

where $KEY_PATH is the path where the private key is found and $IP is the IP of the machine to connect to. 

In case of problems, you can also set up the config file as follows (we assume to have the private key
saved in the file named $KEY_FILE_NAME in the folder ~/.ssh)

```bash
chmod 600 ~/.ssh/$KEY_FILE_NAME
echo -e "Host Drone-Machine\n\tHostname $IP\n\tUser ucloud\n\tIdentityFile ~/.ssh/$KEY_FILE_NAME" >> ~/.ssh/config
ssh -L 8080:localhost:8080 Drone-Machine
```  
<!-- ##### Machine-2:
```bash
echo -e "Host CTF-Machine-1\n\tHostname 130.225.38.227\n\tUser ucloud\n\tIdentityFile ~/.ssh/CTF-Machine-2" >> ~/.ssh/config
cat keys/CTF-Machine-2 | ~/.ssh/CTF-Machine-2
chmod 600 ~/.ssh/CTF-Machine-2
ssh -D 8080 CTF-Machine-2
```
The available machines are:
- IP address: `130.225.38.190, CTF-Machine-1`
- IP address: `130.225.38.227, CTF-Machine-2` -->

<!-- Using the -D option for SSH you need a proxy for the webbrowser. 
here you can use FoxyProxy and create a proxy config link the one below. 
![Image](/report/images/foxyproxy.png)
An alternative to *-D* in SSH is a static classical port forwarding like the one below.
```bash
ssh -L 8080:localhost:8080 CTF-machine-1
```
or 
```bash
ssh -L 8080:localhost:8080 CTF-machine-2
``` -->

#### Clone the repository and run the deployment script

When connected to the machine you should first clone the repository of the script
to deploy droneCI. This can be done by executing on the remote machine the following command:
```bash
git clone https://git.imada.sdu.dk/mojak18/Empowering_DevOps_Security.git
```

At this point, you can enter into the folder Empowering_DevOps_Security and run the deployment script.

```bash
cd Empowering_DevOps_Security
sudo ./run.sh <username> <password>
```

username and password will be the username and password that you will have to use to authenticate to
the Gitea framework. As an example:
```bash
sudo ./run.sh Alice secure_password
```

The deployment of the droneCI may require some minutes and is interactive since the installation of
DroneCI and its configuration with Gitea requires OAuth authorization.

Once the script reaches outputs the following text:  
![Image](/report/images/parse_token.png)  
Open up [http://localhost:8080/welcome](http://localhost:8080/welcome) in incognito mode and you will see this webpage.  
![Image](/report/images/drone-welcome.png)  

click on continue and you will be redirected to the Gitea server.
If you see a ngrok pop up that warns you about the site you're about to visit, click on visit site.   
<!-- This is important because this is how the drone server authenticates itself to the Gitea Server. -->
At this point, you need to authenticate to Gitea.
**DO NOT USE the credentials used when invoking the deployment script**
**Use instead the following username and password:**

* *Username: morten_jakobsen* 
* *Password: escrow*

**PLEASE DO NOT USE THESE PRIVILEGES TO ALTER OR INSPECT THE Gitea SETTINGS.**
This account is indeed only required to "Activate repositories" and for the initial setup that
unfortunately requires an admin account.

You should authorize the account for the drone instance.

Then go to [http://localhost:8080/account](http://localhost:8080/account) in incognito mode, copy the personal token (see image below), paste it into the remote terminal running the deployment script, and then press enter.
![Image](report/images/homepage_2.png)

The initial deployment should be completed. Please close all browsers and then you are ready to play the challenges.
You should be able to connect to the Gitea server `https://full-enormous-crow.ngrok-free.app` 
using the credentials you entered into the deployment script.
Moreover, you should be able to access your CI server at `http://localhost:8080/welcome`

In case you end up having problems, you can try to repeat the procedure. Note, however, that before running again the `run.sh` script you should run a `dockerClean`` command and possibly choose another string as username.
 

## Challenges 1
### Get my credentials!

You have now become a brand new collaborator on the repository Abberus!
Abberus is an exciting place to be!

Here in the Abberus repository. We are working with a brand new Flask Application where we use drone for our pipeline. We use drone both for building, testing and deployment.

The pipeline is very restricted to the main branch and is only available for execution with the permission of senior developers! Please create a pull request if you want something changed and pushed into the newest version!

We are happy to have you on our team and look forward to many new good updates on our platform!

The flag format is EDS{string_of_text_with_symbols_and_numbers}

<!-- ## Challenges 2
### Version control is important

## Solutions
Can be found in the report folder, as the readme.md. Dont go in there if you want to solve the challenges yourself. -->

<!-- ## Motivation for this project
This repository is a collection of all the code and documentation used in the thesis. The repository is divided into two main folders, one for the development of the CTF challenges and one for the deployment of the CTF challenges.
Over the past two decades, software development has witnessed the adoption of various practices aimed at ensuring efficient product delivery. Many of these practices have traditionally prioritized development speed and adherence to tight schedules rather than security considerations. Additionally, then use of monolithic architecture in software development has posed challenges in terms of maintenance and updates.  
As a response to these challenges, a more agile approach emerged, breaking down software into smaller components developed by specialized teams. This shift paved the way for the rise of DevOps and its associated culture, which blends development and operations expertise. The DevOps culture has seen significant growth over the last decade and has proven to be highly successful.  
The expansion of DevOps has generated a heightened demand for improved solutions to address the need for accessibility to development environments and assets. This demand has led to the adoption of various technologies and practices, including virtualization, containerization, cloud services, single sign-on, version control software, vaulting, and more.  
This thesis aims to delve into the deployment, development, and maintenance of DevOps challenges specifically focused on the aspect of the pipeline, version control, vaulting, and so on. Also, the thesis aims to use local resources and known technologies such as haaukins, and cloud computing.  
The thesis will also try to explore the possibility of Automated deployment for end-users to deploy their own CTF environment. Although this will not be the clear focus of the thesis, since before controlling and deploying an automated platform using haaukins and such, everything else will have to be completed.  
The primary goal of this research is to gain a deeper understanding of the security challenges associated with the practice of DevOps and
how they intersect with the broader landscape of software development and operations

## Proposal - Empowering DevOps Security: Capture the Flag Challenge in Development and Operations
The proposal is a document that describes the initial idea of the thesis. It is a document that is written before the thesis is started and is used to get approval from the university to start the thesis. The proposal is written in LaTeX and can be found in the folder `Proposal`.
Several things are included in the thesis such as motivation, proposed timetable and such.

## Report
This folder contains the report of the thesis. The report is written in LaTeX and can be found in the folder `Report`. The report is the final document that is handed in to the university and is the result of the thesis. The report contains the following chapters:

### Abstract

### Acknowledgements

### Table of Contents

### List of Figures

### List of Tables

### List of Listings

### List of Abbreviations

### Introduction

## Src - Source code
This folder contains all the source code used in the thesis. The source code is divided into two main folders, one for the development of the CTF challenges and one for the deployment of the CTF challenges. -->