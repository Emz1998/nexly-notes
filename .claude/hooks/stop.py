from scripts import validate_checklist, reset_cache


def main():
    # Main agent stop - no blocking validation needed
    # SubagentStop validation is handled by subagent_stop.py
    validate_checklist()
    reset_cache()


if __name__ == "__main__":
    main()
