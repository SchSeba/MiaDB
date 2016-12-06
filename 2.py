from docker import Client
from docker.types import TaskTemplate, ContainerSpec

cli = Client(base_url='tcp://127.0.0.1:2376')
print (cli.containers())
cont = ContainerSpec("my-postgres",)
task_tmpl = TaskTemplate(cont)
cli.create_service(task_tmpl)
#cli.inspect_service(service='pgpool')