from docker import Client
from docker.types import TaskTemplate, ContainerSpec

cli = Client(base_url='tcp://10.0.0.12:2375')
print (cli.info())
print (cli.containers())
# cont = ContainerSpec("my-postgres",)
# task_tmpl = TaskTemplate(cont)
# cli.create_service(task_tmpl)
#cli.inspect_service(service='pgpool')