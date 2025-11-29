import json
import sys
import os
from typing import Any

BASE_DIR = os.path.dirname(__file__)
STATE_PATH = os.path.join(BASE_DIR, "state.json")


# Get state for key
def get_states(file_path: str) -> dict:
    try:
        # Check if state file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"State file not found at {file_path}")
        # Load state file
        with open(STATE_PATH, "r") as f:
            data = json.load(f)

        # Get
        return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading state: {e}")
        return {}


# Set state for key
def set_state(key: str, val: Any, state_file_path: str = STATE_PATH):
    try:
        # Check if state file exists
        if not os.path.exists(state_file_path):
            raise FileNotFoundError(f"State file not found at {state_file_path}")

        # Load State File
        with open(state_file_path, "r") as f:
            data = json.load(f)

        # Change Value
        data[key] = val

        # Write on File
        with open(STATE_PATH, "w") as f:
            json.dump(data, f, indent=1)
    except json.JSONDecodeError:
        print("Error Processing Json")


# Check if slash command is triggered
def is_cmd_active(prompt: str):

    # Check if triggered with "/"
    if prompt.startswith(f"/"):
        # Set active state to true
        set_state("active", True)
    else:
        set_state("active", False)


def get_current_phase():
    return get_states["phase"]


def is_iterate() -> bool:
    return get_states["iterate"]
