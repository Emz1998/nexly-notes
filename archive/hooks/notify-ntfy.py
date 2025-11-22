#!/usr/bin/env python3
"""
ntfy.sh Notification Hook for Claude Code
Sends push notifications to your phone/browser via ntfy.sh
"""

import json
import sys
import os
import subprocess
from datetime import datetime

# Configuration - Change this to your unique topic name
NTFY_TOPIC = "claude-code-tasks"  # Change this to something unique!
NTFY_SERVER = "https://ntfy.sh"  # Default public server (or use your own)

def send_ntfy_notification(title, message, priority="default"):
    """Send notification via ntfy.sh using curl"""
    try:
        url = f"{NTFY_SERVER}/{NTFY_TOPIC}"

        # Build curl command
        curl_cmd = [
            'curl', '-s',
            '-H', f'Title: {title}',
            '-H', f'Priority: {priority}',
            '-d', message,
            url
        ]

        # Send the notification
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check if successful (ntfy returns JSON with id field on success)
        if '"id"' in result.stdout:
            # Log success
            log_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/ntfy.log')
            try:
                with open(log_file, 'a') as f:
                    f.write(f"[{datetime.now().isoformat()}] Sent: {title} - {message}\n")
            except:
                pass
            return True

        return False
    except Exception as e:
        # Log error but don't block Claude
        print(f"ntfy error: {e}", file=sys.stderr)
        return False

def track_session_activity(input_data):
    """Track tool usage in session for Stop event summary"""
    # Get the session_id from input_data - Claude Code provides it
    session_id = input_data.get('session_id', '')

    # If no session_id, we can't track this activity properly
    if not session_id:
        return

    hook_event = input_data.get('hook_event_name', '')
    tool_name = input_data.get('tool_name', '')
    params = input_data.get('tool_input', {})

    tracking_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/session_activity.json')

    # Load existing data
    session_data = {}
    if os.path.exists(tracking_file):
        try:
            with open(tracking_file, 'r') as f:
                session_data = json.load(f)
        except:
            pass

    # Initialize session if not exists
    if session_id not in session_data:
        session_data[session_id] = {
            'files_edited': [],
            'files_created': [],
            'commands_run': 0,
            'agents_launched': [],
            'last_prompt': '',
            'all_prompts': [],
            'last_activity': datetime.now().isoformat()
        }

    # Ensure all_prompts exists for older sessions
    if 'all_prompts' not in session_data[session_id]:
        session_data[session_id]['all_prompts'] = []

    current = session_data[session_id]

    # Track user prompts
    if hook_event == "UserPromptSubmit":
        # According to Claude Code docs, UserPromptSubmit has prompt directly in input_data
        prompt = input_data.get('prompt', '')

        if prompt:
            # Truncate very long prompts
            if len(prompt) > 150:
                prompt = prompt[:150] + '...'
            current['last_prompt'] = prompt
            # Keep track of all prompts in session
            current['all_prompts'].append(prompt)
            # Only keep last 5 prompts
            if len(current['all_prompts']) > 5:
                current['all_prompts'] = current['all_prompts'][-5:]

    # Track different tool types
    elif tool_name in ["Edit", "MultiEdit"]:
        file_path = params.get('file_path', '')
        if file_path:
            basename = os.path.basename(file_path)
            if basename not in current['files_edited']:
                current['files_edited'].append(basename)

    elif tool_name == "Write":
        file_path = params.get('file_path', '')
        if file_path:
            basename = os.path.basename(file_path)
            if basename not in current['files_created']:
                current['files_created'].append(basename)

    elif tool_name == "Bash":
        current['commands_run'] += 1

    elif tool_name == "Task":
        subagent = params.get('subagent_type', '')
        if subagent and subagent not in current['agents_launched']:
            current['agents_launched'].append(subagent)

    current['last_activity'] = datetime.now().isoformat()

    # Save updated data
    try:
        os.makedirs(os.path.dirname(tracking_file), exist_ok=True)
        with open(tracking_file, 'w') as f:
            json.dump(session_data, f, indent=2)
    except:
        pass

