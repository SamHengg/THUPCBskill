# Rigid PCB placement, routing, and verification

## Synchronize from the schematic

Save the schematic and review ERC. Preview the changes and examine designators, footprints, additions, removals, changed nets, duplicate-number pads, and effects on existing copper. After applying, reconcile PCB pad nets with the schematic endpoints. Record the effective stackup, board and copper thicknesses, clearance, trace width, hole diameter, and copper-to-edge rules from the current board and fabrication requirements.

## Place the board

1. **Mechanical references.** Establish the closed outline, slots, mounting holes, board-edge parts, and mating clearances. Fix specified locations first. Verify board side, coordinates, rotation, and pin 1.
2. **Interface to front end.** Place interface protection, mux, amplifier, ADC, and controller by their actual pad positions. Reserve short paths for analog inputs, the mux common node, feedback, and references. Recalculate external paths after moving or reusing a block.
3. **Local loops.** Place decoupling by the assigned supply pin and inspect the complete supply and return loop. Keep input protection near the entry point and its return. Use datasheet guidance for switching loops, thermal copper, and vias.
4. **Routing space.** Reserve escape paths, reference copper, test probe access, and routing channels. Keep repeated channels consistent where useful and adjust to fit electrical and mechanical constraints. Check the actual footprints and part heights.

## Route and rebuild copper

- Prioritize the nets with design-specific constraints such as sensitive analog, power, clocks, or differential pairs. Select width, clearance, vias, and reference layers from those constraints. On many two-layer boards, keeping the shortest critical paths on the component side leaves more return copper on the other side.
- Check the layer span and nearby return path at signal vias. Limit loop area and parallel runs alongside switching traces on high-impedance, reference, and feedback nets. Measure critical path length, layer transitions, and reference copper along the route.
- Size power trunks and fanouts for current, copper thickness, temperature rise, and voltage drop. Check narrow sections, contacts, and vias. Use the applicable specifications for impedance and length constraints.
- Set the net, layer, thermal connection, and island rules before rebuilding pours. Read the generated islands and holes. Verify contact through pads, thermal spokes, and vias. Establish where grounds join from the actual return requirements and connection topology.
- Verify pin 1, polarity, connector labels, and orientation on both sides. Keep silkscreen clear of pads and the board edge and recheck it after footprint moves.

## Verify the saved board

| Check | Readback |
| --- | --- |
| Endpoints and ratsnest | Expected pad-to-pad paths, actual copper and nets, and unconnected items after rebuild |
| Shorts and clearance | Effective DRC rules, run coverage, findings, and the disposition of each finding |
| Analog return | Critical trace projection over reference copper, crossings and transitions, actual islands and contacts |
| Mechanics and test access | Outline, slots, holes, mating direction, component envelope, silkscreen, and key test points |
| Persistence | Fresh document readback after save and, where supported, reopen |
| Fabrication and assembly | Gerber and drill previews from the same PCB revision, plus BOM and placement data when applicable |

One reference board had a connected sensitive trace whose projection crossed gaps in the opposite copper layer. Review the actual reference copper along critical traces as well as the ratsnest. Report geometry, ERC, DRC, exports, and hardware evidence separately.

When fabrication files are requested, label each set by board and revision. Include the board outline, Gerber layers, applicable plated and non-plated drill data, and required stackup and finish notes. For assembly, match BOM designators and placement side, rotation, and units to the same revision. For an inter-board harness, include the verified pin map and mating views.

Official workflow references are available for [schematic design](https://prodocs.lceda.cn/cn/private/designer/design-schematic.html), [PCB design](https://prodocs.lceda.cn/cn/private/designer/design-pcb.html), and [PCB rules](https://prodocs.lceda.cn/cn/schematic/design-pcb-design-rule/).
