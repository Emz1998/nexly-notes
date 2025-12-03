# #!/usr/bin/env python3
# """
# Hook: user_prompt_submit
# Event: UserPromptSubmit
# Purpose: Dispatch to specialized modules for prompt handling
# """

# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent))

# from plan_mode import activate_plan_mode
# from research_mode import activate_research_mode
# from explore_mode import activate_explore_mode
# from code_mode import activate_code_mode
# from code_review_mode import activate_code_review_mode
# from implement_flow_mode import activate_implement_flow
# from utils import read_stdin_json


# def main():
#     input_data = read_stdin_json()
#     prompt = input_data.get("prompt", "").lower()

#     # Activate implement flow on /implement command (tracks slash command sequence)
#     if prompt.startswith("/implement"):
#         activate_implement_flow(input_data)

#     # Activate plan mode on /plan command
#     elif prompt.startswith("/plan"):
#         activate_plan_mode(input_data)

#     # Activate research mode on /research command
#     elif prompt.startswith("/research"):
#         activate_research_mode(input_data)

#     # Activate explore mode on /explore command (Phase 1: Explore)
#     elif prompt.startswith("/explore"):
#         activate_explore_mode(input_data)

#     # Activate code mode on /code command (TDD workflow)
#     elif prompt.startswith("/code-review"):
#         activate_code_review_mode(input_data)

#     elif prompt.startswith("/code"):
#         activate_code_mode(input_data)


# if __name__ == "__main__":
#     main()
