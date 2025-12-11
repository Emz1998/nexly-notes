Create a hook that will intercept subagent invocations through PreToolUse hook event via "Task" tool. Parse the subagent "prompt" and "subagent_type" from hook_input and store it in a variable. Send a json output with "additionalContext" (hookSpecificOutput) to the stdout with this instruction:

_Variables:_

INITIAL_AGENT: `subagent_type` from hook_input
INITIAL_PROMPT: `prompt` from hook_input

```
Call the agent-prompt-engineer to review and refine the following prompt:

<subagent_prompt> {INITIAL_PROMPT} </subagent_prompt>

Then,call the agent-prompt-reviewer to rate the refined prompt. If the rating is less than 9, re-invoke the agent-prompt-engineer. Keep iterating until the rating is 9

Iteration Flow:

agent-prompt-engineer -> refine the prompt -> agent-prompt-reviewer -> rate the prompt -> agent-prompt-engineer if rating is less than 10

Once quality check passsed, re-prompt the {INITIAL_AGENT} agent with the refined prompt


```
