# Taskflow

[![Deploy Test Status](https://github.com/akbanana7/TaskFlow/actions/workflows/deploy-test.yaml/badge.svg?branch=main&event=push)](https://github.com/akbanana7/TaskFlow/actions/workflows/deploy-test.yaml?query=branch%3Amain)

## Prerequisites

* Docker
* Pretty much everything else is containerised so it will automatically setup

## Setup

You can set this project up in 1 of 2 ways

### Docker compose:

Run this command to make sure any current docker compose sessions are shutdown for this project:
```bash
docker compose down
```
To build the project (may take a while):
```bash
docker compose build
```
Then to run:
```bash
docker compose up
```

All services will be routed through **Traefik** onto **port 80**

### Individual docker containers:

This route will **require you to tinker with the database api/enviroment variables** along with **requiring manual setup of a postgreSQL server** (I will not guide through this yet)

Navigate to ```./analytics``` then run:
```bash
docker build . && docker run (outputted SHA/docker tag)
```
In a new terminal window, navigate to ```./front``` then run:
```bash
docker build . && docker run (outputted SHA/docker tag)
```
These two lines will start up both of the current working services (frontend and DB API)

### The database API is not working properly

**1.** If you used docker compose, im not quite sure what has gone wrong (other than my horrid coding skills) so raise an issue please.

**2.** If you used the individual docker container method, you probably messed up the postgreSQL DB link. I'll publish an install guide at some point

## Project info

### What is this?

This is a calander sort of app. It can take in tasks, along with dates and times for the start/end of tasks. Store them, and then be able to be accessed, updated, and deleted later down the line.

### Why?

I am developing this by myself to understand and learn various concepts and languages.
Including:
* Languages:
    * Python
    * JavaScript
    * HTML/CSS
    * SQL
* Frameworks/software:
    * Docker
    * Node.js
    * PostgreSQL
* Microservice-based architechture
* Containerisation/deployment
* Self hosted authentication
* App security and redundancy

### What stage is this at?

This project is currently in its **VERY** early stages of development. There is some basic proof of concept code down, but nothing that really all works yet.

When I get to a stage where everything does work together, and I believe enough has been put in, i'll compile and put out an initial release.