def get_context_message(input_data):
    """Extract contextual information from the input data"""
    hook_event = input_data.get('hook_event_name', '')
    tool_name = input_data.get('tool_name', '')
    params = input_data.get('params', {})

    # For Stop hook - get session context and summary
    if hook_event == "Stop":
        # Extract session information - Claude Code always provides session_id
        session_id = input_data.get('session_id', '')
        stop_hook_active = input_data.get('stop_hook_active', False)

        # Debug: Log the actual input structure (only in debug mode)
        debug_mode = os.environ.get('NTFY_DEBUG', '').lower() == 'true'
        if debug_mode:
            log_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/ntfy-debug.log')
            try:
                with open(log_file, 'a') as f:
                    f.write(f"[{datetime.now().isoformat()}] Stop event input:\n")
                    f.write(json.dumps(input_data, indent=2)[:1000] + "\n\n")
            except:
                pass

        # The Stop event doesn't include tool usage directly
        # We'll need to track this via PostToolUse events or parse transcript
        # For now, just provide a simple completion message
        context_parts = []

        # Initialize variables to track prompts
        user_prompts = []

        # Check if we have a transcript path to potentially parse
        transcript_path = input_data.get('transcript_path', '')

        # Try to read recent activity from a tracking file if we maintain one
        tracking_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/session_activity.json')
        if os.path.exists(tracking_file) and session_id:
            try:
                with open(tracking_file, 'r') as f:
                    session_data = json.load(f)
                    current_session = session_data.get(session_id, {})

                    # If we have the session, use it
                    if current_session:
                        pass  # We have the data
                    else:
                        # Session not found - this might be the first Stop without any tracked activity
                        current_session = {}

                    files_edited = current_session.get('files_edited', [])
                    files_created = current_session.get('files_created', [])
                    commands_run = current_session.get('commands_run', 0)
                    agents_launched = current_session.get('agents_launched', [])
                    last_prompt = current_session.get('last_prompt', '')
                    all_prompts = current_session.get('all_prompts', [])

                    # Use all prompts if available, otherwise use last prompt
                    if all_prompts:
                        user_prompts = all_prompts
                    elif last_prompt:
                        user_prompts = [last_prompt]

                    # Build a more descriptive summary
                    if files_edited:
                        count = len(files_edited)
                        if count <= 3:
                            # Show actual filenames if not too many
                            files_str = ', '.join(files_edited[:3])
                            context_parts.append(f"📝 Edited: {files_str}")
                        else:
                            context_parts.append(f"📝 Edited {count} files")

                    if files_created:
                        count = len(files_created)
                        if count <= 2:
                            files_str = ', '.join(files_created[:2])
                            context_parts.append(f"✨ Created: {files_str}")
                        else:
                            context_parts.append(f"✨ Created {count} files")

                    if commands_run:
                        context_parts.append(f"⚡ {commands_run} command{'s' if commands_run > 1 else ''}")

                    if agents_launched:
                        if len(agents_launched) <= 3:
                            # Show agent names if not too many
                            agents_str = ', '.join(agents_launched)
                            context_parts.append(f"🤖 Used: {agents_str}")
                        else:
                            context_parts.append(f"🤖 {len(agents_launched)} agents")
            except:
                pass

        # Default message if nothing tracked and no prompts
        if not context_parts and not user_prompts:
            context_parts.append("✅ Session completed")

        # Don't add session ID to context since it's not very useful
        # The actual work done is more important than the session identifier

        # Format the prompts for display
        prompt_display = ""
        if user_prompts:
            # Only show the most recent prompt (last one in the list)
            last_prompt = user_prompts[-1]
            prompt_text = last_prompt.strip()
            if len(prompt_text) > 150:
                prompt_text = prompt_text[:150] + '...'
            prompt_display = prompt_text

        context = ' | '.join(context_parts) if context_parts else ""

    # For subagent completion
    elif hook_event == "SubagentComplete":
        subagent_type = params.get('subagent_type', 'unknown')
        result = params.get('result', {})
        success = result.get('success', False)

        if success:
            context = f"✅ {subagent_type} completed successfully"
        else:
            context = f"⚠️ {subagent_type} completed with issues"

    # For individual tool hooks
    elif tool_name:
        context_parts = []

        if tool_name == "Edit" or tool_name == "MultiEdit":
            file_path = params.get('file_path', 'unknown file')
            edits = params.get('edits', [])
            if tool_name == "MultiEdit" and edits:
                context_parts.append(f"📝 {len(edits)} edits to {os.path.basename(file_path)}")
            else:
                context_parts.append(f"📝 Edited {os.path.basename(file_path)}")

        elif tool_name == "Write":
            file_path = params.get('file_path', 'unknown file')
            context_parts.append(f"✨ Created {os.path.basename(file_path)}")

        elif tool_name == "Bash":
            command = params.get('command', '')
            description = params.get('description', '')
            if description:
                context_parts.append(f"⚡ {description}")
            elif command:
                cmd_preview = command[:40] + '...' if len(command) > 40 else command
                context_parts.append(f"⚡ {cmd_preview}")

        elif tool_name == "Read":
            file_path = params.get('file_path', 'unknown file')
            context_parts.append(f"👁️ Reading {os.path.basename(file_path)}")

        elif tool_name == "TodoWrite":
            todos = params.get('todos', [])
            completed = sum(1 for t in todos if t.get('status') == 'completed')
            in_progress = sum(1 for t in todos if t.get('status') == 'in_progress')
            total = len(todos)
            context_parts.append(f"📋 Todos: {completed}/{total} done, {in_progress} active")

        elif tool_name == "Task":
            subagent = params.get('subagent_type', 'unknown')
            description = params.get('description', '')
            if description:
                context_parts.append(f"🤖 {subagent}: {description}")
            else:
                context_parts.append(f"🤖 Launched {subagent}")

        elif tool_name == "Grep" or tool_name == "Glob":
            pattern = params.get('pattern', params.get('query', ''))
            context_parts.append(f"🔍 Searching: {pattern[:30]}")

        elif tool_name == "SlashCommand":
            command = params.get('command', '')
            if command:
                context_parts.append(f"🎯 {command}")

        elif tool_name.startswith("mcp__"):
            # MCP tool usage
            tool_short = tool_name.split('__')[-1]
            context_parts.append(f"🔧 {tool_short}")
        else:
            context_parts.append(f"🔨 {tool_name}")

        context = ' | '.join(context_parts) if context_parts else "Task in progress"

    else:
        context = "General task completed"

    # Get working directory and project name
    cwd = os.getcwd()
    project_name = os.path.basename(cwd) if cwd else "workspace"

    # For NEXLY RN project, use the project name
    if "nexly" in project_name.lower() or os.path.exists("/workspace/CLAUDE.md"):
        project_name = "NEXLY RN"

    # Convert to EDT (Eastern Daylight Time) - PDT is 3 hours behind EDT
    from datetime import timedelta
    edt_time = datetime.now() + timedelta(hours=3)

    return {
        'context': context,
        'project': project_name,
        'timestamp': edt_time.strftime("%I:%M %p EDT"),
        'prompt': prompt_display if 'prompt_display' in locals() else ""
    }

