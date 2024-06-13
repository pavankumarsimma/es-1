# Elasticsearch Sample Document Indexing and Querying

This repository contains a Python script for indexing sample documents into an Elasticsearch index and performing various queries to demonstrate the use of different querying techniques and custom scoring functions in Elasticsearch.

### FILES
#### Code - sample1.py
#### Output - outputs.txt
#### Dependencies - requirements.txt

## Table of Contents
- [Introduction](#introduction)
- [Design](#design)
- [Installation](#installation)
- [Running the Script](#running-the-script)

## Introduction

This code demonstrates how to:
- Create an Elasticsearch index with a specific mapping.
- Index sample documents into the created index.
- Perform various types of queries, including match, range, full-text search, boolean, and custom scoring queries.
- Implement a custom scoring function using `script_score`.

## Design

### Index Mapping

The index is created with the following fields:
- `popularity`
- `ratings`
- `reviews_count`
- `description`
- `category`

### Sample Documents

A total of 20 sample documents are indexed, each containing values for the fields defined in the index mapping.

### Queries

Eight different queries are performed on the indexed documents:
1. **Match All**: Retrieves all documents.
2. **Category Match**: Retrieves documents where the category is "electronics".
3. **Range Query**: Retrieves documents where the popularity is greater than 10.
4. **Full-Text Search**: Searches for documents with the description "great product".
5. **Boolean Query**: Combines multiple conditions (e.g., category is "home" and ratings are greater than or equal to 4.0).
6. **Custom Scoring Function**: Ranks documents based on a custom scoring function using multiple fields.
7. **Custom Scoring with Sort**: Similar to query 6 but sorts the results in ascending order of the custom score.
8. **Custom Scoring with Boost**: Custom scoring function with an additional boost for documents where the description contains "value for money".

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/pavankumarsimma/es-1.git
    cd es-1
    ```

2. **Install dependencies**:
    Install the python dependencies from requirements.txt file:
    ```bash
    pip install requirements.txt
    ```
    You can create a python virtual env such that there won't be any problems in installing the packages.

## Running the Script

1. **Update the Elasticsearch configuration**:
    Modify the `es = Elasticsearch(...)` line in the script to use your own Elasticsearch endpoint and API key.

2. **Run the script**:
    Execute the script using Python:
    ```bash
    python sample1.py 
    ```
    or 
    ```bash
    python sample1.py > outputs.txt
    ```
    to capture the output in a separate file `outputs.txt`

