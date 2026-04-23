# Gamma MCP Server (custom)

Bold's custom MCP server for the Gamma API. Exposes **all** Gamma API endpoints, including `from-template` remix which is **absent** from Gamma's official MCP server (`mcp.gamma.app/mcp`).

## Why custom, not the official Gamma connector

Gamma ships a first-party Claude Connector (Settings → Connectors → Browse → Gamma). It exposes only 3 tools: `generate`, `get_themes`, `get_folders`. Missing capabilities critical for Bold's flow:

- **`generate_from_template`**, the remix endpoint. Used to replay a winning deck (e.g. Phoenix 2025 art event) as the scaffold for the next pitch (e.g. Keren 2026 launch), keeping layout and visual system while swapping content. The single most valuable endpoint for Bold's repeat-client pattern.
- **Manual status polling**, `get_generation` by ID. Critical for long runs (30+ cards) where the default poll window isn't enough.
- **Per-call control** over poll interval and timeout, via a `wait: true/false` flag and tunable `pollIntervalMs` + `pollTimeoutMs`.
- **Pagination** on theme and folder listings via `after` / `nextCursor`.

## Source of truth

Code lives in a separate repo, single source of truth:
**https://github.com/hemichaeli/gamma-mcp-server**

This folder in `bold-proposal-skills` documents how Bold uses the server. The TypeScript source is not mirrored here to avoid drift.

## Tools exposed (5)

| Tool | Purpose |
|---|---|
| `gamma_generate` | Create presentation / document / webpage / social post. `wait: true` polls to completion and returns the final `gammaUrl` (+ optional `exportUrl` for pptx/pdf/png). |
| `gamma_generate_from_template` | Remix an existing single-page Gamma with new content. Keeps layout, theme, visuals; swaps text and imagery. |
| `gamma_get_generation` | Poll generation status by ID. |
| `gamma_list_themes` | List workspace themes with optional name filter and pagination. |
| `gamma_list_folders` | List workspace folders with optional name filter and pagination. |

All five return structured text with `generationId`, `status`, `gammaUrl`, `exportUrl`, and credit usage where relevant.

## Deploy (one-time)

1. Clone or fork `hemichaeli/gamma-mcp-server`.
2. Railway → New → Deploy from GitHub repo → select it.
3. Variables tab, add: `GAMMA_API_KEY` = key from https://gamma.app/settings/api-keys (requires Gamma Pro, Ultra, Teams, or Business).
4. Settings → Networking → Generate Domain.
5. Endpoint: `https://<your-service>.up.railway.app/sse`
6. Claude.ai → Settings → Connectors → Add custom connector. Name "Gamma (Bold)", URL from step 5.

## How `bold-proposal-builder` uses it

### Stage 6 (Assembly), deck generation

The `bold-proposal-builder` skill's Stage 6 currently generates the client deck via `premium-deck-strategist`. With this MCP connected, Stage 6 can additionally (or instead) produce a native Gamma deck in one call:

```
gamma_generate(
  inputText: <structured outline built from brand-system.md + agenda.md + mockup captions>,
  format: "presentation",
  numCards: 16,
  themeId: <resolved from gamma_list_themes by brand-heart keywords>,
  folderIds: [<Bold-Proposals folder ID>],
  cardOptions: { dimensions: "16x9" },
  textOptions: { language: "he", tone: "editorial", audience: "decision-maker" },
  imageOptions: { source: "aiGenerated", style: <from brand-system.md>},
  exportAs: "pdf",
  wait: true
)
```

Returns a live Gamma URL the client can view and comment on, plus a PDF export for archival. No manual Import step.

### Stage 7 (Debrief), remixing into the next pitch

When a new event begins for a returning client, Stage 1 of the next proposal can pull the previous successful deck's `gammaId` from the client profile and use:

```
gamma_generate_from_template(
  gammaId: <previous deck ID>,
  prompt: <new event's brief + brand-heart>,
  themeId: <same or new>,
  wait: true
)
```

This is the capability the official Gamma connector does not have and the reason this custom MCP exists.

## Environment expectations

| Variable | Required | Set in |
|---|---|---|
| `GAMMA_API_KEY` | yes | Railway variables, never in chat or repo |
| `PORT` | no | Railway sets automatically |

## Troubleshooting

- `401 Unauthorized` in tool calls: `GAMMA_API_KEY` missing or invalid in Railway. Regenerate at gamma.app/settings/api-keys, paste into Railway Variables.
- `402 Insufficient credits`: upgrade plan or top up credits.
- Tool calls hang: `numCards` above 30 with the default 10-minute timeout may need `pollTimeoutMs: 1800000` (30 min) passed explicitly.
- Tool doesn't appear in Claude: restart the chat. Custom connectors register at session start.

## Versioning

Bumping the MCP server: push changes to the `gamma-mcp-server` repo, Railway auto-redeploys on push to main. No action needed here.

## Related

- [`bold-proposal-builder`](../../src/bold-proposal-builder/) uses this MCP in Stages 6 and 7.
- [`premium-deck-strategist`](../../../) (separate skill) remains the fallback deck builder when Gamma is unavailable.
