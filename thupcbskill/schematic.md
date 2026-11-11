# Schematics, interconnects, and acquisition chains

## Read the reference board

Read the paired schematic and PCB. Capture pages, designators, exact part and library records, symbol pin endpoints, footprints, pads, net memberships, outline, stackup, and copper. For database-backed project files, use a supported editor export or a read-only parser. Cross-check the schematic against the PCB pad-net mapping and record coverage gaps.

In the reference hardware, repeated channels use a common orientation and wired net labels at block boundaries. Their PCB counterparts adapt placement to the board edge, port locations, and available routing space. Carry forward the topology and the association between each supporting part and its owner pin. Recompute geometry from the target device endpoints.

## Draw the schematic

1. Divide the design into power, external interfaces, analog front end, control, and communications as appropriate. Arrange each block along the signal flow. Show local supplies and returns and label cross-page I/O.
2. Compare datasheet pins, symbol pins, and footprint pads. Inspect shared power pins and the common package on multi-unit parts. Keep each physical pad ID when multiple pads share a pin number.
3. Place the core device and then its series, filter, feedback, decoupling, and bias parts according to pin function. Use short orthogonal wires for local connections. Attach net labels to actual wire segments. Check T-junctions, wire crossings, and label scope.
4. Give each repeated channel its own references and endpoint mapping. State any shared supplies, references, select, and enable nets. Verify operating rails, input limits, and startup states for the ADC, switch, and amplifier.
5. Compare expected and actual endpoints on each critical net. Record explicit NCs, reserved pins, single-pad test nets, unresolved pins, and unexpected opens according to their intended use. Resolve unintended differences before synchronizing.

## Review a board-to-board connection

For every conductor, record the connector and pin on each board, local nets, common function, source and load roles, working voltage ranges, and evidence. Check exact connector and mate, pin 1, viewing side, mating orientation, cable reversal, pin count, and actual PCB pads. Compare the symbol pin table, pad table, and measured harness order where available.

Review supply and return conductors first. Then check signal direction, working input range, and logic thresholds. Verify fixed-output regulator suffixes against their datasheets. Account for source tolerance, load limits, and cable drop. Record conflicts such as two sources, unknown direction, or out-of-range supply.

The [wiring checker](check_interfaces.py) handles ordinary point-to-point links. See the [example](example.md) for its data format. Review open-drain, differential, multidrop, shield, level translation, and active adapter circuits using their specific electrical constraints.

## Trace an acquisition channel

| Path | Evidence |
| --- | --- |
| Row drive to sensor cell to column | Connector pins, drive levels, unselected row states, return and leakage paths |
| Column to switch channel to common | Physical pins, address bit weights, enable polarity, truth table, and signal supply range |
| Common to analog front end to ADC | Actual common node, front-end topology, swing, ADC reference, and settling |
| ADC to sample index | ADC input number, scan order, wait or discard interval, and a single-channel test |

Determine whether the path is a voltage divider, current readout, transimpedance amplifier, or another topology before calculating its range. For high-impedance nodes, check switch on-resistance and variation, leakage, capacitance, carryover from the previous channel, and the ADC sampling load. Assign bias, summing nodes, and feedback components to the corresponding amplifier. Specify the required short paths, return connections, and test points. Confirm physical wiring and measurement performance with separate hardware evidence.