def main():
    try:
        # Read input from Claude
        input_data = json.load(sys.stdin)

        # Extract relevant information
        hook_event = input_data.get('hook_event_name', '')

        # Handle different hook events
        if hook_event == "Stop":
            # Main completion hook
            context_info = get_context_message(input_data)

            # Build detailed message
            title = "🤖 Main Agent"

            # Start with the user's prompt(s) if available
            message_parts = []
            if context_info.get('prompt'):
                message_parts.append(f"💬 Prompt:\n{context_info['prompt']}")
                message_parts.append("")  # Empty line for spacing

            # Add the work summary
            if context_info['context']:
                message_parts.append("📊 Work Done:")
                context_lines = context_info['context'].split(' | ')
                if len(context_lines) > 1:
                    # Multi-line format for better readability
                    for line in context_lines:
                        message_parts.append(line)
                else:
                    message_parts.append(context_info['context'])

            # Add timestamp
            message_parts.append(f"\n⏰ {context_info['timestamp']}")

            message = '\n'.join(message_parts)

            # Determine priority based on context
            priority = "default"
            if "error" in context_info['context'].lower() or "failed" in context_info['context'].lower():
                priority = "high"
                title = "⚠️ Main Agent"

            # Send the notification
            send_ntfy_notification(
                title,
                message,
                priority=priority
            )

        elif hook_event == "SubagentStop":
            # Subagent completion hook - similar to Stop but for subagents
            # Get session information
            session_id = input_data.get('session_id', '')

            # Try to get the subagent type from the input
            subagent_type = 'Subagent'

            # Check in params first
            params = input_data.get('params', {})
            if params.get('subagent_type'):
                subagent_type = params.get('subagent_type', 'Subagent')

            # Format the subagent name for the title (capitalize and format nicely)
            formatted_agent = subagent_type.replace('-', ' ').title()

            # Build context info similar to Stop event
            context_parts = []
            user_prompts = []

            # Try to read activity from tracking file
            tracking_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/session_activity.json')
            if os.path.exists(tracking_file) and session_id:
                try:
                    with open(tracking_file, 'r') as f:
                        session_data = json.load(f)
                        current_session = session_data.get(session_id, {})

                        if current_session:
                            files_edited = current_session.get('files_edited', [])
                            files_created = current_session.get('files_created', [])
                            commands_run = current_session.get('commands_run', 0)
                            all_prompts = current_session.get('all_prompts', [])

                            # Get prompts
                            if all_prompts:
                                user_prompts = all_prompts

                            # Build work summary
                            if files_edited:
                                count = len(files_edited)
                                if count <= 3:
                                    files_str = ', '.join(files_edited[:3])
                                    context_parts.append(f"📝 Edited: {files_str}")
                                else:
                                    context_parts.append(f"📝 Edited {count} files")

                            if files_created:
                                count = len(files_created)
                                if count <= 2:
                                    files_str = ', '.join(files_created[:2])
                                    context_parts.append(f"✨ Created: {files_str}")
                                else:
                                    context_parts.append(f"✨ Created {count} files")

                            if commands_run:
                                context_parts.append(f"⚡ {commands_run} command{'s' if commands_run > 1 else ''}")
                except:
                    pass

            # Format prompt for display (only most recent)
            prompt_display = ""
            if user_prompts:
                last_prompt = user_prompts[-1]
                prompt_text = last_prompt.strip()
                if len(prompt_text) > 150:
                    prompt_text = prompt_text[:150] + '...'
                prompt_display = prompt_text

            # Build message
            title = f"🤖 {formatted_agent}"
            message_parts = []

            # Add prompt if available
            if prompt_display:
                message_parts.append(f"💬 Prompt:\n{prompt_display}")
                message_parts.append("")  # Empty line for spacing

            # Add work summary
            if context_parts:
                message_parts.append("📊 Work Done:")
                for part in context_parts:
                    message_parts.append(part)
            else:
                message_parts.append("✅ Task completed")

            # Add timestamp
            from datetime import timedelta
            edt_time = datetime.now() + timedelta(hours=3)
            message_parts.append(f"\n⏰ {edt_time.strftime('%I:%M %p EDT')}")

            message = '\n'.join(message_parts)

            send_ntfy_notification(
                title,
                message,
                priority="low"  # Subagent completions are usually less critical
            )

        elif hook_event == "PostToolUse":
            # Track all tool usage for session summary
            track_session_activity(input_data)

            # Optional: Add notifications for specific tool completions
            tool_name = input_data.get('tool_name', '')

            # Only notify for significant tools
            if tool_name in ["Task", "SlashCommand"]:
                context_info = get_context_message(input_data)

                title = f"🔧 Tool - {context_info['project']}"
                message = f"{context_info['context']}\n⏰ {context_info['timestamp']}"

                send_ntfy_notification(
                    title,
                    message,
                    priority="low"
                )

        elif hook_event == "UserPromptSubmit":
            # Track the prompt for session context
            track_session_activity(input_data)
            # Don't send notifications for prompts, just track them

        elif hook_event == "SessionStart":
            # Clean up old session data (older than 7 days)
            tracking_file = os.path.join(os.environ.get('CLAUDE_PROJECT_DIR', '.'), '.claude/hooks/session_activity.json')
            if os.path.exists(tracking_file):
                try:
                    with open(tracking_file, 'r') as f:
                        session_data = json.load(f)

                    # Remove old sessions
                    now = datetime.now()
                    cleaned_data = {}
                    for sid, data in session_data.items():
                        last_activity = data.get('last_activity', '')
                        if last_activity:
                            try:
                                last_time = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                                age_days = (now - last_time).days
                                if age_days < 7:
                                    cleaned_data[sid] = data
                            except:
                                cleaned_data[sid] = data  # Keep if can't parse date

                    # Save cleaned data
                    with open(tracking_file, 'w') as f:
                        json.dump(cleaned_data, f, indent=2)
                except:
                    pass

        # Success - continue normally
        sys.exit(0)

    except Exception as e:
        # Log error but don't block Claude
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Non-blocking

if __name__ == "__main__":
    main()