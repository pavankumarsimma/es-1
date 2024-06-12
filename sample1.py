from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    "https://a01a6a959e654cdeb34630302869463f.us-central1.gcp.cloud.es.io",  # Elasticsearch endpoint
    api_key="V1RSaURKQUJuLUVrbDRQTnRZVHc6X1k0N0pHejFUOE9lS1ktZmNEeVNfUQ==",
)
index_name = 'sample_doc_1'

mapping = {
    "mappings":{
        "properties":{
            "popularity": {"type": "integer"},
            "ratings": {"type": "float"},
            "reviews_count": {"type": "integer"},
            "description": {"type": "text"},
            "category": {"type": "keyword"}
        }
    }
}

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print("NOTE: created index 'sample_doc_1'")

    # Sample documents
    documents = [
        {"popularity": 10, "ratings": 4.5, "reviews_count": 100, "description": "A great product", "category": "electronics"},
        {"popularity": 20, "ratings": 4.0, "reviews_count": 150, "description": "Good quality item", "category": "home"},
        {"popularity": 5, "ratings": 5.0, "reviews_count": 50, "description": "Excellent value", "category": "clothing"},
        {"popularity": 7, "ratings": 4.7, "reviews_count": 120, "description": "Highly recommended", "category": "electronics"},
        {"popularity": 15, "ratings": 3.5, "reviews_count": 200, "description": "Decent product", "category": "home"},
        {"popularity": 12, "ratings": 4.2, "reviews_count": 80, "description": "Worth the price", "category": "clothing"},
        {"popularity": 9, "ratings": 4.8, "reviews_count": 90, "description": "Best purchase ever", "category": "electronics"},
        {"popularity": 14, "ratings": 4.1, "reviews_count": 110, "description": "Very satisfied", "category": "home"},
        {"popularity": 18, "ratings": 3.9, "reviews_count": 130, "description": "Not bad", "category": "clothing"},
        {"popularity": 6, "ratings": 4.6, "reviews_count": 95, "description": "Loved it", "category": "electronics"},
        {"popularity": 8, "ratings": 4.3, "reviews_count": 140, "description": "Good product", "category": "home"},
        {"popularity": 11, "ratings": 4.0, "reviews_count": 85, "description": "Will buy again", "category": "clothing"},
        {"popularity": 17, "ratings": 3.7, "reviews_count": 115, "description": "Satisfied with the quality", "category": "electronics"},
        {"popularity": 4, "ratings": 4.4, "reviews_count": 70, "description": "Nice and compact", "category": "home"},
        {"popularity": 16, "ratings": 3.8, "reviews_count": 160, "description": "Pretty good", "category": "clothing"},
        {"popularity": 19, "ratings": 3.6, "reviews_count": 105, "description": "Okay product", "category": "electronics"},
        {"popularity": 13, "ratings": 4.9, "reviews_count": 155, "description": "Superb quality", "category": "home"},
        {"popularity": 3, "ratings": 4.0, "reviews_count": 45, "description": "Decent for the price", "category": "clothing"},
        {"popularity": 2, "ratings": 4.1, "reviews_count": 60, "description": "Good enough", "category": "electronics"},
        {"popularity": 1, "ratings": 4.2, "reviews_count": 35, "description": "Value for money", "category": "home"}
    ]

    # Index the documents
    for i, doc in enumerate(documents):
        es.index(index=index_name, document=doc)


# Query 1: Match all documents
query1 = {
    "query": {
        "match_all": {}
    }
}

# Query 2: Match documents where the category is 'electronics'
query2 = {
    "query": {
        "match": {
            "category": "electronics"
        }
    }
}

# Query 3: Range query on popularity (greater than 10)
query3 = {
    "query": {
        "range": {
            "popularity": {
                "gt": 10
            }
        }
    }
}

# Query 4: Full-text search on the description field
query4 = {
    "query": {
        "match": {
            "description": "great product"
        }
    }
}

# Query 5: Boolean query combining multiple conditions
query5 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"category": "home"}},
                {"range": {"ratings": {"gte": 4.0}}}
            ]
        }
    }
}

# Query 6: Custom ranking function based on multiple fields
query6 = {
    "query": {
        "function_score": {
            "query": {
                "match_all": {}
            },
            "script_score": {
                "script": {
                    "source": """
                        double popularity = doc['popularity'].value;
                        double ratings = doc['ratings'].value;
                        double reviews_count = doc['reviews_count'].value;
                        
                        double custom_score = (popularity * 0.3) + (ratings * 0.5) + (Math.log(reviews_count + 1) * 0.2);
                        
                        return custom_score;
                    """
                }
            }
        }
    }
}

# Query 7: Custom ranking function based on multiple fields asc order
query7 = {
    "query": {
        "function_score": {
            "query": {
                "match_all": {}
            },
            "script_score": {
                "script": {
                    "source": """
                        double popularity = doc['popularity'].value;
                        double ratings = doc['ratings'].value;
                        double reviews_count = doc['reviews_count'].value;
                        
                        double custom_score = (popularity * 0.4) + (ratings * 0.6) + (Math.log(reviews_count + 1) * 0.2);
                        
                        return custom_score;
                    """
                }
            }
        }
    },
    "sort":{
        "_score":"asc"
    }
}

# Query 8: same like query6 but if description contains the match "value for money" it gives boost of two for that particular funtion and sums it to the final score from the script
query8 = {
    "query": {
        "function_score": {
            "query": {
                "match_all": {}
            },
            "functions": [
                {
                    "filter": {
                        "match": {
                            "description": "value for money"
                        }
                    },
                    "weight": 2
                },
                {
                    "script_score": {
                        "script": {
                            "source": """
                                double popularity = doc['popularity'].value;
                                double ratings = doc['ratings'].value;
                                double reviews_count = doc['reviews_count'].value;
                                
                                double custom_score = (popularity * 0.3) + (ratings * 0.5) + (Math.log(reviews_count + 1) * 0.2);
                                
                                return custom_score;
                            """
                        }
                    }
                }
            ],
            "boost_mode": "sum" 
        }
    },
    "size": 20
}

# Function to execute a query and print the results
def execute_and_print(query):
    print("Query :")
    print(json.dumps(query, indent=4))
    res = es.search(index=index_name, body=query)
    results = [{
        "_score": hit['_score'],
        "_source": hit['_source']
    } for hit in res['hits']['hits']]
    print("Output :")
    print(f"Total hits: {res['hits']['total']['value']}")
    print(json.dumps(results, indent=4))


# execute_and_print(query2)




queries = [query1, query2, query3, query4, query5, query6, query7, query8]
# queries = [query6, query8]


for i, query in enumerate(queries, 1):
    print(f"Query {i} results:")
    execute_and_print(query)
    print("\n")



