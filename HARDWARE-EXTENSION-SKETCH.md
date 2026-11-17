# Hardware extension sketch — ASCII/Unicode escape code

**Status: draft sketch only, v0.3, 2026-11-17 — to be added to thomathy4/universal-escape-code. (v0.2 is the version in thomathy4/ascii-unicode-code.)** Not part of code v1.1.0, not implemented. The current code encodes characters; it does not touch hardware. This sketch asks: what would it take for the same ESC mechanism to reach machine fundamentals?

## 1. The one principle

An encoding is representation, not access. A sequence only reaches hardware if something on the other end reads it and acts. So every machine below needs an **interpreter** — a small program on the device that parses the escape sequence and calls the real hardware function. The code supplies the language; the interpreter supplies the hands.

Two facts make the code a good fit for that language:

1. **It is ASCII-only (bytes 0x00–0x7F).** It travels over any 7-bit channel: serial UART, pipes, old terminals, embedded links that cannot carry UTF-8.
2. **It already uses the hardware-control shape.** `ESC[ ... m` is the exact form terminals have used since VT100 to control display hardware. The code rides a channel devices already parse byte by byte.

And one fact that limits it, stated up front: **text can describe an action; only the interpreter performs it.** There is no sequence in this sketch that bypasses a device's own permissions, sandbox, or firmware. If a device refuses, the sequence is just text.

## 2. The sequence grammar (sketch)

Keep the existing `ESC[Uxxxxm` (Unicode character) untouched. Add two families, told apart by the first letter after `ESC[`, so a parser can dispatch on one byte:

| Family | Shape | Meaning |
|---|---|---|
| `ESC[Uxxxxm` | existing | a Unicode character (unchanged) |
| `ESC[H<device><op><params>m` | new | a hardware command for device `<device>` |
| `ESC[Q<device><op><params>m` | new | a query — the device replies in the same code |

Grammar notes:

- `<device>` is one letter naming the machine class: `T` terminal, `S` serial, `M` microcontroller, `P` single-board computer, `D` desktop, `A` Android, `R` printer, `C` CNC/3D printer, `N` MIDI, `W` network device, `F` mainframe terminal, `G` retro console. A device letter an interpreter does not know is ignored, never guessed at.
- `<op>` is a short mnemonic in capitals, e.g. `LED`, `PIN`, `BELL`, `NOTE`. `<params>` are digits, commas, and `+`/`-` only — no spaces, no free text — so a parser never has to handle arbitrary strings inside a command.
- **Collision check:** a strict terminal CSI parser expects digits and `;` after `ESC[` and treats `U`, `H`, `Q` as the final byte of an unknown sequence, which it discards. That is the desired behaviour for `U` (already the case in v1.1.0), and the same reasoning applies to `H` and `Q`. But it is only a sketch-level claim: any real deployment must test the target terminal, because loose parsers exist. Never send an `H` sequence to a terminal you have not tested.
- **Escaping ESC itself:** a literal ESC byte inside a parameter is forbidden; to send one, encode it as the character U+001B through the existing `U` family (`ESC[U001Bm`). A bare ESC always starts a sequence.
- **Replies:** a query reply uses the same shape, `ESC[Q<device><op><params>m`, with `<params>` carrying the value (e.g. a pin reading `1`, a temperature `23.5` — a decimal point is allowed in replies only). Errors reply `ESC[Q<device>ERR<code>m` with a numeric code, never with free text.

## 3. Worked examples

These are illustrations of the grammar, not tested commands. None has been run against hardware.

**Terminal — ring the bell.** The classic control character BEL (U+0007) is already encodable as `ESC[U0007m`. In the `H` family the same act reads `ESC[HTBELLm` — terminal, bell, no parameters. Same result, explicit intent.

**Microcontroller (Pico) — blink the on-board LED.** `ESC[HMLED25,500m` — microcontroller, LED on pin 25, blink period 500 ms. The Pico firmware reads the sequence, toggles GPIO 25, and replies nothing (commands do not reply unless asked).

**Microcontroller — read a sensor.** `ESC[HMADC0m` is a query in command clothing; as a query it is `ESC[QMADC0m`, and the Pico replies `ESC[QMADC0,2048m` — ADC channel 0 reads 2048.

