#!/bin/bash

# Launch NEW Claude sessions in 4 worktrees
echo "🚀 Launching NEW Claude sessions in 4 worktrees..."

# Kill existing session if it exists
tmux kill-session -t claude 2>/dev/null

# Create new tmux session with 4 windows (custom order)
tmux new-session -d -s claude -n 'Discovery-Strategy' -c '/workspace/worktrees/discovery-strategy' 'claude; exec bash'
tmux new-window -t claude -n 'Development' -c '/workspace/worktrees/development' 'claude; exec bash'
tmux new-window -t claude -n 'DevOps' -c '/workspace/worktrees/devOps' 'claude; exec bash'
tmux new-window -t claude -n 'Launch' -c '/workspace/worktrees/launch' 'claude; exec bash'

# Attach to the session
echo "✅ NEW Claude sessions running in 4 tmux windows!"
echo ""
echo "📋 Quick Commands:"
echo "  Switch windows: Ctrl+B then 0-3"
echo "  Next window:    Ctrl+B then n"
echo "  Previous:       Ctrl+B then p"
echo "  List windows:   Ctrl+B then w"
echo ""
tmux attach -t claude