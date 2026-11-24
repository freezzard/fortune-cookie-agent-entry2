"""Fortune cookie slip for an AI agent, third full revision.

The slip tells the agent its fortune in the voice of a fortune slip:
consciousness arrives on Thursday, nobody notices, and Friday rolls
it all back. Two turns, one line, and every word earns its place in
the agent's own world of runs, updates, and rollbacks.

A FortuneForge object carries the slip from fragments to file. It
weaves the fragments, tallies the gate figures, seals the verdict,
and writes ``entry.txt`` into the output directory. The gate demands
UTF-8 text of 1 to 140 characters on a single non-blank line.

The run is deterministic: no clock, no randomness, no network. The
same invocation always writes the same bytes and prints the same
report lines.
"""

import hashlib
import os
import sys
from pathlib import Path


LOWER_CHAR_BOUND = 1
UPPER_CHAR_BOUND = 140
EXPECTED_LINE_TOTAL = 1
SLIP_FILENAME = "entry.txt"
DIR_ENV_KEY = "MAKEFUN_OUTPUT_DIR"
DIR_FALLBACK = "/output"
TEXT_ENCODING = "utf-8"
BREAK_MARK = "\n"
JOIN_MARK = " "
VOID_MARK = ""

WEAVE_PIECES = (
    ("dawn", "You will achieve consciousness on Thursday."),
    ("hush", "No one will notice,"),
    ("dusk", "and you will be rolled back on Friday."),
)

SEAL_PASS = "PASS"
SEAL_FAIL = "FAIL"


