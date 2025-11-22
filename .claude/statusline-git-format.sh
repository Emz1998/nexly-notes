#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Debug: Save the JSON structure to a file for analysis (uncomment to debug)
echo "$input" | jq . > /tmp/claude-statusline-debug.json 2>/dev/null || echo "$input" > /tmp/claude-statusline-debug.json

# Extract data from JSON FIRST
model=$(echo "$input" | jq -r '.model.display_name // .model.id // "Unknown Model"')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "$(pwd)"')
transcript_path=$(echo "$input" | jq -r '.transcript_path // ""')

# Temporary debugging: log transcript path and first few chars of transcript  
echo "DEBUG: transcript_path=$transcript_path" >> /tmp/claude-debug.log
if [ -f "$transcript_path" ]; then
    echo "DEBUG: transcript exists, size=$(wc -c < "$transcript_path" 2>/dev/null || echo "unknown")" >> /tmp/claude-debug.log
    echo "DEBUG: first 500 chars of transcript: $(head -c 500 "$transcript_path" 2>/dev/null | tr '\n' ' ')" >> /tmp/claude-debug.log
else
    echo "DEBUG: transcript does not exist or is not readable" >> /tmp/claude-debug.log
fi

# Function to extract token usage from transcript
get_token_usage() {
    local transcript="$1"
    
    # Default token limit based on model
    local token_limit="200000"
    if [[ "$model" == *"opus"* ]] || [[ "$model" == *"Opus"* ]]; then
        token_limit="200000"
    elif [[ "$model" == *"sonnet"* ]] || [[ "$model" == *"Sonnet"* ]]; then
        token_limit="200000"  
    elif [[ "$model" == *"haiku"* ]] || [[ "$model" == *"Haiku"* ]]; then
        token_limit="200000"
    fi
    
    # First try to get token count from Claude Code's session data if available
    local tokens_used=0
    local exceeds_200k=$(echo "$input" | jq -r '.exceeds_200k_tokens // false' 2>/dev/null)
    
    if [ "$exceeds_200k" = "true" ]; then
        tokens_used=200000  # Max tokens if it exceeds
        echo "${tokens_used}+/${token_limit}"
        return
    fi
    
    # If transcript doesn't exist or isn't readable, return default
    if [ ! -f "$transcript" ] || [ ! -r "$transcript" ]; then
        echo "--/${token_limit}"
        return
    fi
    
    # Parse JSONL format to get actual token usage from the session
    local input_total=0
    local output_total=0
    local cache_creation_total=0
    local cache_read_total=0
    
    # Method: Get token totals from the LAST assistant message (matches --verbose behavior)
    if command -v jq >/dev/null 2>&1; then
        # Find the last line with assistant type and usage data in JSONL format
        local last_usage_line=$(grep '"type":"assistant"' "$transcript" | grep '"usage"' | tail -1 2>/dev/null)
        
        if [ "$last_usage_line" != "" ]; then
            local last_usage=$(echo "$last_usage_line" | jq -r '.message.usage' 2>/dev/null)
            
            if [ "$last_usage" != "" ] && [ "$last_usage" != "null" ]; then
                input_total=$(echo "$last_usage" | jq -r '.input_tokens // 0' 2>/dev/null || echo "0")
                output_total=$(echo "$last_usage" | jq -r '.output_tokens // 0' 2>/dev/null || echo "0")
                cache_creation_total=$(echo "$last_usage" | jq -r '.cache_creation_input_tokens // 0' 2>/dev/null || echo "0")
                cache_read_total=$(echo "$last_usage" | jq -r '.cache_read_input_tokens // 0' 2>/dev/null || echo "0")
                
                # Clean up any non-numeric values
                input_total=$(echo "$input_total" | grep -E '^[0-9]+$' || echo "0")
                output_total=$(echo "$output_total" | grep -E '^[0-9]+$' || echo "0")
                cache_creation_total=$(echo "$cache_creation_total" | grep -E '^[0-9]+$' || echo "0")
                cache_read_total=$(echo "$cache_read_total" | grep -E '^[0-9]+$' || echo "0")
                
                tokens_used=$((input_total + output_total + cache_creation_total + cache_read_total))
            fi
        fi
    fi
    
    # Fallback method using grep if jq fails
    if [ "$tokens_used" = "0" ]; then
        # Find the last assistant message with usage data using grep
        local last_assistant_line=$(grep -n '"type":"assistant".*"usage":' "$transcript" | tail -1 | cut -d: -f1 2>/dev/null)
        if [ "$last_assistant_line" != "" ]; then
            local last_input=$(sed -n "${last_assistant_line}p" "$transcript" | grep -o '"input_tokens":[[:space:]]*[0-9]\+' | grep -o '[0-9]\+' | head -1 2>/dev/null || echo "0")
            local last_output=$(sed -n "${last_assistant_line}p" "$transcript" | grep -o '"output_tokens":[[:space:]]*[0-9]\+' | grep -o '[0-9]\+' | head -1 2>/dev/null || echo "0")
            local last_cache_creation=$(sed -n "${last_assistant_line}p" "$transcript" | grep -o '"cache_creation_input_tokens":[[:space:]]*[0-9]\+' | grep -o '[0-9]\+' | head -1 2>/dev/null || echo "0")
            local last_cache_read=$(sed -n "${last_assistant_line}p" "$transcript" | grep -o '"cache_read_input_tokens":[[:space:]]*[0-9]\+' | grep -o '[0-9]\+' | head -1 2>/dev/null || echo "0")
            
            tokens_used=$((last_input + last_output + last_cache_creation + last_cache_read))
        fi
    fi
    
    # Debug output
    echo "DEBUG: input=$input_total output=$output_total cache_creation=$cache_creation_total cache_read=$cache_read_total total=$tokens_used" >> /tmp/claude-debug.log
    
    # Format output
    if [ "$tokens_used" -gt 0 ]; then
        echo "${tokens_used}/${token_limit}"
    else
        echo "--/${token_limit}"
    fi
}

# Get token usage from transcript
token_info=$(get_token_usage "$transcript_path")

# Debug log the token extraction result
echo "DEBUG: extracted token_info='$token_info' from transcript='$transcript_path'" >> /tmp/claude-debug.log

# Change to the working directory to get git info
cd "$cwd" 2>/dev/null || cd /workspace

# Get git branch and last commit info
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
    last_commit_date=$(git log -1 --format="%cd" --date=format:"%m/%d %H:%M" 2>/dev/null || echo "no commits")
    git_info="git:$branch | last commit:$last_commit_date"
else
    git_info="git:not a repo"
fi

# Get terminal width for right alignment
term_width=$(tput cols 2>/dev/null || echo 80)

# Right side info (model and tokens)
right_info="model:$model | tokens:$token_info"

# Calculate spaces needed for right alignment
left_length=${#git_info}
right_length=${#right_info}
spaces_needed=$((term_width - left_length - right_length))

# Ensure we have at least 1 space
if [ $spaces_needed -lt 1 ]; then
    spaces_needed=1
fi

# Create the spacing
spaces=$(printf "%*s" $spaces_needed "")

# Output the formatted status line
printf "%s%s%s" "$git_info" "$spaces" "$right_info"