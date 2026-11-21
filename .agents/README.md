# AI 팀 브리지 (Claude · Codex · Gemini)

`team-bridge.mjs`는 의존성 없는 MCP 서버입니다. 에이전트끼리 서로 일을 넘길 수 있게 해 줍니다.

| 호출하는 쪽 | 쓸 수 있는 도구 | 등록 위치 |
|---|---|---|
| Claude Code | `ask_codex`, `ask_gemini` | `.mcp.json` |
| Codex CLI | `ask_gemini` | `~/.codex/config.toml` (`codex mcp add team ...`) |
| Gemini CLI | `ask_codex` | `~/.gemini/settings.json` (`gemini mcp add -s user team ...`) |

- 위임 깊이 제한: `TEAM_MAX_DEPTH` (기본 2). 무한으로 서로 넘기는 것을 막습니다.
- 작업 로그: `.agents/logs/team.log`
- 키는 코드에 넣지 않습니다. 클라우드 환경의 네트워크 비밀값으로 저장하면 프록시가 요청에 넣어 줍니다.
