# #!/usr/bin/env python3
# """
# Hook: subagent_stop
# Event: SubagentStop
# Purpose: Dispatch to specialized modules for subagent stop validation
# """

# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent))

# from plan_mode import validate_subagent_stop as plan_validate_stop
# from research_mode import validate_subagent_stop as research_validate_stop
# from explore_mode import validate_subagent_stop as explore_validate_stop
# from code_mode import validate_subagent_stop as code_validate_stop
# from code_review_mode import validate_subagent_stop as code_review_validate_stop
# from utils import read_stdin_json


# def main():
#     input_data = read_stdin_json()

#     # Validate plan mode subagent completed required work before stopping
#     plan_validate_stop(input_data)

#     # Validate research mode subagent completed required work before stopping
#     research_validate_stop(input_data)

#     # Validate explore mode subagent completed required work before stopping
#     explore_validate_stop(input_data)

#     # Validate code mode subagent completed required work before stopping
#     code_validate_stop(input_data)

#     # Validate code-reviewer produced review report before stopping
#     code_review_validate_stop(input_data)


# if __name__ == "__main__":
#     main()