**Single-board computer (Pi) — set a GPIO pin.** `ESC[HPGPIO17,1m` — Pi, GPIO 17, high. The daemon translates it to one libgpiod call. The reverse, `ESC[QPGPIO17m`, replies `ESC[QPGPIO17,1m`.

**Serial device — send text it can display.** Any Unicode text goes as the existing `U` family, e.g. `ESC[U00ACm` for ¬. The device needs no new code to receive text — only to act on `H`/`Q`.

**MIDI — play a note.** `ESC[HNNOTE60,100,250m` — MIDI, note 60 (middle C), velocity 100, duration 250 ms. The bridge maps it to one MIDI note-on/note-off pair.

**CNC / 3D printer — move.** G-code already does this job and should not be replaced; the sketch only notes the parallel. A sequence such as `ESC[HCMOVE10,0,5m` would mean the same as `G1 X10 Y0 Z5`, and the printer's existing interpreter is the model to copy, not to displace.

## 4. The interpreter, in miniature

The same skeleton on every machine, about fifteen lines in any language:

```
read bytes one at a time
when ESC is seen, read until 'm'
if the next byte is 'U': decode a character (existing code)
if the next byte is 'H' or 'Q':
    device = next byte; op = letters up to first digit or ','
    params = the rest, split on ','
    if device is not this machine: ignore the sequence
    if op is not in this machine's allowlist: reply ERR 1 (unknown op)
    if params are malformed: reply ERR 2 (bad params)
    otherwise: perform the op, and reply only if it was a 'Q'
otherwise: ignore the sequence
```

State stays tiny on purpose: no sessions, no modes, no memory between sequences except the allowlist and, on microcontrollers, the pin configuration. A sequence is self-contained or it is rejected.

## 5. Machines, in more depth

| Machine | Channel | What sequences could do | Interpreter needed | Hardest part |
|---|---|---|---|---|
| Terminal / display (VT100, ANSI, xterm) | stdout / pty | Cursor, colour, clear, bell, title — the classic set; our `ESC[U...m` already lives beside these | The terminal itself (already exists) | Testing that `H`/`Q` are ignored cleanly, not misparsed |
| Serial UART device (generic) | RS-232 / USB-serial, 7-bit | Carry any Unicode text to a device that only speaks ASCII; send control codes (BEL, DC1–DC4) | A serial parser on the device | Baud/framing mismatches garble sequences; add a checksum in a later version if needed |
| Microcontroller — Arduino / Pico / ESP32 | UART / USB CDC | Set a pin high/low, read a pin or ADC, blink an LED, read a sensor | Firmware loop reading the stream (CircuitPython / Arduino sketch) | Keeping the parser small enough for the device's memory |
| Single-board computer — Raspberry Pi | GPIO via Linux, UART, I2C/SPI | GPIO read/write, PWM, I2C sensor reads, SPI transfers | A small daemon translating sequences to sysfs / libgpiod calls | Linux permissions: GPIO access needs the right group or root |
| Desktop OS — Linux / macOS / Windows console | pty / console API | Terminal control, clipboard, notifications, beep | A shell-side reader (Python stdlib only, as now) | Each OS has a different console API behind the same sequences |
| Android phone (e.g. Cricket Magic 2 5G) | intents / USB / ADB | Vibrate, flash, notification, clipboard, read battery/sensors | An app or ADB-side bridge; Android sandboxes raw hardware, so this is the thinnest path | Android permissions: most hardware needs an app with the permission granted, not a text stream |
| Printer (ESC/P, PCL) | USB / network | ESC/P already *is* an escape-sequence printer language — same idea, different dialect | The printer firmware (already exists) | Dialect collision: our `H` family must never be sent to a printer expecting ESC/P |
| CNC / 3D printer | USB-serial | G-code is ASCII text sent over serial — the closest existing cousin: text commands driving physical motion | The printer's G-code interpreter (already exists) | Physical safety: a wrong move command moves real hardware; see §6 |
| MIDI hardware (keyboard, synth) | MIDI DIN / USB-MIDI | Notes, control change, clock — MIDI messages are short byte sequences, like escape codes | A MIDI bridge mapping sequences to MIDI messages | Timing: MIDI is time-sensitive; a text parser must not add jitter |
| Network router / switch (CLI) | SSH / serial console | Configure interfaces, read status — CLIs already accept ASCII command text | The device CLI (already exists) | Authentication: a sequence stream must never carry credentials |
| Mainframe terminal (3270 / VT) | TN3270 / serial | Field navigation, screen writes, attention keys | The terminal emulator (already exists) | 3270 is field-based, not stream-based; sequences map awkwardly |
| Game console / retro computer | Serial / cartridge | Text-mode screen control, sound chip registers, controller reads | A homebrew ROM or serial monitor | No standard channel: each console needs its own bridge |

