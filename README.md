# Lexigraph
Acquire vocabulary tailored to <u>you</u>.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#folder-structure">Folder Structure</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#what-i-learned-until-now">What I learned until now!</a></li>
  </ol>
</details>

## About the project
Create and add cards to Anki from a word
with its definition, spoken version and a sample dialog tailored to the chosen occupation.
All of this without leaving this containerized website, 
while keeping it self-hosted.
<br/>
Built upon <a href="https://www.youtube.com/watch?v=dam0GPOAvVI">this</a> website tutorial,
using APIs from <a href="https://ollama.com/">Ollama</a> and <a href="https://foosoft.net/projects/anki-connect/">AnkiConnect</a>
for my specific use case (ease the Anki card-making process based on newly learned words I've been accumulating)
<br/>
Another goal was to learn more about APIs, Python and the cloud.

## Installation
1. Install the <a href="https://docs.docker.com/engine/install/">Docker engine</a>
2. Install <a href="https://docs.docker.com/compose/gettingstarted">Docker Compose</a>
3. Clone the repo
```bash
git clone https://github.com/axelcarapinha/Lexigraph.git 
```
4. Create the .env files
```bash
touch Lexigraph/.env 
touch Lexigraph/0_interface/.env 
```
5. Place this data in each of them
```bash
BASE_API_WORD='http://lexigraph-api-ollama:7653/'
DATABASE_NAME='database.db'
SERVER_SECRET_KEY='a-secret-of-your-choice'
AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY='this-is-not-needed-for-now'
```
6. Running Lexigraph
```bash
cd 
sudo bash install.sh -y # remove the -y for it to wait for confirmation
sudo docker-compose up --build
```

## Folder Structure
```sh
.
├── 0_audios
├── 0_data
├── 0_interface
│   ├── app.py
│   ├── config.py
│   ├── requirements.Flask.txt
│   └── website
│       ├── api_anki.py
│       ├── api_request.py
│       ├── authn.py
│       ├── __init__.py
│       ├── models.py
│       ├── static
│       │   ├── HTML5-template
│       │   │   ├── assets
│       │   │   │   ├── css
│       │   │   │   ├── js
│       │   │   │   ├── sass
│       │   │   │   └── webfonts
│       │   │   ├── images
│       │   │   │   ├── logo-lexigraph-4.png
│       │   │   │   ├── logo-lexigraph-4-rounded.png
│       │   │   ├── index.html
│       │   │   ├── LICENSE.txt
│       │   │   └── README.txt
│       │   ├── index.js
│       │   └── logo-Lexigraph.png
│       ├── templates
│       │   ├── about.html
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── login.html
│       │   └── sign_up.html
│       └── views.py
├── 1_app-api
│   ├── llm_prompt.py
│   └── main.py
├── 2_ollama-data
├── docker-compose.yaml
├── Dockerfile.Api-Ollama
├── Dockerfile.Flask
├── Dockerfile.Ollama
├── install.sh
├── README.md
├── requirements.Api-Ollama.txt
└── run-ollama.sh
```

## Results
Click <a href="https://www.youtube.com/watch?v=9o9YHCFGIJg">here</a> to watch the video.

## What I learned until now!
Had fun knowing more about:
* APIs (types of APIs, how they function, ...)
* Python (classes, packages, dependencies, exceptions, environment variables, ...)
* Flask 
    * using in websites (with the Jinja2 templating language)
    * to make APIs
* Authentication and authorization _in practice_
* Database creation and management with sqlalchemy
* Ollama (chosing and deploying LLMs, its APIs, ...)
* Docker 
    * Docker Compose
    * Docker networks
    * Docker volumes
* Cross-Origin Resource Sharing (to add cards from the browser with the JS fetch API)
<br/>
<br/>


The Azure deployment must be deeply modified, because my student plan does _not_ allow everything I was using X'D. <br/>But learned about this along the way:
* Cloud deployments (using Microsoft Azure)
    * Web Applications
    * Container Registries
    * Container Instances
    * WebHooks
    * Load balancers
    * Automations (with Azure Runbooks)
    * Application Insights (integrated with Python logging)
    * Azure VNets (only the website was exposed to the public network, not the APIs)
    * How to optimize resource usage (was making that a logged visit would trigger a Runbook that would start Ollama's VM)
* Passkeys 
    * theoretical foundations
    * challenges of applying into practice
    * the easier management provided by <a href="https://www.corbado.com/blog">Corbado</a>
* Telegram bots (how to develop them, use them, ...)
