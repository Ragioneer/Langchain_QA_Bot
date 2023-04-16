# Lanchain_QA_Bot
This is a Q&amp;A bot based on generative AI using GPT-3 engines

When crafting a commit, it‘s very important to only include changes that belong together. You should
never mix up changes from multiple, different topics in a single commit. For example, imagine
wrapping both some work for your new login functionality and a fix for bug #122 in the same
commit

To set-up the web-application:

* you need to create a virtual environment and activate, if using a linux distro the cmd is **`python3 -m venv venv && source ./venv/bin/activate`**.
* If you don't have it install the cmd follows as `sudo apt install python3-venv` or `sudo yum install python3-venv` depending on your distro

* run **`pip install -r requirements.txt`** to install dependencies
* Copy the .env file using .env.example file.

### If you want to use your own PDF

* The way it is designed you can download a pdf from an s3 bucket (I've done this because I will be deploying the app on AWS. by running **file.py**. make sure to setup related env variables
* You can upload the file into your project directory and specify the relative file path to the FILE_NAME env variable, or simply use an online PDF by running **pdfloader.py** make sure to uncomment your option in code


### if you want to use the same pdf as mine

* set the FILE_NAME variable as **`"./git.pdf"`** and run **pdfloader.py**

* **`flask run`** to run the application
