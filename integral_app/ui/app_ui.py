import tkinter as tk
from tkinter import font as tkfont

from core.validator import validate_input
from core.engine import compute_integral
from core.trail_logger import build_trail
from core.verifier import verify
from core.formatter import fmt


class IntegrationApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("Indefinite Integration Generator")
        self.geometry("750x640")
        self.configure(bg="#F0F0F0")
        self._build_fonts()
        self._build_ui()

    def _build_fonts(self):
        self.font_label  = tkfont.Font(family="Arial",       size=11)
        self.font_input  = tkfont.Font(family="Courier New", size=12)
        self.font_answer = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.font_trail  = tkfont.Font(family="Courier New", size=10)
        self.font_btn    = tkfont.Font(family="Arial",       size=11)
        self.font_title  = tkfont.Font(family="Arial",       size=13, weight="bold")
        self.font_status = tkfont.Font(family="Arial",       size=9,  slant="italic")

    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self, bg="#2E75B6", pady=10)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Indefinite Integration Generator",
                 font=self.font_title, fg="white", bg="#2E75B6").pack()
        tk.Label(title_frame,
                 text="Enter a function f(x) to compute its antiderivative with step-by-step explanation.",
                 font=tkfont.Font(family="Arial", size=9),
                 fg="#D9E2F3", bg="#2E75B6").pack()

        # Input row
        input_frame = tk.Frame(self, bg="#F0F0F0", pady=12, padx=16)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Enter f(x):",
                 font=self.font_label, bg="#F0F0F0").grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.entry = tk.Entry(input_frame, font=self.font_input, relief=tk.SUNKEN, bd=2, width=40)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), ipady=4)
        self.entry.bind("<Return>", lambda e: self._on_integrate())
        self.entry.bind("<KeyRelease>", self._on_input_change)
        self.entry.focus_set()

        self.integrate_btn = tk.Button(
            input_frame, text="Integrate", font=self.font_btn,
            bg="#2E75B6", fg="white", relief=tk.FLAT, padx=12, pady=4,
            command=self._on_integrate)
        self.integrate_btn.grid(row=0, column=2, padx=(0, 6))

        tk.Button(input_frame, text="Clear", font=self.font_btn,
                  bg="#D0D0D0", fg="black", relief=tk.FLAT, padx=12, pady=4,
                  command=self._on_clear).grid(row=0, column=3)

        input_frame.columnconfigure(1, weight=1)

        tk.Label(input_frame,
                 fg="#666666", bg="#F0F0F0").grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 0))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(input_frame, textvariable=self.status_var,
                 font=self.font_status, fg="#888888",
                 bg="#F0F0F0").grid(row=2, column=0, columnspan=4, sticky="w", pady=(2, 0))

        # Result display
        ans_frame = tk.LabelFrame(self, text="  Result  ", font=self.font_label,
                                  bg="#F0F0F0", padx=12, pady=8)
        ans_frame.pack(fill=tk.X, padx=16, pady=(0, 8))

        self.answer_var = tk.StringVar(value="—")
        self.answer_label = tk.Label(ans_frame, textvariable=self.answer_var,
                             font=self.font_answer, fg="#1F5C1F",
                             bg="#F0F0F0", wraplength=1200, justify=tk.LEFT)
        self.answer_label.pack(anchor="w")

        # Solution trail
        trail_frame = tk.LabelFrame(self, text="  Solution Trail  ", font=self.font_label,
                                    bg="#F0F0F0", padx=8, pady=6)
        trail_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        self.trail_text = tk.Text(trail_frame, font=self.font_trail, bg="white", fg="#1A1A1A",
                                  relief=tk.SUNKEN, bd=1, wrap=tk.NONE,
                                  state=tk.DISABLED, padx=8, pady=6)
        self.trail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(trail_frame, command=self.trail_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trail_text.configure(yscrollcommand=v_scroll.set)

        h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.trail_text.xview)
        h_scroll.pack(fill=tk.X, padx=16, pady=(0, 6))
        self.trail_text.configure(xscrollcommand=h_scroll.set)

    def _on_input_change(self, event=None):
        """Clears stale result whenever the user edits the input field."""
    # Ignore modifier-only keys like Shift, Ctrl, Alt, Caps Lock
        if event and event.keysym in (
        "Shift_L", "Shift_R", "Control_L", "Control_R",
        "Alt_L", "Alt_R", "Caps_Lock", "Tab",
        "Left", "Right", "Up", "Down", "Home", "End"
    ):
            return
            self.answer_var.set("—")
            self.answer_label.configure(fg="#1F5C1F")
            self._set_trail("")
            self.status_var.set("Ready")

    def _on_integrate(self):
        raw = self.entry.get()

        is_valid, err_msg, expr = validate_input(raw)
        if not is_valid:
            self._show_error(err_msg)
            return

        self.integrate_btn.configure(state=tk.DISABLED, text="Working...")
        self.status_var.set("Computing...")
        self.update_idletasks()

        try:
            antiderivative = compute_integral(expr)
        except ValueError as e:
            self._show_error(str(e))
            return
        except Exception as e:
            self._show_error(f"Unexpected error: {e}")
            return
        finally:
            self.integrate_btn.configure(state=tk.NORMAL, text="Integrate")

        try:
            _, verification_msg = verify(expr, antiderivative)
        except Exception as e:
            verification_msg = f"Verification failed: {e}"

        try:
            trail = build_trail(expr, antiderivative, verification_msg)
        except Exception as e:
            trail = f"Error building trail: {e}"

        self.answer_var.set(f"integral( {fmt(expr)} ) dx  =  {fmt(antiderivative)} + C")
        self.answer_label.configure(fg="#1F5C1F")
        self.status_var.set("Done")
        self._set_trail(trail)

    def _on_clear(self):
        self.entry.delete(0, tk.END)
        self.answer_var.set("—")
        self.answer_label.configure(fg="#1F5C1F")
        self.status_var.set("Ready")
        self._set_trail("")
        self.entry.focus_set()

    def _show_error(self, message: str):
        self.answer_var.set("Error: " + message.splitlines()[0])
        self.answer_label.configure(fg="#B00000")
        self.status_var.set("Error")
        self.integrate_btn.configure(state=tk.NORMAL, text="Integrate")
        self._set_trail("ERROR\n" + "-" * 55 + "\n" + message)

    def _set_trail(self, text: str):
        self.trail_text.configure(state=tk.NORMAL)
        self.trail_text.delete("1.0", tk.END)
        self.trail_text.insert(tk.END, text)
        self.trail_text.configure(state=tk.DISABLED)
        self.trail_text.see("1.0")