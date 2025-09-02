#!/usr/bin/env python

import sys
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Caps Locker – Uppercase Converter"

def to_caps(text: str) -> str:
    # For this use-case, uppercasing the whole string matches the example transformation.
    # It preserves digits and underscores as-is.
    if text is None:
        return ""
    return text.upper()

def run_cli(argv):
    parser = argparse.ArgumentParser(
        prog="caps_locker",
        description="Convert text to UPPERCASE. Example: ST010_FG01_BG1_Container_Present -> ST010_FG01_BG1_CONTAINER_PRESENT",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to convert. If omitted, reads from STDIN.",
    )
    args = parser.parse_args(argv)

    if args.text:
        # Join with spaces so multiple args form a single string as typed.
        input_text = " ".join(args.text)
    else:
        # Read from STDIN if piped or user hits Enter on empty args.
        input_text = sys.stdin.read()

    result = to_caps(input_text)
    # Print without extra newline if input already ended with newline
    sys.stdout.write(result)
    if not result.endswith("\n"):
        sys.stdout.write("\n")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(540, 360)
        self._build_ui()

    def _build_ui(self):
        # Root container
        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        # Input label + text
        lbl_in = ttk.Label(container, text="Input")
        lbl_in.pack(anchor="w")
        self.txt_in = tk.Text(container, height=6, wrap="none", undo=True)
        self.txt_in.pack(fill="both", expand=True, pady=(4, 12))
        self.txt_in.bind("<<Modified>>", self._on_input_modified)

        # Output label + text (read-only)
        lbl_out = ttk.Label(container, text="Output (UPPERCASE)")
        lbl_out.pack(anchor="w")
        self.txt_out = tk.Text(container, height=6, wrap="none", state="disabled")
        self.txt_out.pack(fill="both", expand=True, pady=(4, 12))

        # Controls
        controls = ttk.Frame(container)
        controls.pack(fill="x")

        self.var_auto = tk.BooleanVar(value=True)
        chk_auto = ttk.Checkbutton(controls, text="Auto-convert", variable=self.var_auto)
        chk_auto.pack(side="left")

        btn_convert = ttk.Button(controls, text="Convert", command=self.convert_now)
        btn_convert.pack(side="left", padx=(8, 0))

        btn_copy = ttk.Button(controls, text="Copy Output", command=self.copy_output)
        btn_copy.pack(side="left", padx=(8, 0))

        btn_clear = ttk.Button(controls, text="Clear", command=self.clear_all)
        btn_clear.pack(side="left", padx=(8, 0))

        # Status bar
        self.status = ttk.Label(self, relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom")
        self.set_status("Ready")

    def set_status(self, text: str):
        self.status.config(text=f" {text}")

    def _on_input_modified(self, event):
        # Reset modified flag
        self.txt_in.edit_modified(False)
        if self.var_auto.get():
            self.convert_now()

    def _set_output(self, text: str):
        self.txt_out.config(state="normal")
        self.txt_out.delete("1.0", "end")
        self.txt_out.insert("1.0", text)
        self.txt_out.config(state="disabled")

    def convert_now(self):
        src = self.txt_in.get("1.0", "end").rstrip("\n")
        converted = to_caps(src)
        self._set_output(converted)
        self.set_status("Converted to UPPERCASE")

    def copy_output(self):
        try:
            out = self.txt_out.get("1.0", "end")
            self.clipboard_clear()
            self.clipboard_append(out.strip("\n"))
            self.set_status("Output copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")

    def clear_all(self):
        self.txt_in.delete("1.0", "end")
        self._set_output("")
        self.set_status("Cleared")

if __name__ == "__main__":
    # If arguments are present or piped input exists, prefer CLI behavior.
    # Detect if launched from a console with args or piped input.
    if len(sys.argv) > 1 or not sys.stdin.isatty():
        run_cli(sys.argv[1:])
    else:
        # GUI mode for double-click on Windows
        try:
            # Use ttk theme if available
            app = App()
            app.mainloop()
        except Exception as e:
            # Fallback to CLI error message if GUI fails for some reason
            sys.stderr.write(f"Error starting GUI: {e}\n")
            sys.exit(1)
