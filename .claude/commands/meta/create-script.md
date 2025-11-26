---
name: create-script
description: Deploy script-writer agent to create Python scripts
allowed-tools: all
argument-hint: <script-name> <instructions>
model: claude-opus-4-5-20251101
---

Deploy @agent-script-writer to create a Python script named $1 that will $2. Save the script to ./scripts/ directory.

## 1. Context

This command delegates Python script creation to the specialized script-writer agent for automation and utility tasks.

- Purpose: Automate Python script generation through agent delegation
- Use case: When users need custom Python scripts for automation, data processing, or utilities
- Dependencies: @agent-script-writer agent with script creation capabilities
- Requirements: Script name and clear instructions for functionality

## 2. Goal / Intent

Deploy the script-writer agent to create a well-structured Python script based on user requirements.

- Primary objective: Generate Python script named $1 that accomplishes $2
- Expected outcome: Complete, functional Python script saved to ./scripts/$1.py
- Deliverables: Python script with proper structure, error handling, and documentation

## 3. Constraints / Rules

Technical requirements and boundaries for script generation.

- Technical constraints: Python 3.8+ compatible, prefer standard library
- Scope boundaries: Only Python scripts, delegate entirely to script-writer agent
- Quality standards: PEP 8 compliance, proper error handling, comprehensive docstrings
- Always provide comprehensive reports back to main agent

## 4. Output Format

Expected deliverables and reporting structure.

- Report structure: Confirmation with script path, brief functionality summary, usage instructions
- File locations: ./scripts/$1.py
- Response style: Concise report with example command to run the script

## 5. Examples

Usage patterns and execution examples.

- Good approach: Clear instructions with specific requirements, let script-writer handle implementation
- Bad approach: Vague instructions or attempting to write script directly without agent
- Sample usage: /create-script data_processor "process CSV files and generate summary statistics"
