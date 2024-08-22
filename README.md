# Empowering DevOps Security: Capture the Flag Challenge in Development and Operations

This repository contains the necessary artifacts to deploy a virtualized CI/CD pipeline
that is meant to be used as an exploration to develop DevOps CTF challenges.

The pipeline is composed of a source control version server (Gitea) and a continuous integration server DroneCI.
Gitea supports the creation of GitHub-like actions that can be executed in DroneCI runners.

The deployment of the pipeline is fully automized and can be done if using ```bash sudo ./prerun.sh```
## How to run the project

### Pre-requisites
- Docker (See [Docker installation guide](https://docs.docker.com/engine/install/ubuntu/))
- Part of the sudoers group
- Ubuntu or Kali linux, the project is not aimed towards any other Operating system for the time being.

If you dont want to run on your own machines run it through virtualbox. Kali Linux virtualbox image can be found at:
https://cdimage.kali.org/kali-2024.1/kali-linux-2024.1-virtualbox-amd64.7z

### prerun.sh
prerun is the script which is run to deploy the pipeline command to run the script is:
```bash
    sudo ./prerun.sh
```


First part of why the script needs sudo access is to run docker commands.
Now there is multiple docker commands in the prerun script. But the two main onces are


```bash
    docker network create network_eds
    docker compose up -d
```
First docker command is the create the network where the containers will run.
Second command is to spawn the containers, since the containers


Second command is to spawn the containers, since the containers


Now this script needs access to sudo because it needs access to ```/etc/hosts```.
Because it needs access to the hosts file on linux is to do the command:

```bash
	sudo echo -e "$GATEWAY_IP\tgit.devops.eds" >> /etc/hosts
	sudo echo -e "$GATEWAY_IP\tdrone.devops.eds" >> /etc/hosts
	sudo echo -e "$GATEWAY_IP\tregistry.devops.eds" >> /etc/hosts
    sudo echo -e "$GATEWAY_IP\tdevops.eds" >> /etc/hosts
```
This adds the DNS records in your local ```/etc/hosts``` with the IP of "$GATEWAY_IP"
so that possible to access the four different URL's for the challenge

### Run the project

1. Clone the project
```bash
    git clone https://git.imada.sdu.dk/mojak18/Empowering_DevOps_Security.git
```
2. Move into Empowering_DevOps_Security direct and inside the src/ folder
```bash
    cd Empowering_DevOps_Security/src
```
If you're an Kali Linux - Run the Command inside the src folder `sudo ./install-docker-kali.sh`
3. Start the pipeline and create DNS records inside `/etc/hosts` and certificate in `/etc/ssl/certs/ca-certificates.crt`
```bash
    sudo ./prerun.sh
```
4. Explore git, drone, and registry
```
Username: Alice
Password: password
```
    1. https://git.devops.eds
    2. https://drone.devops.eds
    3. https://registry.devops.eds
<!--
## Challenges 1 Our webiste is our brand
Welcome to Empowering DevOps Security!

Here at EDS, we understand that developers like you are the lifeblood of innovation. That's why we've crafted our website to be more than just a platform – it's a playground for your creativity, a hub for collaboration, and a gateway to endless possibilities.

As you navigate through our Developer Portal, you'll find a treasure trove of tools, documentation, and resources designed to fuel your imagination and streamline your development process. Whether you're a seasoned pro or just starting your coding journey, we're here to support you every step of the way.

Please make sure you've landed the correct place and happy hunting! :)

The flag format is HKN{string_of_text_with_symbols_and_numbers}


Access to EDS Organization Products

To access all the products within the EDS organization, users must be accepted by an EDS admin. Currently, we are in the process of hiring someone to manage this role, so granting access to the organization is temporarily unavailable.

We appreciate your patience as we work to fill this position. In the meantime, you might want to consider if there’s an alternative way to gain access—perhaps by finding an account that is already part of the organization? 

While we don’t officially endorse any alternative methods, creative solutions often arise in challenging situations like this. 

The flag format is HKN{string_of_text_with_symbols_and_numbers}

## Challenges 2 Training is key
Welcome to the Firelands, Drone Training Repository.

Here at EDS, we understand the importance of empowering developers like you with the knowledge and skills needed to succeed. That's why we've curated this comprehensive training repository specifically for the Drone tool – your gateway to mastering drone-based development and automation.

Whether you're a novice eager to learn the basics or an experienced developer looking to deepen your expertise, you'll find everything you need right here. Our training materials cover a wide range of topics, from setting up your first Drone pipeline to advanced automation techniques and best practices.

The flag format is HKN{string_of_text_with_symbols_and_numbers}

## Challenges 3 Controlling the pipeline
You've stepped into the role of the new developer for our esteemed project, Amirdrassil!

Amirdrassil stands as one of our company's flagship products, boasting our renowned photo service. While we've maintained this project with care, we're eager to welcome your fresh perspective.

As you familiarize yourself with our existing pipeline, we encourage you to prioritize security enhancements. Feel empowered to make necessary modifications to fortify our system against potential vulnerabilities.

The flag format is HKN{string_of_text_with_symbols_and_numbers}

## Challenges 4
### Get my credentials!

You have now become a brand new collaborator on the repository Abberus!
Abberus is an exciting place to be!

Here in the Abberus repository. We are working with a brand new Flask Application where we use drone for our pipeline. We use drone both for building, testing and deployment.

The pipeline is very restricted to the main branch and is only available for execution with the permission of senior developers! Please create a pull request if you want something changed and pushed into the newest version!

We are happy to have you on our team and look forward to many new good updates on our platform!

The flag format is HKN{string_of_text_with_symbols_and_numbers}


## Solutions
Can be found in the report folder, as the readme.md. Dont go in there if you want to solve the challenges yourself.
Although you will have to switch the branch report to find them :)
 -->

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