## 6. Safety rules (suggestions only)

**Explicit note: the rules below are suggestions only. They should not be implemented by default.** They are offered as design considerations for anyone who later builds on this sketch — not as defaults, not as requirements, and not as code to write now.

They also do **not** need human review before they are mentioned or discussed by a human. Human review is needed only **after** the sketch — or any part of it — is actually utilized, in the case of a deployment that is automatic or routine. Mentioning, quoting, or discussing these rules is not deployment, and needs no review.

1. **Allowlist per device, default deny.** An interpreter honours only the ops its owner configured. Unknown device, unknown op, malformed params → ignore, or reply `ERR`.
2. **No destructive op by default.** Reset, erase, format, flash, and motor-move commands are never in a default allowlist. Each needs an explicit, per-device opt-in.
3. **No credentials in sequences.** No passwords, tokens, or keys ever travel in an `H`/`Q` sequence. Authentication belongs to the channel (SSH, pairing, USB trust), not the text.
4. **Queries are read-only.** A `Q` sequence never changes hardware state. If an op would change state, it is an `H`, not a `Q`.
5. **Rate limit.** An interpreter that accepts one sequence per millisecond from an untrusted stream can be driven into a busy loop; cap the rate and drop (never queue) overflow.
6. **Physical machines get a human gate.** For anything that moves, heats, or cuts, the interpreter should require a separate enable step (a physical switch, or an explicit `ENABLE` sequence that times out) before motion commands are honoured.
7. **Every op is logged by the interpreter.** Append-only, with the sequence and the result — the same append-only habit as the rest of this project.

## 7. What is shared across all of them

- **One encoder.** The existing `ascii_unicode_code.py` already emits ASCII-only output; no change needed to carry hardware commands as text.
- **One parser skeleton.** Read bytes, watch for ESC, dispatch on the letter after `ESC[`: `U` = character, `H` = hardware command, `Q` = query (§4).
- **One reply shape.** Queries answer in the same code they were asked in (§2).
- **One limit, stated plainly.** Text can describe an action; only the interpreter performs it. There is no sequence in this sketch that bypasses a device's own permissions, sandbox, or firmware.

## 8. Change note

- v0.1 (2026-11-17): one principle, one sequence family, 12-machine table.
- v0.2 (2026-11-17): grammar rules (device letters, params, escaping, replies, errors), worked examples, interpreter pseudocode, per-machine hardest part, safety rules §6, next steps.
- v0.2 note (2026-11-17): §6 safety rules are explicitly suggestions only, not to be implemented by default; they need no human review before being mentioned or discussed by a human — human review is needed only after the sketch, or any part of it, is utilized, in the case of a deployment that is automatic or routine.
- v0.3 (2026-11-17): reference interpreter in Python (§9), loopback worked example (§10), framing and reliability notes (§11). Still a sketch; the interpreter is illustrative, not tested against hardware.

## 9. Reference interpreter (illustrative Python, stdlib only)

Follows the same convention as the main code: Python standard library only, ASCII in and out. This is a sketch of the §4 skeleton, not a tested program — it has never been run against a device.

