import json
import sys
import os

BASE_DIR = os.path.dirname(__file__)
STATE_PATH = os.path.join(BASE_DIR, "state.json")

def change_state(key: str, state: any):
  try:
    with open(STATE_PATH, "r") as f:
      data = json.load(f)
    data[key]= state
    with open(STATE_PATH, "w") as f:
      json.dump(data, f, indent= 1)
  except json.JSONDecodeError:
    print("Error Processing Json")
    
def slash_cmd_triggered(prompt: str, cmd_name: str = ""):
  if prompt.startswith(f"/{cmd_name}"):
    print(prompt, cmd_name)
    change_state("active", True)
  else:
    change_state("active", False)
  
slash_cmd_triggered("/implement", "implement")