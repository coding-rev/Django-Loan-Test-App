# Loan Application Project
Simple django application with website crawling and excel generation as main features

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Commands](#commands)
* [App endpoints](#app-endpoints)
* [API Documentation](#api-documentation)


## General info
Simple django application with website crawling and excel generation as main features


## Technologies
* Python
* Django
* Django Rest Framework
* Selenium
* BeautifulSoup4
* Xlsxwriter
* Docker
* SQlite3

### Setup
## Installation on Linux and Mac OS
* [Follow the guide here](https://help.github.com/articles/fork-a-repo) on how to clone or fork a repo
* [Follow the guide here](https://docs.docker.com/engine/install/) on how to install and run docker
* To run application with docker
```
docker-compose up --build
```
  
* Copy the IP address provided once your server has completed building the site. (It will say something like >> Serving at http://0.0.0.0:8000).
* Open the address in the browser

## Commands
Open docker bash with 
```
docker ps
docker exec -it <CONTAINER_NAME> bash
```
In our case, default container name is "setup"
* To run migrations
```
python manage.py makemigrations
python manage.py migrate

```
* To run crawler and populate data to db
```
python manage.py crawl_load_data
```

## App Endpoints
* /api/loans - return the list of all saved loans
* /api/countries - returns the list of all saved countries
* /api/sectors - returns the list of all saved sectors
* /api/excel - returns an attachment of generated excel file

## API Documentation
```
http://127.0.0.1:8000/api/doc
```


