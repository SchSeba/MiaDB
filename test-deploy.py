import requests
import json

data = {"projectName":"test",
        "deployPlan":"postgres",
        "swarmCluster":"test-cluster",
        "params":{"POSTGRES_USER":"testuser",
                  "POSTGRES_PASSWORD":"testpass",
                  "POSTGRES_DB": "testdb",
                  }}
r = requests.post("http://192.168.88.136:8000/Deploy/",data=json.dumps(data))
print (r.text)

