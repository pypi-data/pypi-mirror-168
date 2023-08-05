import json
from jsonschema import validate
from typing import Dict

configuration_schema = {
  "type": "object",
  "properties": {
    "project": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "outDir": {
          "type": "string"
          }
      }
    },
    "ignore": {"type": "array"},
    "tags": {"type": "object"}
  },
  "required": ["ignore", "tags"]
}

def check_configurations(configuration: Dict):
  validate(configuration, configuration_schema)

def load_configuration(filePath: str)-> Dict:
  configuration = {}
  with open(filePath, encoding="utf-8") as configurationFile:
    configuration = json.load(configurationFile)
  check_configurations(configuration)

  configuration['ignore'].append("*kamino*")
  return configuration