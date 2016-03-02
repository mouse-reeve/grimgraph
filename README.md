# Grimgraph

## What
Some kind of note taking tool for building the database behind https://www.grimoire.org

## How
To get an instance running:
- Fork this repo and clone it to your development environment
```bash
$ git clone https://github.com/[your_username]/grimgraph.git
```

- Create a virtual environment and install dependencies
```bash
$ virtualenv .
$ source bin/activate
$ pip install -r requirements.txt
```

- [Install Neo4j](http://neo4j.com/download/) version 2.3.1
- Open Neo4j and create or select the desired database
- Set the environment variables `NEO4J_USER` and `NEO4J_PASS` to the Neo4j user and password
- Run the application
```bash
$ python runserver.py
```
