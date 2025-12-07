Create a hook that will validate if Slash Commands flow. The initial trigger point will be /implement. This slash command will call the /explore slash command via `SlashCommand` Tool then the /plan then the /research then the /code then the /code-review then the /commit. Flow should look like this:

/implement -> /explore -> /research -> /plan -> /code -> /code-review -> /commit

The hook should validate if the flow is correct and if not, it should return an error message.

The hook should also validate if the slash commands are called in the correct order.
