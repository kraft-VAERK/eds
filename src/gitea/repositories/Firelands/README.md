# Firelands
"👋 Welcome to the EDS Developer Training Repository: Pipeline Edition! 🚀

Hello, aspiring pipeline creators! Whether you're a seasoned developer looking to expand your skill set or a newcomer eager to dive into the world of continuous integration and delivery, you've come to the right place.

In this repository, we're focused on empowering you with the knowledge and tools to craft robust and efficient pipelines tailored to EDS's unique development environment. From version control to automated testing and deployment, we've curated a collection of resources designed to demystify the pipeline creation process and set you on the path to success.

Within these digital halls, you'll discover step-by-step guides, hands-on exercises, and real-world examples to help you master the art of pipeline creation. Whether you're building pipelines for web applications, microservices, or infrastructure as code, we've got you covered.

So, buckle up and get ready to embark on a journey of exploration and discovery. Your pipeline-building adventure starts now!

Happy pipelining! 💻✨"
## Pipeline Construction.
### Step 1 - Config
At EDS, Docker is the cornerstone of our pipeline infrastructure. 
When configuring Drone, specify docker as the type. Drone supports various pipeline types, including exec, k8s, docker-ssh, and more.

Set the kind to pipeline and the type docker. Then move unto next step before commiting, since the pipeline will need
a step before being able to rune!

```
    kind: 
    type: 
    name: im-learning
```
### Step 2 - Steps, Pipeline does things
Choosing a name and an image for the step you want to run. This is the cornerstone of the pipeline
Choosing the correct image for the step is crucial, you dont want to choose a nodeJS image for a python application run

Get it to run with a registry.devops.eds/python:buster image and give it the command to run with python file in repository called `app.py`
In the command section you write commands like you would in a normal linux machine. here you should run the python file called
`app.py` and see the out on the drone side. 

```
    steps:
      - name: 
        image:
        commands:
```
### Step 3 - Services, Utility for steps.
Services are a help for the steps. What that means is that if you need a external service such temporary database, a second 
server for network connectivity and such, services will run until the pipeline has finished.

Start a server from the file `python_server.py`. You should also modify the steps, so that container has the 
python package that the `app.py` needs for the connections to the server. The first python script will try to connect 
to the server using a url. The service is exposed through drone internal dns. The name you give a step or a service is its domain name, 
in drone internal DNS records. The services should be named `python-server`. If name otherwise, you should change the name in the
`app.py` file.

```
    services:
      - name: 
        image:
        commands:
```
### Step 4 - Environments and Indentation
The drone pipeline support multiple different functions and they're vaulable for the use of the pipeline
variable.

Create an entire new step under the first step (Not the service but under the step) where you created 
a python file run.
Once you have created the step, make the use of environmental function in the steps,
and make it connect to the repository `https://registry.devops.eds`
The docker image needed from the eds registry is docker:1.

1. Environment
    Environment makes it possible for us to declare variable to use in the steps, without having 
    to show them during our execute, this means that you can use passwords in the pipeline execution.
2. Identation
    Since it a yml file, the indentation is important. Therefore keeping the identation
    clean is important for the pipeline to work.

```
  environment:
    from_secret:
  PASSWORD:
    from_secret: 
  USERNAME:
```
If anything is unclear or needs more information there's documentation at [Drone](https://docs.drone.io/)
### Step Getting the flag.
For the last step you must create a new step or modify a previous one to execute the python file `flag.py`
you must use the secret `FLAG` in the same way you did in step 4 to login with docker. You must give the 
python program the flag as input when executing