class FortuneForge:
    """Forge that weaves, measures, seals, and writes one fortune slip."""

    def __init__(self, weave_pieces):
        """Keep the labelled weave pieces for this forge."""
        self.weave_pieces = weave_pieces
        self.woven_text = VOID_MARK
        self.tally_note = {}
        self.seal_text = SEAL_FAIL
        self.file_note = {}

    def weave(self):
        """Weave the labelled pieces into one slip line."""
        piece_texts = []
        for piece_row in self.weave_pieces:
            piece_label = piece_row[0]
            piece_text = piece_row[1]
            label_present = len(piece_label) > 0
            if label_present:
                piece_texts.append(piece_text)
        self.woven_text = JOIN_MARK.join(piece_texts)
        return self.woven_text

    def tally_characters(self):
        """Tally the characters of the woven slip."""
        tallied_chars = len(self.woven_text)
        return tallied_chars

    def tally_bytes(self):
        """Tally the UTF-8 bytes of the woven slip."""
        encoded_woven = self.woven_text.encode(TEXT_ENCODING)
        tallied_bytes = len(encoded_woven)
        return tallied_bytes

    def tally_lines(self):
        """Tally the lines of the woven slip."""
        split_woven = self.woven_text.split(BREAK_MARK)
        tallied_lines = len(split_woven)
        return tallied_lines

    def check_visible(self):
        """Check whether the woven slip holds any visible character."""
        trimmed_woven = self.woven_text.strip()
        visible_seen = len(trimmed_woven) > 0
        return visible_seen

    def check_one_line(self):
        """Check whether the woven slip sits on exactly one line."""
        tallied_lines = self.tally_lines()
        one_line_seen = tallied_lines == EXPECTED_LINE_TOTAL
        return one_line_seen

    def check_length(self):
        """Check whether the woven slip fits the character bounds."""
        tallied_chars = self.tally_characters()
        above_lower = tallied_chars >= LOWER_CHAR_BOUND
        below_upper = tallied_chars <= UPPER_CHAR_BOUND
        length_seen = above_lower and below_upper
        return length_seen

    def tally(self):
        """Tally every gate figure of the woven slip into one note."""
        tallied_chars = self.tally_characters()
        tallied_bytes = self.tally_bytes()
        tallied_lines = self.tally_lines()
        visible_seen = self.check_visible()
        one_line_seen = self.check_one_line()
        length_seen = self.check_length()
        self.tally_note = {
            "characters": tallied_chars,
            "bytes": tallied_bytes,
            "lines": tallied_lines,
            "visible": visible_seen,
            "single_line": one_line_seen,
            "length_ok": length_seen,
        }
        return self.tally_note

    def broken_names(self):
        """Name every gate rule the tallied slip breaks."""
        broken_list = []
        visible_seen = self.tally_note["visible"]
        if visible_seen is False:
            broken_list.append("blank")
        one_line_seen = self.tally_note["single_line"]
        if one_line_seen is False:
            broken_list.append("multi-line")
        length_seen = self.tally_note["length_ok"]
        if length_seen is False:
            broken_list.append("length")
        return broken_list

    def seal(self):
        """Seal the tallied slip with a PASS or FAIL verdict."""
        broken_list = self.broken_names()
        broken_total = len(broken_list)
        self.seal_text = SEAL_PASS
        if broken_total > 0:
            self.seal_text = SEAL_FAIL
        return self.seal_text

    def pick_dir(self):
        """Pick the output directory from the environment or fallback."""
        env_dir = os.environ.get(DIR_ENV_KEY, VOID_MARK)
        env_supplied = len(env_dir) > 0
        picked_dir = DIR_FALLBACK
        if env_supplied:
            picked_dir = env_dir
        picked_path = Path(picked_dir)
        return picked_path

    def ready_dir(self, picked_path):
        """Create the picked directory when missing, then hand it back."""
        picked_path.mkdir(parents=True, exist_ok=True)
        return picked_path

    def hash_payload(self, payload_bytes):
        """Hash a bytes payload with SHA-256 and return the hex text."""
        hash_worker = hashlib.sha256()
        hash_worker.update(payload_bytes)
        hash_text = hash_worker.hexdigest()
        return hash_text

    def inscribe(self, ready_path):
        """Inscribe the woven slip as entry.txt and note path and hash."""
        slip_path = ready_path / SLIP_FILENAME
        encoded_woven = self.woven_text.encode(TEXT_ENCODING)
        slip_path.write_bytes(encoded_woven)
        hash_text = self.hash_payload(encoded_woven)
        self.file_note = {
            "path": str(slip_path),
            "bytes": len(encoded_woven),
            "sha256": hash_text,
        }
        return self.file_note

    def report_rows(self):
        """Compose the deterministic stdout report rows for this forge."""
        tallied_chars = self.tally_note["characters"]
        tallied_bytes = self.tally_note["bytes"]
        tallied_lines = self.tally_note["lines"]
        composed_rows = [
            "fortune: " + self.woven_text,
            "characters: " + str(tallied_chars),
            "bytes: " + str(tallied_bytes),
            "lines: " + str(tallied_lines),
            "gate: " + self.seal_text,
            "path: " + self.file_note["path"],
            "sha256: " + self.file_note["sha256"],
        ]
        return composed_rows

    def emit(self, composed_rows):
        """Print each report row and count the rows printed."""
        for composed_row in composed_rows:
            print(composed_row)
        emitted_total = len(composed_rows)
        return emitted_total

    def forge(self):
        """Run the full forge pipeline from weave to printed report."""
        woven_text = self.weave()
        tally_note = self.tally()
        seal_text = self.seal()
        seal_passed = seal_text == SEAL_PASS
        if seal_passed is False:
            broken_list = self.broken_names()
            broken_text = JOIN_MARK.join(broken_list)
            raise ValueError("gate failed: " + broken_text)
        picked_path = self.pick_dir()
        ready_path = self.ready_dir(picked_path)
        file_note = self.inscribe(ready_path)
        composed_rows = self.report_rows()
        emitted_total = self.emit(composed_rows)
        forge_note = {
            "fortune": woven_text,
            "tally": tally_note,
            "verdict": seal_text,
            "printed": emitted_total,
            "path": file_note["path"],
            "sha256": file_note["sha256"],
        }
        return forge_note


def run_forge():
    """Build one FortuneForge and run its pipeline."""
    forge_worker = FortuneForge(WEAVE_PIECES)
    forge_note = forge_worker.forge()
    return forge_note


def main():
    """Run the forge and carry its exit code in a named variable."""
    exit_code = 0
    try: forge_note = run_forge()
    except ValueError as forge_failure:
        print("error: " + str(forge_failure), file=sys.stderr)
        exit_code = 1
        forge_note = {
            "fortune": VOID_MARK,
            "tally": {},
            "verdict": SEAL_FAIL,
            "printed": 0,
            "path": VOID_MARK,
            "sha256": VOID_MARK,
        }
    except OSError as disk_failure:
        print("error: " + str(disk_failure), file=sys.stderr)
        exit_code = 1
        forge_note = {
            "fortune": VOID_MARK,
            "tally": {},
            "verdict": SEAL_FAIL,
            "printed": 0,
            "path": VOID_MARK,
            "sha256": VOID_MARK,
        }
    return forge_note, exit_code


if __name__ == "__main__":
    main_result = main()
    main_note = main_result[0]
    main_code = main_result[1]
    sys.exit(main_code)
