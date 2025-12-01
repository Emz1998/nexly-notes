#!/usr/bin/env python3
"""
PreToolUse Hook: Enhanced security validation using unified logger
"""
import json
import sys
import os
import re
import time
from datetime import datetime
from pathlib import Path


# Removed UnifiedLogger - now using simple file logging

# Risk scoring system
RISK_SCORES = {
    "low": 1,
    "medium": 5,
    "high": 10,
    "critical": 20
}

# Dangerous patterns with risk levels - ONLY TRULY SYSTEM-DAMAGING OPERATIONS
DANGEROUS_PATTERNS = {
    "paths": {
        # Only block ACTUAL system directories when being modified
        "/etc/passwd": {"risk": "critical", "category": "system"},
        "/etc/shadow": {"risk": "critical", "category": "system"},
        "/boot/": {"risk": "critical", "category": "system"},
        "/sys/": {"risk": "critical", "category": "system"},
        # SSH keys - only the actual private key files
        "id_rsa": {"risk": "critical", "category": "ssh_keys"},
        "id_dsa": {"risk": "critical", "category": "ssh_keys"},
        "id_ecdsa": {"risk": "critical", "category": "ssh_keys"},
        "id_ed25519": {"risk": "critical", "category": "ssh_keys"},
    },
    "commands": {
        # Only block commands that can ACTUALLY damage the system
        "rm -rf / ": {"risk": "critical", "category": "destructive"},
        "rm -rf /*": {"risk": "critical", "category": "destructive"},
        "rm -rf /etc": {"risk": "critical", "category": "destructive"},
        "rm -rf /boot": {"risk": "critical", "category": "destructive"},
        "rm -rf /sys": {"risk": "critical", "category": "destructive"},
        "dd if=/dev/zero of=/dev/": {"risk": "critical", "category": "destructive"},
        "mkfs.ext": {"risk": "critical", "category": "destructive"},
        "mkfs.xfs": {"risk": "critical", "category": "destructive"},
        "mkfs.btrfs": {"risk": "critical", "category": "destructive"},
        "> /dev/sd": {"risk": "critical", "category": "destructive"},
        "> /dev/nvme": {"risk": "critical", "category": "destructive"},
        ":(){ :|:& };:": {"risk": "critical", "category": "malicious"},
        "chmod -r 777 /": {"risk": "critical", "category": "permissions"},
    },
    "file_patterns": {}  # Don't block files by pattern alone
}

def ensure_log_file():
    """Ensure security log file exists with header"""
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    logs_dir = project_dir / ".claude" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "SECURITY.log"

    # Create file with header if it doesn't exist
    if not log_file.exists():
        with open(log_file, "w") as f:
            f.write("""# Security Log

## Format

```
TIME | TYPE | DESCRIPTION | FILE_PATH | AGENT | SESSION | RISK_SCORE | CATEGORIES | DECISION_TIME | MATCHES
```

**Types:** Access, Blocked, Alert, Threat, Vulnerability, Authentication, Authorization, Audit

---

""")

    return log_file

def calculate_risk_score(matches):
    """Calculate total risk score from matches"""
    total_score = 0
    categories = set()
    
    for match in matches:
        risk_level = match.get("risk", "low")
        category = match.get("category", "unknown")
        total_score += RISK_SCORES.get(risk_level, 1)
        categories.add(category)
    
    return total_score, list(categories)

def check_dangerous_path(file_path):
    """Check if a file path is potentially dangerous with risk assessment"""
    if not file_path:
        return False, "", []

    matches = []

    # Only check for ACTUAL dangerous paths (exact matches or critical system files)
    for pattern, details in DANGEROUS_PATTERNS["paths"].items():
        # For system paths, require exact match or directory prefix
        if pattern in file_path:
            # Allow if it's in project directory (.claude, src, etc)
            if "/.claude/" in file_path or "/src/" in file_path or "/tests/" in file_path:
                continue
            matches.append({
                "pattern": pattern,
                "risk": details["risk"],
                "category": details["category"],
                "reason": f"Attempting to modify critical system file: {pattern}"
            })

    if matches:
        risk_score, categories = calculate_risk_score(matches)
        should_block = risk_score >= RISK_SCORES["critical"]  # Only block CRITICAL paths
        reason = "; ".join([m["reason"] for m in matches])
        return should_block, reason, matches

    return False, "", []

