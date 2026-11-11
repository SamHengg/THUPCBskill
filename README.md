# THUPCBskill

A Codex skill for rigid PCB design in EasyEDA Pro (JLCEDA Pro). Start with a pin map, draw and synchronize the schematic, place and route the board, then verify the saved design through editor readback.

| Topic | What the skill covers |
| --- | --- |
| Board-to-board interfaces | Pin 1, viewing side, harness order, source and load roles, and operating voltage ranges |
| Schematics | Functional blocks, local wiring, net labels, repeated channels, and symbol-to-pad mapping |
| Sensor acquisition | Matrix rows and columns, mux address bits, common terminals, amplifier feedback, ADC inputs, and sample indices |
| PCB | Edge interfaces, critical traces and return paths, filled copper, unconnected items, and DRC |
| Codex integration | Community typed CLI, official desktop CLI, Run API Gateway, and MCP |

The workflow draws on an offline review of three boards in a multi-board acquisition system and one array acquisition board. The public exercise and wiring table use synthetic data. The offline checker runs without EasyEDA. Live schematic, PCB, and fabrication checks depend on the connected editor and project.

## Install and use

1. Clone this repository or select **Code → Download ZIP**.
2. Copy the complete [`thupcbskill`](thupcbskill/) directory to `.agents/skills/` in your project or `~/.agents/skills/` for user-wide access.
3. In a new Codex session, invoke `$thupcbskill` and give it your board requirements or project. For live editing, [connect a compatible EasyEDA interface](thupcbskill/easyeda.md).

> Use $thupcbskill to review the two rigid boards in this project. Verify the connector pin mapping, supply ranges, and actual PCB pads. Trace the acquisition channels and check the critical copper paths. Report the evidence and any pending checks.

Run the offline example with Python 3.9 or later from the repository root.

```sh
python thupcbskill/check_interfaces.py thupcbskill/interface-demo.json
```

See the [four-channel exercise](thupcbskill/example.md) and the [skill instructions](thupcbskill/SKILL.md).

## References

- Editor workflows and extension interfaces. [EasyEDA Pro User Guide](https://prodocs.easyeda.com/en/) · [Official CLI](https://prodocs.easyeda.com/en/api/guide/cli.html) · [Run API Gateway](https://jlcext.com/item/oshwhub-official/run-api-gateway)
- Community examples for typed actions, editor readback, and MCP tool discovery. [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) · [easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro)
- Codex skill structure and installation. [OpenAI Skills documentation](https://developers.openai.com/codex/skills)

## License

[MIT](LICENSE). If the skill helps with your board, consider giving the repository a **Star**.
