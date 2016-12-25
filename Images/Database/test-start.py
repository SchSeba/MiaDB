import requests
import json

data = {"projectName":"test",
        "deployPlan":"postgres publish pgpool",
        "swarmCluster":"test-cluster"}
r = requests.post("http://127.0.0.1:8000/StartDeployment/",data=json.dumps(data))
print (r.text)

