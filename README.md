# Unify news tag generator

This repository contains the news tag generator for the project Unify. It is part of the Final Work of Axelle Vanden Eynde for the Bachelor Multimedia and Communication Technology at the Erasmus University College.

The news tag generator is a small api that generates content labels for news articles in dutch. 

## Get it running

1. Clone this repository
2. run the command `python -m pip install -r requirements.txt`
3. run the command `python labels.py`

## Usage

The API has a single route: 

POST `/generateDutchLabels` 

the body must at least contain these fields
```
{
    title: "",
    description: ""

}
```
