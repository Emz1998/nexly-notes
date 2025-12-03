#!/usr/bin/env python3
"""Test git commands using subprocess."""

import subprocess


def run_git_command(command: list[str]) -> str:
    """Run a git command and return raw output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout + result.stderr


def main():
    """Run git status and git log commands."""
    print(run_git_command(["git", "status", "--porcelain"]))
    print(run_git_command(["git", "log", "--oneline", "-5"]))
    print(run_git_command(["git", "log", "-3", "--format=%h %an %s"]))


if __name__ == "__main__":
    main()
