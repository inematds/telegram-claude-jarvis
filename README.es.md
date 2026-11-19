# Tu Jarvis en Telegram

[![Tu Jarvis en Telegram](guia/assets/banner-es.jpg)](https://inematds.github.io/telegram-claude-jarvis/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Aquí tienes dos formas de conversar por Telegram con una IA que trabaja en tu servidor. La primera es el **control remoto de Claude Code**: un bot verifica que seas tú y reenvía la solicitud a Claude Code, que responde o la ejecuta. La segunda es **Jarvis do Intelecto**: un asistente con identidad, memoria, reglas y un mecanismo de seguridad, que usa la IA como cerebro y puede cambiar de cerebro. Está pensado para quienes quieren enviar tareas desde el celular sin abrir la computadora. El proyecto incluye demostraciones reales, piezas animadas y videos.

## 📖 Guía de uso

Guía completa (página de presentación + paso a paso): **https://inematds.github.io/telegram-claude-jarvis/guia/es/**

## Cómo empezar (sin instalar nada a mano)

Abre Claude Code o Codex en la computadora donde trabajará la IA y pega:

```text
Lee el proyecto "Tu Jarvis en Telegram" en https://github.com/inematds/telegram-claude-jarvis (el README lo explica todo, incluida la instalación).
Quiero conversar por Telegram con una IA que trabaja en esta computadora.
Respóndeme en español sencillo:
1. ¿Cuál de las dos opciones tiene sentido para mí ahora: el control remoto de Claude Code o Jarvis do Intelecto? ¿Por qué?
2. ¿Qué necesito tener (bot de Telegram, mi número de usuario, dónde está la IA) y dónde guardar el token de forma segura?
3. ¿Qué solicitudes se ejecutarán directamente y cuáles me pedirán confirmación antes?
No instales ni cambies nada todavía. Muéstrame el plan y espera a que diga que sí.
```

## Las dos opciones

| | Opción 1 · control remoto | Opción 2 · Jarvis do Intelecto |
|---|---|---|
| Flujo | Telegram → bot → Claude Code → respuesta | Telegram → Intelecto (8 piezas) → cerebro y herramientas → respuesta |
| Quién piensa | Claude Code | el cerebro elegido (local, en la nube o de prueba) |
| Memoria e identidad | las del agente | capa propia: SOUL, AGENTS, USER, MEMORY + memoria SQLite |
| Seguridad | lista de usuarios + «¿Confirmas?» antes de borrar, pagar o enviar | mecanismo de seguridad (leer pasa, cambiar pide OK, acciones destructivas rechazadas), cofre, auditoría y caja Docker sin red |
| Ideal para | empezar rápido | evolucionar hacia un asistente personal |

---

## Instalación técnica

### Requisitos previos

- Python 3.10+ y Node 18+ (Playwright, solo para grabar las demostraciones).
- **Opción 1:** Claude Code instalado e iniciado con la suscripción (`claude -p` funcionando).
- **Opción 2:** Intelecto v2 descargado ([https://github.com/inematds/intelecto-v2](https://github.com/inematds/intelecto-v2)) (`git clone https://github.com/inematds/intelecto-v2 ~/projetos/intelecto-v2`; en otro lugar → variable `INTELECTO_V2`) y Docker con la imagen `python:3.12-slim` (`docker pull python:3.12-slim`), que es la «caja».

### Archivos

| Ruta | Qué es |
|---|---|
| `ponte-opcao1/server.py` + `chat.html` | Puente de la Opción 1: pantalla al estilo de Telegram → verifica al usuario → `claude -p` (stream-json) con herramientas limitadas y la regla «¿Confirmas?». Solo en 127.0.0.1. |
| `ponte-opcao1/preparar-sandbox.sh` | Crea la carpeta de prueba (12 registros antiguos + 9 recientes) donde trabaja Claude. |
| `ponte-opcao2/server.py` + `chat.html` | Puente de la Opción 2: pantalla al estilo de Telegram → Intelecto v2 real con cerebro `mock`; cada pieza avisa cuando actúa y la pantalla ilumina esa pieza. Aprobación mediante el botón del chat. |
| `pecas/opcao1-telegram.html` | Pieza animada de la Opción 1 (3 casos, sin biblioteca). `?roteiro=1` desactiva el ciclo y expone `window.cena()`. |
| `pecas/opcao2-jarvis.html` | Pieza animada de la Opción 2 (8 piezas con «por qué» y «cómo»). |
| `filmes/opcao1`, `filmes/opcao2` | Películas HyperFrames 0.8.77 + GSAP; `tpl/` tiene los moldes con tiempos `{{var}}` y `spec.json` contiene las anclas de la narración. |
| `ferramentas/` | Captura cuadro a cuadro, grabación de las páginas, montaje sincronizado con la narración y composición con el avatar. |

### Ejecutar las demostraciones

```bash
# Opção 1 — Claude Code de verdade (assinatura)
cd ponte-opcao1 && ./preparar-sandbox.sh && python3 server.py 8794
# abra http://127.0.0.1:8794 e pergunte: "Quanto espaço livre tem no disco do servidor?"

# Opção 2 — Intelecto v2 com cérebro de teste
cd ponte-opcao2 && INTELECTO_V2=~/projetos/intelecto-v2 python3 server.py 8798   # o servidor é este arquivo; não precisa instalar o intelecto com pip
# abra http://127.0.0.1:8798 e mande: "lembre que o meu servidor de backup se chama Atlas", "rode: df -h /", "rode: rm -r logs"
```

Conectarse a Telegram de verdad:
- **Opción 2:** Intelecto ya tiene el canal (`python3 -m intelecto telegram`, con el token en el cofre y tu ID en `telegram_donos`).
- **Opción 1:** falta el adaptador del bot (recibir el mensaje por Telegram, verificar el ID y llamar a la misma función `chama_claude` del puente). Es el siguiente paso.

### El proceso, de principio a fin

| # | Paso | Comando | Quién lo hace |
|---|---|---|---|
| 1 | Diálogos de los 6 videos (llamada D20, una línea, sin «IAs») | `falas/*.txt` | 🧠 sesión con Nei |
| 2 | Avatar en el estudio HeyGen (con la suscripción) | `node explicavideos/engine/heygen-studio.mjs --titulo tcj-<id> --fala-arquivo <txt> --template TEMPLATE-AVATAR16` | ⚙️ script |
| 3 | Descargar el avatar (API de lectura) | `node explicavideos/engine/heygen-estudio-baixar.mjs --id <id> --saida <mp4>` | ⚙️ script |
| 4 | Tiempo de cada palabra de la narración | Whisper local (inemavox) → `palavras.json` | ⚙️ script |
| 5 | Demostraciones reales cuadro a cuadro | `node ferramentas/capturar-real.cjs <porta> a\|b <pasta>` | ⚙️ script (la respuesta viene de 🤖 `claude -p` en la Opción 1) |
| 6 | Demostraciones reales sincronizadas con la narración | `python3 ferramentas/stopmotion.py <quadros> <spec> <palavras> <dur> <capa> <cta> <saida>` | ⚙️ script |
| 7 | Piezas animadas sincronizadas con la narración | `node ferramentas/gravar-pagina.cjs <pagina> <roteiro.json> <saida>` | ⚙️ script |
| 8 | Películas sincronizadas con la narración | `python3 ferramentas/filme.py filmes/opcaoN spec.json <palavras> <dur>` + `npx hyperframes@0.8.77 check` + `render` | ⚙️ script |
| 9 | Combinar avatar (media pantalla → esquina), voz y música | `python3 ferramentas/compor.py <visual> <avatar> <t_meia> dir\|esq <saida>` | ⚙️ script |
| 10 | Revisión independiente de la guía y los videos | revisor nuevo según el runbook | 🤖 revisor |
| 11 | Guía en Pages, portal, tema en INEMA.VIBE y videos en lives3 (1 h entre ellos) | `git push`, `atualiza-portal`, `postar-telegram`, fila do yt-pub-x3 | 🧠 sesión con Nei |

### Límites conocidos

- La demostración de la Opción 1 usa una pantalla local al estilo de Telegram, no Telegram.
- El cerebro de la demostración de la Opción 2 es `mock` (no razona; sigue un guion fijo). Las otras 7 piezas son reales.
- En una de las 3 grabaciones de la Opción 1, Claude contó 4,8 MB (base decimal) en vez de 4,6 MB; el video usa la grabación que coincide con la narración.

## Licencia

MIT. Gratis en [inema.club](https://inema.club), directamente en internet.