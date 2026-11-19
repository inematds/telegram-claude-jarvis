# Your Jarvis on Telegram

[![Your Jarvis on Telegram](guia/assets/banner-en.jpg)](https://inematds.github.io/telegram-claude-jarvis/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Here you can see two ways to chat on Telegram with an AI that works on your server. The first is **Claude Code remote control**: a bot checks that it’s you and forwards your request to Claude Code, which responds or carries it out. The second is **Intelecto’s Jarvis**: an assistant with an identity, memory, rules, and a safety lock, which uses AI as its brain and can switch brains. It’s for anyone who wants to send tasks from their phone without opening a computer. The project includes real demonstrations, animated components, and videos.

## 📖 Usage guide

Complete guide (landing page + walkthrough): **https://inematds.github.io/telegram-claude-jarvis/guia/en/**

## How to get started (without installing anything by hand)

Open Claude Code or Codex on the computer where the AI will work, then paste:

```text
Read the "Your Jarvis on Telegram" project at https://github.com/inematds/telegram-claude-jarvis (the README explains everything, including installation).
I want to chat on Telegram with an AI that works on this computer.
Answer me in simple English:
1. Which of the two options makes sense for me right now: Claude Code remote control or Intelecto’s Jarvis? Why?
2. What do I need (a Telegram bot, my user ID, where the AI is) and where should I securely store the token?
3. Which requests will run directly, and which will ask me for confirmation first?
Don’t install or change anything yet. Show me the plan and wait for me to say yes.
```

## The two options

| | Option 1 · remote control | Option 2 · Intelecto’s Jarvis |
|---|---|---|
| Flow | Telegram → bot → Claude Code → response | Telegram → Intelecto (8 pieces) → brain and tools → response |
| Who thinks | Claude Code | the selected brain (local, cloud, or for testing) |
| Memory and identity | the agent’s own | its own layer: SOUL, AGENTS, USER, MEMORY + SQLite memory |
| Security | user list + “Confirm?” before deleting, paying, or sending | safety lock (reading is allowed, changes ask for OK, destructive actions are refused), vault, audit, and Docker box without network access |
| Best for | getting started quickly | growing into a personal assistant |

---

## Technical setup

### Prerequisites

- Python 3.10+ and Node 18+ (Playwright, only for recording the demonstrations).
- **Option 1:** Claude Code installed and logged in through the subscription (`claude -p` working).
- **Option 2:** [Intelecto v2](https://github.com/inematds/intelecto-v2) downloaded (`git clone https://github.com/inematds/intelecto-v2 ~/projetos/intelecto-v2`; elsewhere → variable `INTELECTO_V2`) and Docker with the `python:3.12-slim` image (`docker pull python:3.12-slim`), which is the “box.”

### Files

| Path | What it is |
|---|---|
| `ponte-opcao1/server.py` + `chat.html` | Option 1 bridge: Telegram-style screen → checks the user → `claude -p` (stream-json) with limited tools and the “Confirm?” rule. Only on 127.0.0.1. |
| `ponte-opcao1/preparar-sandbox.sh` | Creates the test folder (12 old logs + 9 recent ones) where Claude works. |
| `ponte-opcao2/server.py` + `chat.html` | Option 2 bridge: Telegram-style screen → actual Intelecto v2 with a `mock` brain; each piece reports when it acts, and the screen lights up that piece. Approval via the button in chat. |
| `pecas/opcao1-telegram.html` | Animated component for Option 1 (3 cases, no library). `?roteiro=1` disables the cycle and exposes `window.cena()`. |
| `pecas/opcao2-jarvis.html` | Animated component for Option 2 (8 pieces with “why” and “how”). |
| `filmes/opcao1`, `filmes/opcao2` | HyperFrames 0.8.77 + GSAP films; `tpl/` contains templates with `{{var}}` timings, and `spec.json` contains the speech cues. |
| `ferramentas/` | Frame-by-frame capture, page recording, timing to match the speech, and composition with the avatar. |

### Run the demonstrations

```bash
# Option 1 — actual Claude Code (subscription)
cd ponte-opcao1 && ./preparar-sandbox.sh && python3 server.py 8794
# open http://127.0.0.1:8794 and ask: "How much free space is on the server's disk?"

# Option 2 — Intelecto v2 with a test brain
cd ponte-opcao2 && INTELECTO_V2=~/projetos/intelecto-v2 python3 server.py 8798   # this file is the server; you don't need to install Intelecto with pip
# open http://127.0.0.1:8798 and send: "remember that my backup server is called Atlas", "run: df -h /", "run: rm -r logs"
```

Connect to Telegram for real:
- **Option 2:** Intelecto already has the channel (`python3 -m intelecto telegram`, with the token in the vault and your ID in `telegram_donos`).
- **Option 1:** the bot adapter is still missing (receive the Telegram message, check the ID, and call the same `chama_claude` function as the bridge). This is the next step.

### The process, from beginning to end

| # | Step | Command | Who does it |
|---|---|---|---|
| 1 | Lines for the 6 videos (D20 hook, one line, no “AIs”) | `falas/*.txt` | 🧠 session with Nei |
| 2 | Avatar in the HeyGen Studio (subscription) | `node explicavideos/engine/heygen-studio.mjs --titulo tcj-<id> --fala-arquivo <txt> --template TEMPLATE-AVATAR16` | ⚙️ script |
| 3 | Download the avatar (read-only API) | `node explicavideos/engine/heygen-estudio-baixar.mjs --id <id> --saida <mp4>` | ⚙️ script |
| 4 | Timing for each word in the speech | Local Whisper (inemavox) → `palavras.json` | ⚙️ script |
| 5 | Real demos, frame by frame | `node ferramentas/capturar-real.cjs <porta> a\|b <pasta>` | ⚙️ script (the response comes from 🤖 `claude -p` in Option 1) |
| 6 | Real demos timed to the speech | `python3 ferramentas/stopmotion.py <quadros> <spec> <palavras> <dur> <capa> <cta> <saida>` | ⚙️ script |
| 7 | Animated components timed to the speech | `node ferramentas/gravar-pagina.cjs <pagina> <roteiro.json> <saida>` | ⚙️ script |
| 8 | Films timed to the speech | `python3 ferramentas/filme.py filmes/opcaoN spec.json <palavras> <dur>` + `npx hyperframes@0.8.77 check` + `render` | ⚙️ script |
| 9 | Combine avatar (half-screen → corner), voice, and soundtrack | `python3 ferramentas/compor.py <visual> <avatar> <t_meia> dir\|esq <saida>` | ⚙️ script |
| 10 | Independent review of the guide and videos | new reviewer via runbook | 🤖 reviewer |
| 11 | Guide on Pages, portal, topic on INEMA.VIBE, and videos on lives3 (1 hour apart) | `git push`, `atualiza-portal`, `postar-telegram`, yt-pub-x3 queue | 🧠 session with Nei |

### Known limitations

- The Option 1 demonstration uses a local Telegram-style screen, not Telegram itself.
- The brain in the Option 2 demonstration is `mock` (it doesn’t reason; it follows a fixed script). The other 7 pieces are real.
- In one of the 3 Option 1 recordings, Claude reported 4.8 MB (decimal) instead of 4.6 MB; the video uses the recording that matches the narration.

## License

MIT. Free on [inema.club](https://inema.club), directly on the internet.