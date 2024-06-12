from elasticsearch import Elasticsearch
import json
import time
from datetime import datetime

es = Elasticsearch(
    "https://a01a6a959e654cdeb34630302869463f.us-central1.gcp.cloud.es.io",  # Elasticsearch endpoint
    api_key="V1RSaURKQUJuLUVrbDRQTnRZVHc6X1k0N0pHejFUOE9lS1ktZmNEeVNfUQ==",
)

index_name = "kibana_sample_data_ecommerce"

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# res = es.search(index=index_name, body={
#     "query": {
#         "match_all": { }
#     },
#     "size": 10,
#     "_source": {
#         "includes": ["*"],
#         "excludes": ["products"]
#     }
# })

# res = es.search(index=index_name, body={
#     "query":{
#         "bool":{
#             "must":{
#                 "match":{ "category":"Women's Clothing" }
#             },
#             "filter":{
#                 "range" : {
#                     "taxless_total_price" : { "gte" : 20, "lte" : 40 }
#                 }
#             },
#             "boost":2.0
#         }
#     },
#     "size":20,
#     "_source":{
#         "includes":["*"],
#         "excludes":["products"]
#     }
# })

# res = es.search(index=index_name, body={
#     "query":{
#         "bool":{
#             "should":[
#                 {"match":{
#                     "customer_gender":{
#                         "query": "MALE"
#                     }
#                 }},
#                 {"match":{
#                     "day_of_week":{
#                         "query":"Monday",
#                         "boost":3
#                     }
#                 }},
#                 {"match":{
#                     "day_of_week":{
#                         "query":"Tuesday",
#                         "boost":2
#                     }
#                 }}
#             ],
#             "minimum_should_match":1
#         }
#     },
#     "sort":{
#         "_score":"desc"
#     }
# })



results = [{
    "_score":hit['_score'],
    "_source":hit['_source']
} for hit in res['hits']['hits']]

print(json.dumps(results, indent=4))
