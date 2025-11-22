# /setup Command Template

## Command
`/setup <environment-type>`

## Purpose
Setup coding environment and install all dependencies

## Output Structure

### Setup Log
**Location**: Console output and logs

```markdown
# Environment Setup Log

## Requirements Found
### From requirements.txt
- Package 1==version
- Package 2==version
- Package 3==version

### From package.json
- "dependency1": "version"
- "dependency2": "version"
- "devDependency1": "version"

## Installation Progress

### Python Dependencies
- [ ] numpy==1.24.0 - Installing...
- [✓] pandas==2.0.0 - Installed
- [✗] scipy==1.10.0 - Failed (retry)

### Node Dependencies
- [✓] react@18.2.0 - Installed
- [✓] typescript@5.0.0 - Installed
- [ ] @shadcn/ui - Installing...

## Verification Results

### Python
```bash
$ python --version
Python 3.11.0

$ pip list
[List of installed packages]
```

### Node
```bash
$ node --version
v18.0.0

$ npm list
[Dependency tree]
```

## Issues Encountered
- **Issue 1**: [Description] - [Resolution]
- **Issue 2**: [Description] - [Resolution]

## Post-Setup Configuration
- Environment variables set
- Config files created
- Git hooks installed

## Status
- **Total Dependencies**: [Count]
- **Successfully Installed**: [Count]
- **Failed**: [Count]
- **Setup Complete**: [Yes/No]
```

## Process Flow
1. Read requirements.txt
2. Read package.json (if exists)
3. Create TODO list with TodoWrite
4. Install Python dependencies
5. Install Node dependencies
6. Verify installations
7. Report results

## Environment Types
- **python**: Python-only setup
- **node**: Node.js-only setup
- **fullstack**: Both Python and Node
- **auto**: Detect from files

## Files Checked
- `requirements.txt`
- `package.json`
- `Pipfile`
- `poetry.lock`
- `yarn.lock`

## Verification Commands
```bash
# Python
python --version
pip list
pip check

# Node
node --version
npm --version
npm list
npm audit
```

## Common Issues
- **Missing Python**: Install Python 3.8+
- **Missing Node**: Install Node.js 16+
- **Permission Errors**: Use sudo or admin
- **Network Issues**: Check proxy settings