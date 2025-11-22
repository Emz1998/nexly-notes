# Troubleshooting Report: Dockerfile .zshrc Generation Issue

## Purpose
Fix persistent parse errors in .zshrc after Docker container rebuilds.

## Issue Summary
- **Error**: Parse errors in .zshrc/bashrc after container rebuild
- **Root Cause**: Dockerfile incorrectly escaping dollar signs in command substitution
- **File**: /workspace/.devcontainer/Dockerfile

## Problems Found
1. Lines 427-428: `\$(...)` in wtinfo function for .zshrc
2. Lines 258-260: `\$(...)` in wtinfo function for .bashrc  
3. Lines 181, 184: `\$(find ...)` in wtr function for .bashrc
4. Line 242: `\$(find ...)` in wtgo function for .bashrc

## Fix Applied
Removed backslashes from command substitution syntax:
- Changed `\$(command)` to `$(command)` in all affected lines
- Fixed both .bashrc and .zshrc generation sections

## Affected Lines Fixed
- Line 181: `path=$(find ...)` 
- Line 184: `path=$(find ...)`
- Line 242: `path=$(find ...)`
- Line 258: `name=$(basename ...)`
- Lines 259-260: `branch=$(...)` and `commit=$(...)`
- Lines 427-428: ZSH versions of branch and commit

## Verification
- Syntax now generates correct shell command substitution
- Next container rebuild will produce valid .zshrc/.bashrc files
- No parse errors expected after rebuild

## Prevention
- Review Dockerfile echo statements for proper escaping
- Test generated shell scripts before container deployment
- Use heredocs for complex shell function generation

---
*Resolved: 2025-09-06*