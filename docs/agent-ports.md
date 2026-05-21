# Agent Default Ports

This document tracks the default ports used by various agent systems and services within the repository to avoid conflicts.

## Active Agents & Services

| Agent/Service | Default Port(s) | Description / Protocol |
|---------------|-----------------|------------------------|
| **OpenFang** | `4200` | OpenFang daemon API (HTTP) |
| **Moltis** | `13131` | Moltis agent server (HTTP) |
| **PicoClaw** | `18790`, `18800` | Gateway (HTTP/Webhook) & Launcher Web UI |
| **NanoBot** | `8790` | NanoBot Gateway API |
| **Hermes** | `8000` | Hermes Messaging Gateway (typical, check config) |
| **ZeroClaw** | `42617` | ZeroClaw Gateway |
| **NanoClaw** | `3000` | Webhook Server |
| **Signal-CLI** | `50887`, `50888`, `50889` | TCP JSON-RPC, HTTP JSON-RPC, REST API |
| **Local-Inference** | `50080` | Llama-server local instance |

> [!NOTE]
> When integrating new agents, consult this list to ensure their configured `PORT` or `WEBHOOK_PORT` does not overlap with existing infrastructure.
