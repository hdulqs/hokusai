from hokusai.lib.config import config
from hokusai.lib.command import command
from hokusai.services.configmap import ConfigMap
from hokusai.lib.common import print_green, print_smart
from hokusai.lib.exceptions import HokusaiError

@command()
def create_env(context, namespace=None):
  configmap = ConfigMap(context, namespace=namespace)
  configmap.create()
  print_green("Created configmap %s-environment" % config.project_name)


@command()
def delete_env(context, namespace=None):
  configmap = ConfigMap(context, namespace=namespace)
  configmap.destroy()
  print_green("Deleted configmap %s-environment" % config.project_name)


@command()
def get_env(context, environment, namespace=None):
  configmap = ConfigMap(context, namespace=namespace)
  configmap.load()
  if environment:
    for k, v in configmap.all():
      if k in environment:
        print_smart("%s=%s" % (k, v))
  else:
    for k, v in configmap.all():
      print_smart("%s=%s" % (k, v))


@command()
def set_env(context, environment, namespace=None):
  configmap = ConfigMap(context, namespace=namespace)
  configmap.load()
  for s in environment:
    if '=' not in s:
      raise HokusaiError("Error: environment variables must be of the form 'KEY=VALUE'")
    split = s.split('=', 1)
    configmap.update(split[0], split[1])
  configmap.save()


@command()
def unset_env(context, environment, namespace=None):
  configmap = ConfigMap(context, namespace=namespace)
  configmap.load()
  for s in environment:
    configmap.delete(s)
  configmap.save()
