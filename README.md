- **get_revenue_at_time** — Get revenue up to a specific time on a given date.
# iikoServer MCP Server

MCP (Model Context Protocol) server for [iiko](https://iiko.ru) restaurant management system REST API.

Exposes 39 tools covering products, employees, entities, documents, payments, reports, and raw API access.

## Setup

```bash
cd ~/iiko-mcp
pip install -r requirements.txt
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `IIKO_URL` | No | `https://poidu-poem.iiko.it:443` | iikoServer base URL |
| `IIKO_LOGIN` | Yes | — | Login username |
| `IIKO_PASS` | Yes | — | Plain password (SHA1 computed internally) |

## Usage

```bash
IIKO_URL=https://your-server:443 IIKO_LOGIN=katerina IIKO_PASS=secret python3 server.py
```

The server communicates over stdio using the MCP protocol.

## MCP Client Configuration

### Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
mcp:
  servers:
    iiko:
      command: python3
      args: ["/home/simba87/iiko-mcp/server.py"]
      env:
        IIKO_URL: "https://poidu-poem.iiko.it:443"
        IIKO_LOGIN: "katerina"
        IIKO_PASS: "your-password-here"
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "iiko": {
      "command": "python3",
      "args": ["/home/simba87/iiko-mcp/server.py"],
      "env": {
        "IIKO_URL": "https://poidu-poem.iiko.it:443",
        "IIKO_LOGIN": "katerina",
        "IIKO_PASS": "your-password-here"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "iiko": {
      "command": "python3",
      "args": ["/home/simba87/iiko-mcp/server.py"],
      "env": {
        "IIKO_URL": "https://poidu-poem.iiko.it:443",
        "IIKO_LOGIN": "katerina",
        "IIKO_PASS": "your-password-here"
      }
    }
  }
}
```

## Available Tools (39)

### System
- **ping** — Health check, returns server status and auth state
- **list_endpoints** — List all available endpoints with descriptions

### Products / Nomenclature
- **get_products** — All products
- **get_product_groups** — Product groups/categories
- **get_product_sizes** — Product sizes/units
- **get_nomenclature** — Full nomenclature (alias for get_products)
- **get_corporate_structure** — Corporate departments
- **get_corporate_groups** — Corporate groups
- **search_products** — Search products by name (case-insensitive substring)

### Employees
- **get_employees** — All employees
- **get_employee** — Single employee by UUID
- **get_employee_roles** — Employee roles
- **get_persons** — All persons/users

### Entities
- **get_entity_types** — Available entity types
- **get_entities** — Entities by type
- **get_entity_by_id** — Single entity by type + UUID
- **get_stores** — Stores/warehouses
- **get_contractors** — Contractors/suppliers

### Documents
- **get_incoming_invoices** — Incoming invoices (date range)
- **get_outgoing_invoices** — Outgoing invoices (date range)
- **get_incoming_invoice_by_id** — Single incoming invoice
- **get_outgoing_invoice_by_id** — Single outgoing invoice
- **get_waste_documents** — Waste/write-off documents (date range)
- **get_menu_changes** — Menu change documents
- **get_menu_change_by_id** — Single menu change

### Cash & Payments
- **get_payment_types** — Payment types
- **get_cash_shifts** — Cash shifts
- **get_cash_shift** — Single cash shift by session ID
- **get_payments** — Payments for a session
- **get_payment** — Single payment by session + payment ID
- **create_encashment** — Create cash in/out entry

### Prices
- **get_price_categories** — All price categories
- **get_price_category** — Single price category by ID

### Reports & OLAP
- **get_olap_columns** — OLAP columns for a report type
- **run_olap_report** — Run OLAP report with custom columns/filters
- **get_olap_presets** — Saved OLAP presets
- **run_olap_by_preset** — Run OLAP by preset ID
- **run_custom_report** — Run custom report by name

### Raw
- **raw_request** — Make any authenticated request to iikoServer

## Date Format

All dates use **DD.MM.YYYY** format (iiko convention). Example: `15.01.2025`.

## Features

- Auto-authentication on startup via env vars
- Auto-re-authentication on 401 (token expiry)
- Graceful logout on shutdown (releases license slot)
- Self-signed cert support (`verify=False`)
- Error messages returned as tool results (no crashes)
- SHA1 password hashing computed internally
