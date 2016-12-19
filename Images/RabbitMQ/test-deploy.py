import requests
import json

data = {"projectName":"test",
        "deployPlan":"rabbitmq",
        "swarmCluster":"test-cluster",
        "params":{}}
r = requests.post("http://127.0.0.1:8000/Deploy/",data=json.dumps(data))
print (r.text)

