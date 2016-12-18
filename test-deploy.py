import requests
import json

data = {"projectName":"test",
        "deployPlan":"postgres publish pgpool",
        "swarmCluster":"test-cluster",
        "params":{"POSTGRES_USER":"testuser",
                  "POSTGRES_PASSWORD":"testpass",
                  "POSTGRES_DB": "testdb",
                  }}
r = requests.post("http://127.0.0.1:8000/Deploy/",data=json.dumps(data))
print (r.text)

