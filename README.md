# any-cli

CLI for a multitude of LLM providers.

Focusing on those with free API access.

Currently implemented:
- Gemini
- Groq

## Sources

Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling
Groq tool calling: https://console.groq.com/docs/tool-use/local-tool-calling

## TODO

- Ensure client specific logic is fully encapsulated
- Global rate limit in .env
- Switch between sessions, requires session manager and UI improvement
- Add Nix packaging, and UV support