def check_dangerous_command(command):
    """Check if a command is potentially dangerous with risk assessment"""
    if not command:
        return False, "", []

    cmd_lower = command.lower()
    matches = []

    # Only check for TRULY dangerous command patterns
    for pattern, details in DANGEROUS_PATTERNS["commands"].items():
        if pattern.lower() in cmd_lower:
            matches.append({
                "pattern": pattern,
                "risk": details["risk"],
                "category": details["category"],
                "reason": f"CRITICAL: System-damaging command detected: {pattern}"
            })

    if matches:
        risk_score, categories = calculate_risk_score(matches)
        # Only block CRITICAL commands that can actually destroy the system
        should_block = risk_score >= RISK_SCORES["critical"]
        reason = "; ".join([m["reason"] for m in matches])
        return should_block, reason, matches

    return False, "", []

def rotate_log_if_needed(log_file, max_entries=1000):
    """Rotate log file if it exceeds max entries"""
    try:
        if not log_file.exists():
            return

        with open(log_file, "r") as f:
            lines = f.readlines()

        # Find where entries start (after the header)
        entry_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == "---":
                entry_start_idx = i + 1
                break

        # Count actual log entries (non-empty lines after header)
        entries = [line for line in lines[entry_start_idx:] if line.strip()]

        # If exceeds max, keep only the header and last max_entries
        if len(entries) > max_entries:
            header = lines[:entry_start_idx]
            recent_entries = entries[-max_entries:]

            with open(log_file, "w") as f:
                f.writelines(header)
                f.write("\n")
                f.writelines(recent_entries)

    except Exception:
        # Fail silently
        pass

def sanitize_and_truncate(text, max_length=80):
    """Sanitize and truncate text for logging"""
    if not text:
        return "N/A"

    # Replace newlines and excessive whitespace with single space
    text = re.sub(r'\s+', ' ', text.strip())

    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length - 3] + "..."

    return text

def log_security_event(session_id, tool_name, tool_input, analysis_result):
    """Log security event to SECURITY.log in markdown format"""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Determine risk level and type
        risk_score = analysis_result["risk_score"]
        if risk_score >= RISK_SCORES["critical"]:
            risk_level = "CRITICAL"
        elif risk_score >= RISK_SCORES["high"]:
            risk_level = "HIGH"
        elif risk_score >= RISK_SCORES["medium"]:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Determine event type
        if analysis_result["blocked"]:
            event_type = "Blocked"
        elif risk_score > 0:
            event_type = "Alert"
        else:
            event_type = "Access"

        # Build description
        status = "BLOCKED" if analysis_result["blocked"] else "ALLOWED"
        description = f"{status} - {risk_level} RISK"

        # Get file path or command and sanitize it
        file_path = tool_input.get("command") or tool_input.get("file_path", "N/A")
        file_path = sanitize_and_truncate(file_path, max_length=100)

        # Get categories
        categories = ", ".join(analysis_result["risk_categories"]) if analysis_result["risk_categories"] else "none"

        # Get log file path
        log_file = ensure_log_file()

        # Format log entry (TIME | TYPE | DESCRIPTION | FILE_PATH | AGENT | SESSION | RISK_SCORE | CATEGORIES | DECISION_TIME | MATCHES)
        log_entry = f"- {time_str} | {event_type} | {description} | {file_path} | {tool_name} | {session_id} | {risk_score} | {categories} | {analysis_result['decision_time_ms']}ms | {len(analysis_result['matches'])}\n"

        # Read existing content
        with open(log_file, "r") as f:
            lines = f.readlines()

        # Find where entries section starts (after "---")
        entries_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == "---":
                entries_start_idx = i + 1
                break

        # Check if today's date header exists
        date_header_idx = -1
        for i in range(entries_start_idx, len(lines)):
            if f"### {date_str}" in lines[i]:
                date_header_idx = i
                break

        # Rotate log if needed (every 10th write to reduce I/O)
        import random
        if random.randint(1, 10) == 1:
            rotate_log_if_needed(log_file, max_entries=1000)

        # Insert entry at the top
        if date_header_idx != -1:
            # Date header exists, insert entry right after it
            # Skip the date header line and any blank lines
            insert_idx = date_header_idx + 1
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            lines.insert(insert_idx, log_entry)
        else:
            # Create new date header at the top of entries
            new_section = ["\n", f"### {date_str}\n", "\n", log_entry]
            # Insert after entries_start_idx, skipping any blank lines
            insert_idx = entries_start_idx
            while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                insert_idx += 1
            for item in reversed(new_section):
                lines.insert(insert_idx, item)

        # Write back to file
        with open(log_file, "w") as f:
            f.writelines(lines)

    except Exception:
        # Fail silently
        pass


