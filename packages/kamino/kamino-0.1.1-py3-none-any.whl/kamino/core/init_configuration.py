import json

def init_configuration(filename: str, outDir: str):
  """
    Create kamino initial configurations
  """
  repo_name = filename
  initial_configs = {
    'project': {
      'name': repo_name
    },
    'ignore': ['*node_modules*', '*__pycache__*', '.git*', '.pytest_cache*'],
    'tags': {
      'exampleTag': 'value' 
    }
  }

  json_initial_configs = json.dumps(initial_configs, indent=2)
  with open(f'{outDir}/{filename}.kamino.json', 'w', encoding="utf-8") as file:
    file.write(json_initial_configs)
    print("Configuration file created!")