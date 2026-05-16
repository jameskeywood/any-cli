# any-cli

CLI for a multitude of LLM providers.

Focusing on those with free API access.

Currently implemented:
- Gemini
- Groq (slightly buggy)

## Usage

Add required API keys to a `.env` file:
```
GEMINI_API_KEY=<gemini_api_key>
GROQ_API_KEY=<groq_api_key>
```

Execute the following:
```
python src/any-cli/main.py --provider <provider> --model <model>
```

## Sources

- Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling
- Groq tool calling: https://console.groq.com/docs/tool-use/local-tool-calling

## TODO

- Ensure client specific logic is fully encapsulated
- Global rate limit in .env
- Switch between sessions, requires session manager and UI improvement
- Add Nix build, and UV support
- /cwd command
- New file / update file tools