try:
    # Start timing for performance metrics
    start_time = time.time()
    
    # Load input from stdin
    input_data = json.load(sys.stdin)
    
    # Validate input structure
    if not isinstance(input_data, dict):
        raise ValueError("Invalid input: expected dictionary")
    
    # Extract and validate data
    session_id = input_data.get("session_id", "")
    if session_id and not re.match(r'^[a-zA-Z0-9\-_]+$', session_id):
        raise ValueError("Invalid session_id format")
    
    tool_name = input_data.get("tool_name", "")
    if tool_name and not re.match(r'^[A-Za-z]+$', tool_name):
        raise ValueError("Invalid tool_name format")
    
    tool_input = input_data.get("tool_input", {})
    if not isinstance(tool_input, dict):
        raise ValueError("Invalid tool_input: expected dictionary")
    
    # Initialize analysis result
    analysis_result = {
        "blocked": False,
        "risk_score": 0,
        "risk_categories": [],
        "matches": [],
        "reason": "",
        "decision_time_ms": 0
    }
    
    # Perform security analysis based on tool type
    if tool_name in ["Write", "Edit", "MultiEdit"]:
        file_path = tool_input.get("file_path", "")
        should_block, reason, matches = check_dangerous_path(file_path)
        if matches:
            risk_score, categories = calculate_risk_score(matches)
            analysis_result.update({
                "blocked": should_block,
                "risk_score": risk_score,
                "risk_categories": categories,
                "matches": matches,
                "reason": reason
            })
            
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        should_block, reason, matches = check_dangerous_command(command)
        if matches:
            risk_score, categories = calculate_risk_score(matches)
            analysis_result.update({
                "blocked": should_block,
                "risk_score": risk_score,
                "risk_categories": categories,
                "matches": matches,
                "reason": reason
            })
    
    # Calculate decision time
    decision_time = (time.time() - start_time) * 1000
    analysis_result["decision_time_ms"] = round(decision_time, 2)
    
    # Log to date-based folders
    log_security_event(session_id, tool_name, tool_input, analysis_result)
    
    # Handle blocking decision
    if analysis_result["blocked"]:
        # Return JSON to block with detailed feedback
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Security Policy Violation: {analysis_result['reason']} (Risk Score: {analysis_result['risk_score']})"
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # Allow the operation - suppress output
    print(json.dumps({"suppressOutput": True}))
    sys.exit(0)
    
except Exception as e:
    # Log error but don't block execution
    try:
        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
        error_log = project_dir / ".claude" / "logs" / "errors.log"
        error_log.parent.mkdir(parents=True, exist_ok=True)
        with open(error_log, "a") as f:
            f.write(f"{datetime.now().isoformat()} - Surveillance security hook error: {str(e)}\n")
    except:
        pass  # Fail silently if error logging fails
    sys.exit(0)