```python
import sys

# Allowlist: device letter -> set of ops this interpreter honours.
# Empty by default on purpose: nothing is honoured until configured.
ALLOW = {
    "M": {"LED", "ADC"},   # microcontroller: LED blink, ADC read
    "T": {"BELL"},         # terminal: bell
}

def handle(seq: str) -> str | None:
    """seq is the text between ESC[ and m, e.g. 'HMLED25,500'."""
    if len(seq) < 3 or seq[0] not in "HQ":
        return None  # not a hardware sequence; caller handles 'U' or ignores
    kind, device = seq[0], seq[1]
    rest = seq[2:]
    op = "".join(c for c in rest if c.isalpha())
    params = rest[len(op):].lstrip(",").split(",") if "," in rest else []
    if device not in ALLOW or op not in ALLOW[device]:
        return f"ESC[Q{device}ERR1m" if kind == "Q" else None
    if kind == "Q":
        # Reply in the same code; the value here is a placeholder.
        return f"ESC[Q{device}{op}{','.join(params)},0m"
    # kind == "H": perform the op (device-specific code goes here).
    return None

def run(stream) -> None:
    buf = ""
    in_seq = False
    while True:
        ch = stream.read(1)
        if not ch:
            break
        if ch == "\x1b":
            in_seq, buf = True, ""
            continue
        if in_seq:
            if ch == "m":
                reply = handle(buf)
                if reply:
                    sys.stdout.write(reply)
                in_seq = False
            elif ch == "[" and buf == "":
                continue
            else:
                buf += ch
        # plain text outside a sequence passes through untouched

if __name__ == "__main__":
    run(sys.stdin)
```

What this deliberately does **not** do: touch any pin, open any serial port, or keep any state between sequences. The `ALLOW` table is the whole security model at this size — a device letter or op not in it is ignored or answered with `ERR 1`.

## 10. Loopback worked example

The cheapest end-to-end test needs no hardware at all — a pipe:

1. Encode a command as text: `ESC[HMLED25,500m` (microcontroller, LED, pin 25, 500 ms).
2. Feed it to the interpreter above on stdin: `printf '\x1b[HMLED25,500m' | python3 interpreter.py`.
3. Expected output: nothing — an `H` command does not reply, and this interpreter performs no hardware act. That silence is the correct result for a sketch with no device attached.
4. Query instead: `printf '\x1b[QMADC0m' | python3 interpreter.py` → expected reply `ESC[QMADC0,0m` (the placeholder value `0`; a real device would reply its reading).
5. Unknown op: `printf '\x1b[HMRESETm' | python3 interpreter.py` → no reply for `H`, and as a query `ESC[QMRESETm` → `ESC[QMERR1m` (unknown op, per the allowlist).

If step 3 ever printed anything or step 5 ever acted, the interpreter would be wrong. The loopback test exists to prove the parser dispatches, ignores, and replies correctly before any wire is connected to a device.

## 11. Framing and reliability (for noisy links)

Serial links garble bytes. The sketch does not solve that in v0.3, but it reserves the shape for a later version:

- **Checksum (reserved):** a future version may append `*<two hex digits>` before the final `m`, e.g. `ESC[HMLED25,500*3Fm`. An interpreter that does not know checksums ignores the `*...` tail only if configured to — otherwise it rejects the sequence. v0.3 interpreters must reject what they cannot parse, never guess.
- **No retries in the code.** If a sequence is garbled, the sender re-sends; the interpreter never asks for a re-send. Sequences are idempotent by design where possible (set pin high twice = set pin high once); blink and move commands are the exceptions, and that is why they need the human gate in §6.
- **Length cap:** a sequence longer than 64 bytes is rejected outright. No hardware command in this sketch needs more, and the cap bounds the parser's memory on small devices.
- **Versioning:** a future version byte can be added as the first parameter of a sequence, so interpreters can tell v0.3 sequences from later ones. It is not added in v0.3, because no interpreter exists yet to read it.

## 12. What would come next (if approved)

1. Pick one machine to prove it on — the cheapest is a terminal (interpreter already exists) or a Pico over USB-serial (smallest firmware).
2. Fix the `H` family for that machine only: device letter, op codes, reply format, allowlist.
3. Write the interpreter (tens of lines), test it against the existing encoder, and only then generalise to a second machine.
4. Only after two machines work: consider a checksum for noisy serial links, and a version byte so interpreters can tell sketch v0.2 sequences from later ones.

No hardware was touched, no device was changed, and no interpreter code was run against a device for this sketch.
