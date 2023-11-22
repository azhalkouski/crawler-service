import json


def openServiceConfig():
  serviceConfig = None

  try:
      with open("searchConfig.json") as search_config_file:
         serviceConfig = json.load(search_config_file)

  except Exception as e:
     print(f"Exception while reading serviceConfig: {e}")
     # TODO: log the error to file

  return serviceConfig
