# simple_fastapi_template ⏩

This is a microservice template written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework and deployed in AWS Lambda using [Mangum](https://mangum.io).

## Introduction and Objectives ⁉
The main objective is to provide a template for repositories that can be used as a starting point for new projects. This architecture is based on the Clean Architecture, and it was based in many other projects and books, articles that were mixed by the students of Mauá Institute of Technology, from the academic group Dev. Community Mauá.
## How to use 🤔
First of all, you need to create a repo using issues from [Devmaua setup](https://github.com/Maua-Dev/devmaua_setup/), set the **project_name** as you prefer and project template as **simple_fastapi_template** and make sure it's **public** . Hit create issue and wait for the setup to finish.

After that you need to clone your new repo, create a virtual environment and install the requirements.

## Installation 👩‍💻

### Create virtual ambient in python (only first time)

###### Windows

    python -m venv venv

###### Linux

    virtualenv -p python3.9 venv

#### Activate the venv

###### Windows:

    venv\Scripts\activate

###### Linux:

    source venv/bin/activate

#### Install the requirements

    pip install -r requirements-dev.txt
    pip install -r requirements.txt

#### Run the tests

    pytest

#### Run the server local

    uvicorn src.app.main:app

### Atention 🚨
In order to deploy your microservice in AWS Lambda, you need to follow some rules:
- The routes must be created using FastAPI decorators;
- Don't use complete import, only relative ones. (eg: from .move_function import move);
- ALWAYS test your code before pushing it to the repo. You can use pytest to test your code;
- Don't forget to create your own tests;
- Make sure there is a \_\_init\_\_.py file each directory, otherwise it's not a Python package;
- Every file should be inside the app folder;

### Deploy 🚀

### \<FAST API DRAW IO\>

After pushing your code to the repo, it will trigger an action to deploy your code in AWS Lambda. You can find the action in the **.github/workflows/aws_cd.yml** file.

In the first time you push your code, the action will create a new stack in AWS CloudFormation. After that, every time you push your code, the action will update the stack with the new code.

In the [Actions](https://github.com/Maua-Dev/battlesnake_fastapi_template/actions) tab you can see the status of the deploy, and if it was successful or not. If it was successful, you can find the URL of your API in the outputs tab of the action (in the final part of the "Deploy with CDK" step).


![Action Tab](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/ca447b23-e4f3-423c-8ba2-3f7c891849c9)
![CD](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/1340c269-f182-46eb-ae12-1d0bdd6059a2)
![STEP](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/6129f465-a54d-46fc-b45a-c8b219a6823b)

There you can find your API URL. You can use this URL to create your Battlesnake in the Battlesnake website. You can find the documentation [here](https://docs.battlesnake.com/guides/getting-started#step-2-create-a-battlesnake).
You can also find an user and password to access the AWS Console and view the logs of the lambda function to debug it.

![Outputs](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/e06bf1dd-18cc-4057-91ea-3ccd8074848f)


To login in the AWS Console, click in the link name "console" on the output, and then click in "Sign in to a different account". There you need to put the account id and the user and password from the outputs tab. On your login you are required to change your password, DON'T FORGET THE NEW ONE. After that you can click in the link to lambda console, and click monitor to find the logs.

![Lambda Console](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/8a584df8-9efe-432d-9083-6f3523b7f58c)
![Cloudwatch Logs](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/94483cd1-ae3c-46c0-86df-d8fff0b0490e)

After finishing your project, you can delete it from our backend using our CD.

![AwsDestroy](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/68a73993-c55e-4ba8-8bf9-2becbc9decf6)

## Useful tools 🛠

- [Postman](https://www.postman.com/) - API development environment
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Python3.9](https://docs.python.org/3.9/) - Python Documentation

## Thanks 👢🍿

We hope you like and enjoy it! Thanks!

## Contributors 💰🤝💰

This project was developed to use inside Dev. Community Mauá, but feel free to help!.

- Bruno Vilardi - [Brvilardi](https://github.com/Brvilardi) 👷‍♂️
- Hector Guerrini - [hectorguerrini](https://github.com/hectorguerrini) 🧙‍♂️
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) 😎
- Luigi Trevisan - [LuigiTrevisan](https://github.com/LuigiTrevisan) 🔙 
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio) 🌞

## Contact us 📞
If you have any questions, feel free to contact us! You can find us in our [Discord](https://discord.gg/Yr2VPgAmcb) server.
