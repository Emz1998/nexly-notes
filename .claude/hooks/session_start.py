# import json
# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent))

# from utils import read_stdin_json, set_cache


# def get_milestone():
#     try:
#         return json.loads(Path("project/status.json").read_text()).get(
#             "current_milestone", ""
#         )
#     except (json.JSONDecodeError, FileNotFoundError):
#         return ""


# def main():
#     input_data = read_stdin_json()
#     set_cache("plan_mode", "session_id", input_data.get("session_id", ""))

#     response = {
#         "hookSpecificOutput": {
#             "hookEventName": "SessionStart",
#             "additionalContext": f"Session id : {input_data.get('session_id')}\n  Milestone: {get_milestone()}",
#         }
#     }
#     print(json.dumps(response))
#     sys.exit(0)


# if __name__ == "__main__":
#     main()
