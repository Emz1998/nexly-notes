# Command Documentation Template

## Command Name
`/command-name`

## Purpose
*Brief description of what this command does and when to use it*

## Category
*One of: Meta, Development, Research, Planning, Testing, DevOps, Quality*

## Synopsis
```
/command-name [required-arg] [--optional-flag] [--option=value]
```

## Description
*Detailed explanation of the command's functionality and behavior*

## Arguments

### Required Arguments
- **`arg1`**: Description of first required argument
- **`arg2`**: Description of second required argument

### Optional Arguments
- **`--flag1`**: Description of optional flag
- **`--option=value`**: Description with default value

## Options
- **`--verbose`**: Enable detailed output
- **`--dry-run`**: Preview changes without applying
- **`--format=[json|text|markdown]`**: Output format (default: markdown)

## Usage Examples

### Basic Usage
```
/command-name basic-arg
```
*What this does*

### Advanced Usage
```
/command-name arg1 arg2 --flag --option=value
```
*What this does*

### Complex Scenario
```
/command-name "complex arg" --multiple --flags --option="with spaces"
```
*What this does*

## Output Format
*Description of what the command outputs*

### Sample Output
```
Expected output format here
```

## Workflow Integration

### Prerequisites
- Required setup or dependencies
- Environment requirements
- Permission requirements

### Related Commands
- `/related-command1`: How it relates
- `/related-command2`: How it relates

### Next Steps
1. Typical follow-up action
2. Common next command
3. Verification steps

## Error Handling

### Common Errors
- **Error 1**: Description and resolution
- **Error 2**: Description and resolution

### Validation Rules
- Rule 1: What gets validated
- Rule 2: Input constraints

## Performance Notes
- Expected execution time
- Resource usage
- Concurrency limitations

## Security Considerations
- Permission requirements
- Data handling
- Compliance notes (FERPA/HIPAA if applicable)

## Implementation Details

### Tools Used
- Primary tool: Purpose
- Secondary tool: Purpose

### File Operations
- Read: What files are read
- Write: What files are created/modified
- Delete: What might be removed

### Agent Involvement
*If applicable, which agents are used*

## Best Practices
1. When to use this command
2. When NOT to use this command
3. Performance optimization tips

## Limitations
- Known limitations
- Edge cases not handled
- Maximum input sizes

## Version History
- **v1.0**: Initial implementation
- **v1.1**: Added feature X
- **v1.2**: Fixed issue Y

## Configuration
*If command uses configuration files*
```json
{
  "setting1": "default",
  "setting2": true
}
```

## Notes
*Additional implementation notes or warnings*

## Examples in Context

### Scenario 1: Development Workflow
```bash
/command-name development-specific-args
```

### Scenario 2: Production Use
```bash
/command-name production-safe-args --dry-run
```

## Troubleshooting

### Issue: Command not responding
**Solution**: Check prerequisites and permissions

### Issue: Unexpected output
**Solution**: Verify input format and flags

## Metadata
- **Author**: Agent/Human who created
- **Created**: Date created
- **Modified**: Last modified date
- **Status**: Active/Deprecated/Beta
- **Complexity**: Low/Medium/High
- **Execution Time**: Fast (<5s)/Medium/Slow (>30s)