---
name: thupcbskill
description: Design, edit, or review rigid PCBs in EasyEDA Pro (JLCEDA Pro) with Codex. Use for schematic capture and wiring, board-to-board connector checks, sensor array and multiplexer readout, schematic-to-PCB synchronization, placement, routing, copper pours, and verification through a compatible CLI, extension bridge, or MCP.
license: MIT
metadata:
  version: "1.0.0"
---

# THUPCBskill

Turn the requirements into an endpoint map, mechanical constraints, and a placement and routing plan. Use the available EasyEDA Pro interface within the authorized scope, then verify the resulting objects in the editor.

| Task | Reference |
| --- | --- |
| Connect Codex to the editor or select an available CLI, gateway, or MCP | [Connection and operations](easyeda.md) |
| Read a reference board, draw a schematic, or review an interconnect or sensor readout | [Schematics and interfaces](schematic.md) |
| Synchronize, place, route, verify return paths, or review fabrication files | [PCB layout and verification](layout.md) |
| Run an offline wiring check and practice the design workflow | [Four-channel example](example.md) |

## Design workflow

1. Identify the target project, board, and pages. Record the source revision, exact part and package, connector viewing side, outline, keepouts, supplies, and sampling requirements. Check which assumptions from a reference board carry over.
2. Enumerate editor sessions and verify the target documents and host and connector versions. Read the baseline before writing. Keep a recoverable snapshot for structural or batch changes. With only local source files or drawings, complete offline analysis and prepare the design inputs that the evidence supports. Mark any work that depends on missing pin, voltage, or mechanical data as pending.
3. Record each intended endpoint with its reference designator, symbol pin number, physical pad, net, role, and source. Use actual pin coordinates for short orthogonal wires within each block. Use wired net labels or ports between blocks. Check net scope, junctions, explicit NCs, and shared power pins and packages on multi-unit parts.
4. Trace an acquisition channel from excitation through selection and conditioning to the ADC and sample index. Map physical pins, matrix rows and columns, switch inputs, and address bit weights. Check leakage, source impedance, and settling on high-impedance paths. Verify supply net labels against regulator variants and load limits.
5. Read back the schematic and run ERC. Preview the schematic-to-PCB change list and review part, package, and net differences. Establish the outline, holes, edge-mounted parts, and real stackup before placing critical paths and their supporting parts. Route and rebuild copper.
6. Read actual pad nets, tracks, vias, filled copper, and unconnected items. Check layer transitions, return paths, footprint orientation, and the effective DRC rules. Save and obtain fresh readback to verify persistence. After a timeout or partial write, read what exists before retrying or reverting.

## Evidence to report

| Status | Evidence |
| --- | --- |
| Offline analysis complete | Source revision, endpoint map or plan, and open questions |
| Schematic saved | Target pages, expected versus actual endpoint diff, ERC, and save readback |
| PCB saved | Outline and stackup, synchronization diff, critical copper paths, unconnected items, DRC, and save readback |
| Fabrication files reviewed | Gerber and drill previews from the same revision and assembly file checks where applicable |
| Hardware verified | Harness continuity, controlled power-up, or measurements |

Report unavailable checks as pending. Cite the actual result for each electrical, geometric, manufacturing, and hardware check.
