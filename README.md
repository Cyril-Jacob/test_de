# Drug Journal

Drug Journal is a Python Package that helps in building a data pipeline and do some analysis to deal with drug related data published in various scientific journals.

<br/>


## Table of Contents
1. [Design](#design)
2. [Installation](#installation)
2. [Static analysis](#static-analysis)
2. [Test](#test)
2. [Documentation](#documentation)
2. [Usage](#usage)
2. [Build package & Installation](#build-package-and-installation)

<br/>

## Design

We have decided to represent the entities and their relationships via UML in a class diagram.(see docs/drug_journal_uml.png)

![class diagram](docs/drug_journal_uml.png?raw=true "Drug journal class diagram")

The split of three entities (drug, publications and readers) was mainly due to the effort to respect SOLID principle. 
A more natural relationship between entities would have been to have a journal class composed of publications that are themselves composed of drugs, but that was not my choice with regards to the problem we are trying to solve centered on drugs.  

Two abstract classes were used to respect as much as possible Python principle DRY: CSVReader and Publication. 
Methods that could be put in helpers were implemented as static methods in theses classes.

A package 'drug_journal' can be built to help reuse most of the class features. 

Data pipeline consists of three stages:

- Data loading: 
Reading CSV files and JSON files

- Data cleaning:
Remove inconsistencies rows (e.g. missing mandatory fields), 
Fix data error (e.g. extra \xC3)

- Data wrangling:
Output in JSON Format a linked graph between drugs and publications/journals

Data analysis consists of reusing the graph structure built in Drug class during the data pipeline process to answer the question of the journal with higher drugs (question 4)

<br/>

## Installation

This code is run on Windows using Python 3.9.13 and virtual environment venv.

> pip3 install venv

> pip3 install -r requirements.txt

Note: 
json5 package is used in reading csv to recover from extra comma character in the file.
dev_requirements.txt is built out of 'pip freeze' and help to know the exact version used.

<br/>

## Static analysis

mypy is used as static type checker.

> dmypy run -- main.py drug_journal/*.py

> dmypy check .\main.py

<br/>

## Test

unittest toot is used to test units of our code.

Execute all tests:
> python3 -m unittest discover .\tests\

Execute specific test:
> python3 -m unittest tests.test_drug.TestDrug

<br/>

## Documentation

pdoc is used to automatically generate source documentation from Python docstring.
Generate the documentation on drug journal package:
> pdoc .\drug_journal\ -o .\docs\

<br/>
Tree view of the project:

    main.py: 
        - entry point of the project 
        - Data pipeline and Data analysis are launched here
    
    drug_journal:
        - root directory of our package containing reader classes, publication classes and drug class

    tests:
        - unittest Testcases are in implemented in this directory
    
    data:
        - input and output data of the project; more verbose outputs are displayed in the console as well
    
    test_de: 
        - question 6 part I and SQL queries for part II
<br/>

## Usage

Run Data Pipeline (question 3) and Data Analysis (question 4)

> python3 -m main

  
    This command outputs the drug graph JSON in data/output/drug/graph.json and the journal with higher number of drugs in the console in addition with extra logs.



## Build package and installation

> python3 setup.py sdist bdist_wheel

> python3 setup.py install
