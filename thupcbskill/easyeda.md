# Connect Codex to EasyEDA Pro

| Editor environment | Interface | First check |
| --- | --- | --- |
| Web editor with the community connector | [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) CLI, daemon, and matching extension | `easyeda health` and the connected project and documents |
| Supported desktop client | Official `lceda-pro` (international edition `easyeda-pro`) or its stdio MCP | `lceda-pro doctor` and `lceda-pro session list` |
| Editor with the official extension gateway | Run API Gateway and its matching local bridge | Extension loaded, external interaction enabled, and target window connected |
| Existing EasyEDA MCP integration | The health, window, API discovery, and editing tools exposed in the current session | Enumerate windows and inspect the capabilities and argument schemas |

Use the current upstream release instructions for the selected interface. Match the connector to its bridge and CLI. On failure, check extension state, permissions, bridge address, handshake, and document identity in that order. Keep the bridge within the local scope needed for the task.

## Community typed CLI

These examples follow the easyeda-agent 1.8 series documentation. Check `--help` and `easyeda actions` on the installed build. Set the project, schematic page, and PCB variables to the IDs returned by the connector. A library device ID, schematic instance ID, and PCB instance ID each serve different purposes.

```powershell
easyeda health
easyeda doc ls --project $project --json
easyeda sch connectivity --all-pages --project $project
easyeda sch list --project $project --doc $sheet --include-pins --include-wires --include-bbox
easyeda pcb dump --project $project --doc $pcb --include-copper --out board-before.json
```

**Schematic.** Use `easyeda lib by-lcsc --help` to find the exact device and verify its symbol, pin numbers, and footprint. Build `apply.json` with the upstream schema. Bind the operation to the intended project and page. Run `easyeda sch apply apply.json --dry-run`, review the actions and targets, then apply with `easyeda sch apply apply.json --yes`. Read back with `sch list` and `sch connectivity`, then run `sch check`, `sch drc`, and `sch save`. Use the target flags supported by the installed version.

**Synchronization.** Verify the board's schematic and PCB pairing. Review the difference between the intended schematic connectivity and the current PCB. Use the native preview when the installed interface exposes it. Check `easyeda pcb import-changes --help` before applying, and use the schematic ID required by the command. Read fresh footprints, pad nets, and unconnected items afterward. Use the complete design connectivity for multi-page schematics.

**PCB.** Plan from the measured outline, pads, keepouts, and stackup. Use the available `pcb` subcommands for placement, tracks, vias, and pours. Run `pcb pour-rebuild`, `pcb dump --include-copper`, `pcb drc`, and `pcb save`. If supported, use a targeted `doc reload` after saving and obtain a fresh dump. Report any missing capability and the checks it prevents.

For version-specific command details and examples, see [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent).

## Official desktop CLI and extension API

```powershell
lceda-pro doctor
lceda-pro session list
lceda-pro doc api --class-name SCH_PrimitiveWire
lceda-pro doc api --class-name PCB_PrimitiveLine
```

The mainland desktop CLI guide specifies V4.1.60 or later. Use `lceda-pro --help` to confirm support in the installed build. For Codex with stdio MCP, run `codex mcp add lceda -- lceda-pro --mcp stdio` with the executable's absolute path if needed. In a new session, inspect the available tools and identify the intended editor session.

After setting `$session` to the ID returned by `session list`, probe the selected editor version.

```powershell
lceda-pro invoke --session $session --ext-uuid eda --code 'return eda.sys_Environment.getEditorCurrentVersion()'
```

Look up exact API signatures before using them. Start with a small read-only probe to identify the active document and its objects. Build bounded calls using actual pin endpoints for schematic wires and the actual net, layer, and endpoints for PCB traces. Keep the arguments and generated code inspectable. After each batch, read the objects by ID and verify their properties.

For the extension route, follow the gateway's installation instructions and start the matching bridge before connecting to the editor. [Official CLI](https://prodocs.easyeda.com/en/api/guide/cli.html) · [Extension API](https://prodocs.easyeda.com/en/api/reference/pro-api.html) · [Run API Gateway](https://jlcext.com/item/oshwhub-official/run-api-gateway) · [Codex MCP](https://developers.openai.com/codex/mcp)

## Readback and recovery

- Before writing, verify project, document, units, origin, Y direction, component anchor, and board side. Read the actual bounding boxes and pad positions when placing parts.
- Use returned IDs to locate new objects and read them back from the target document. Compare the resulting nets, coordinates, and rules with the plan.
- After a timeout or disconnect, reconnect to the intended document and read the current objects, including any unsaved changes, before reloading or writing. Compare the baseline and desired state with the fresh inventory. Skip operations that already took effect and apply only the missing delta. Resolve unknown state with a fresh read or a known snapshot before retrying.
- Use the active tool profile to establish which operations are supported. The [easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) examples illustrate capability discovery, ERC, DRC, and exports.
