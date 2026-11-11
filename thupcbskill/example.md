# Four-channel resistance acquisition exercise

This exercise uses synthetic design inputs. The main board supplies power and two select lines. The sensor board measures four resistances and returns one buffered analog signal. Fill in the actual parts and fabrication requirements when implementing the exercise.

## Circuit

- Each branch uses `EXC → 10 kΩ → SENSE_n → sensor resistance → GND`. With ideal 3.3 V excitation and 2–50 kΩ sensors, the nominal voltage is 0.55–2.75 V and the Thevenin resistance is approximately 1.67–8.33 kΩ. Include tolerances, switch leakage, and ADC loading for the real design.
- Route each `SENSE_n` to one input of a selected 4:1 analog switch. Check the channel selected by each `SEL1:SEL0` value in the device truth table. Set the enable state. Connect the common terminal to a buffer and send its output across the harness to the main-board ADC. Verify common-mode range, output swing, capacitive loading, and acquisition settling.
- The example interconnect carries supply, return, two select lines, and analog output. The two connectors have different physical pin assignments. Verify the actual connector view and cable order before using the design.

## Run the offline check

Run from this directory with Python 3.9 or later.

```sh
python check_interfaces.py interface-demo.json
```

In [the wiring table](interface-demo.json), `pins` uses `board.connector.physical_pin` identifiers. Each entry in `wires` identifies the two ends of one conductor.

| Field | Meaning |
| --- | --- |
| `net` | Local board net |
| `function` | Shared interconnect function |
| `role` | `power_out`, `power_in`, `signal_out`, `signal_in`, `gnd`, or `nc` |
| `voltage_v` | Two-element operating range in volts. Give the actual source range on outputs and the acceptable load range on inputs. |

List each expected pin once. For an intentionally open pin, use `nc` and optionally omit `net` and `function`. The checker covers pin use, compatible roles and functions, and supply ranges. Exit codes are `0` for consistency, `1` for conflicts, and `2` for invalid input. Check logic thresholds, current capacity, cable drop, physical order, and copper connectivity with separate evidence.

Copy `interface-demo.json` to `interface-conflict.json`. Change `pins["main.J1.1"].voltage_v` to `[4.9, 5.1]` and run `python check_interfaces.py interface-conflict.json`. The checker reports a voltage conflict on the supply conductor. Swapping `sensor.J2.3` and `sensor.J2.2` in the last two wires of a separate copy produces two function conflicts.

Enter the voltage range at the connector, including any upstream regulation. Compare net labels and pin counts with the actual schematic, footprint, and harness before accepting the table.

## Practice in EasyEDA Pro

1. Choose an [editor interface](easyeda.md) and identify both boards and their documents in a practice project.
2. Record the four dividers, switch truth table, buffer, ADC, and connector endpoints. Resolve the actual pin numbers, footprints, and values from the datasheets and current library. Have Codex place and connect devices using the reviewed endpoint map.
3. Read back the four inputs to the switch and the common path to the ADC. Check the harness table and run ERC. Preview the synchronization and verify the resulting footprints and pad nets.
4. Set the outline and connector orientation. Place the switch, buffer, and ADC endpoints. Route critical analog paths first and inspect their reference copper. Rebuild pours, review copper, unconnected items, and DRC, then save and obtain fresh readback.

> Use $thupcbskill in the current practice project. List the available EasyEDA tools, target boards, and missing device data. Check interface-demo.json and map the actual pins from the datasheets. Draw and verify the schematic and PCB, then report the results of the connectivity and rule checks.
