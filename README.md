# Seu Jarvis no Telegram

[![Seu Jarvis no Telegram](guia/assets/banner.jpg)](https://inematds.github.io/telegram-claude-jarvis/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Aqui você vê dois jeitos de conversar pelo Telegram com uma IA que trabalha no seu servidor. O primeiro é o **controle remoto do Claude Code**: um bot confere se é você e repassa o pedido ao Claude Code, que responde ou executa. O segundo é o **Jarvis do Intelecto**: um assistente com identidade, memória, regras e trava, que usa a IA como cérebro e pode trocar de cérebro. Serve para quem quer mandar tarefas pelo celular sem abrir o computador. O projeto traz as demonstrações reais, as peças animadas e os vídeos.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/telegram-claude-jarvis/guia/**

## Como começar (sem instalar nada à mão)

Abra o Claude Code ou o Codex no computador onde a IA vai trabalhar e cole:

```text
Leia o projeto "Seu Jarvis no Telegram" em https://github.com/inematds/telegram-claude-jarvis (o README explica tudo, inclusive a instalação).
Quero conversar pelo Telegram com uma IA que trabalha neste computador.
Me responda em português simples:
1. Qual das duas opções faz sentido para mim agora: o controle remoto do Claude Code ou o Jarvis do Intelecto? Por quê?
2. O que eu preciso ter (bot do Telegram, meu número de usuário, onde fica a IA) e onde guardar o token com segurança.
3. Quais pedidos vão rodar direto e quais vão me pedir confirmação antes.
Não instale nem mude nada ainda. Mostre o plano e espere eu dizer sim.
```

## As duas opções

| | Opção 1 · controle remoto | Opção 2 · Jarvis do Intelecto |
|---|---|---|
| Fluxo | Telegram → bot → Claude Code → resposta | Telegram → Intelecto (8 peças) → cérebro e ferramentas → resposta |
| Quem pensa | Claude Code | o cérebro escolhido (local, nuvem ou de teste) |
| Memória e identidade | as do agente | camada própria: SOUL, AGENTS, USER, MEMORY + memória SQLite |
| Segurança | lista de usuários + "Confirma?" antes de apagar, pagar ou enviar | trava (lê passa, muda pede OK, destrutivo recusado), cofre, auditoria e caixa Docker sem rede |
| Melhor para | começar rápido | evoluir para um assistente pessoal |

---

## Instalação técnica

### Pré-requisitos

- Python 3.10+ e Node 18+ (Playwright, só para gravar as demonstrações).
- **Opção 1:** Claude Code instalado e logado pela assinatura (`claude -p` funcionando).
- **Opção 2:** o [Intelecto v2](https://github.com/inematds/intelecto-v2) baixado (`git clone https://github.com/inematds/intelecto-v2 ~/projetos/intelecto-v2`; outro lugar → variável `INTELECTO_V2`) e Docker com a imagem `python:3.12-slim` (`docker pull python:3.12-slim`), que é a "caixa".

### Arquivos

| Caminho | O que é |
|---|---|
| `ponte-opcao1/server.py` + `chat.html` | Ponte da Opção 1: tela estilo Telegram → confere o usuário → `claude -p` (stream-json) com ferramentas limitadas e a regra do "Confirma?". Só em 127.0.0.1. |
| `ponte-opcao1/preparar-sandbox.sh` | Cria a pasta de teste (12 logs antigos + 9 recentes) onde o Claude trabalha. |
| `ponte-opcao2/server.py` + `chat.html` | Ponte da Opção 2: tela estilo Telegram → Intelecto v2 de verdade com cérebro `mock`; cada peça avisa quando age e a tela acende a peça. Aprovação pelo botão no chat. |
| `pecas/opcao1-telegram.html` | Peça animada da Opção 1 (3 casos, sem biblioteca). `?roteiro=1` desliga o ciclo e expõe `window.cena()`. |
| `pecas/opcao2-jarvis.html` | Peça animada da Opção 2 (8 peças com "por quê" e "como"). |
| `filmes/opcao1`, `filmes/opcao2` | Filmes HyperFrames 0.8.77 + GSAP; `tpl/` tem os moldes com tempos `{{var}}` e `spec.json` as âncoras da fala. |
| `ferramentas/` | Captura quadro a quadro, gravação das páginas, montagem no tempo da fala e composição com o avatar. |

### Rodar as demonstrações

```bash
git clone https://github.com/inematds/telegram-claude-jarvis && cd telegram-claude-jarvis

# Opção 1 — Claude Code de verdade (assinatura)
(cd ponte-opcao1 && ./preparar-sandbox.sh && python3 server.py 8794)
# abra http://127.0.0.1:8794 e pergunte: "Quanto espaço livre tem no disco do servidor?"

# Opção 2 — Intelecto v2 com cérebro de teste
(cd ponte-opcao2 && INTELECTO_V2=~/projetos/intelecto-v2 python3 server.py 8798)   # em outro terminal; não precisa instalar o intelecto com pip
# abra http://127.0.0.1:8798 e mande: "lembre que o meu servidor de backup se chama Atlas", "rode: df -h /", "rode: rm -r logs"
```

Ligar no Telegram de verdade:
- **Opção 2:** o Intelecto já tem o canal (`python3 -m intelecto telegram`, com o token no cofre e o seu id em `telegram_donos`).
- **Opção 1:** falta o adaptador do bot (receber a mensagem pelo Telegram, conferir o id e chamar a mesma função `chama_claude` da ponte). É o próximo passo.

### O processo, do início ao fim

| # | Passo | Comando | Quem faz |
|---|---|---|---|
| 1 | Falas dos 6 vídeos (chamada D20, uma linha, sem "IAs") | `falas/*.txt` | 🧠 sessão com o Nei |
| 2 | Avatar no estúdio HeyGen (pela assinatura) | `node explicavideos/engine/heygen-studio.mjs --titulo tcj-<id> --fala-arquivo <txt> --template TEMPLATE-AVATAR16` | ⚙️ script |
| 3 | Baixar o avatar (API de leitura) | `node explicavideos/engine/heygen-estudio-baixar.mjs --id <id> --saida <mp4>` | ⚙️ script |
| 4 | Tempo de cada palavra da fala | Whisper local (inemavox) → `palavras.json` | ⚙️ script |
| 5 | Demos reais quadro a quadro | `node ferramentas/capturar-real.cjs <porta> a\|b <pasta>` | ⚙️ script (a resposta vem do 🤖 `claude -p` na Opção 1) |
| 6 | Demos reais no tempo da fala | `python3 ferramentas/stopmotion.py <quadros> <spec> <palavras> <dur> <capa> <cta> <saida>` | ⚙️ script |
| 7 | Peças animadas no tempo da fala | `node ferramentas/gravar-pagina.cjs <pagina> <roteiro.json> <saida>` | ⚙️ script |
| 8 | Filmes no tempo da fala | `python3 ferramentas/filme.py filmes/opcaoN spec.json <palavras> <dur>` + `npx hyperframes@0.8.77 check` + `render` | ⚙️ script |
| 9 | Juntar avatar (meia tela → canto), voz e trilha | `python3 ferramentas/compor.py <visual> <avatar> <t_meia> dir\|esq <saida>` | ⚙️ script |
| 10 | Revisão independente do guia e dos vídeos | revisor novo pelo runbook | 🤖 revisor |
| 11 | Guia no Pages, portal, tópico no INEMA.VIBE e vídeos no lives3 (1 h entre eles) | `git push`, `atualiza-portal`, `postar-telegram`, fila do yt-pub-x3 | 🧠 sessão com o Nei |

### Limites conhecidos

- A demonstração da Opção 1 usa uma tela local no estilo do Telegram, não o Telegram.
- O cérebro da demonstração da Opção 2 é o `mock` (não raciocina; segue um roteiro fixo). As outras 7 peças são as reais.
- Numa das 3 gravações da Opção 1, o Claude contou 4,8 MB (base decimal) em vez de 4,6 MB; o vídeo usa a gravação que bate com a narração.

## Licença

MIT. Grátis no [inema.club](https://inema.club), direto na internet.
