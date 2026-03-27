import tkinter as tk
from tkinter import font as tkfont, ttk

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
        self.geometry("1000x660")
        self.minsize(1000, 500)
        self.configure(bg="#F0F0F0")
        self._history = []          # stores last 5 successful inputs
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
        self.font_calc   = tkfont.Font(family="Courier New", size=10)

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

        # Main body — left (solver) and right (calculator panel)
        body_frame = tk.Frame(self, bg="#F0F0F0")
        body_frame.pack(fill=tk.BOTH, expand=True)

        # ── LEFT SIDE ──────────────────────────────────────────────────────
        left_frame = tk.Frame(body_frame, bg="#F0F0F0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Input row
        input_frame = tk.Frame(left_frame, bg="#F0F0F0", pady=12, padx=16)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Enter f(x):",
                 font=self.font_label, bg="#F0F0F0").grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.entry = tk.Entry(input_frame, font=self.font_input, relief=tk.SUNKEN, bd=2, width=34)
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


        # History dropdown — row 2
        history_frame = tk.Frame(input_frame, bg="#F0F0F0")
        history_frame.grid(row=2, column=0, columnspan=4, sticky="w", pady=(4, 0))

        tk.Label(history_frame, text="History:",
                 font=self.font_status, fg="#888888", bg="#F0F0F0").pack(side=tk.LEFT, padx=(0, 6))

        self.history_var = tk.StringVar(value="")
        self.history_dropdown = ttk.Combobox(
            history_frame,
            textvariable=self.history_var,
            font=tkfont.Font(family="Courier New", size=9),
            state="readonly",
            width=45,
            values=[]
        )
        self.history_dropdown.pack(side=tk.LEFT)
        self.history_dropdown.bind("<<ComboboxSelected>>", self._on_history_select)

        # Status label — row 3
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(input_frame, textvariable=self.status_var,
                 font=self.font_status, fg="#888888",
                 bg="#F0F0F0").grid(row=3, column=0, columnspan=4, sticky="w", pady=(2, 0))

        # Result display
        ans_frame = tk.LabelFrame(left_frame, text="  Result  ", font=self.font_label,
                                  bg="#F0F0F0", padx=12, pady=8)
        ans_frame.pack(fill=tk.X, padx=16, pady=(0, 8))

        self.answer_var = tk.StringVar(value="—")
        self.answer_label = tk.Label(ans_frame, textvariable=self.answer_var,
                                     font=self.font_answer, fg="#1F5C1F",
                                     bg="#F0F0F0", wraplength=1200, justify=tk.LEFT)
        self.answer_label.pack(anchor="w")

        # Solution trail
        trail_frame = tk.LabelFrame(left_frame, text="  Solution Trail  ", font=self.font_label,
                                    bg="#F0F0F0", padx=8, pady=6)
        trail_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 4))

        self.trail_text = tk.Text(trail_frame, font=self.font_trail, bg="white", fg="#1A1A1A",
                                  relief=tk.SUNKEN, bd=1, wrap=tk.NONE,
                                  state=tk.DISABLED, padx=8, pady=6)
        self.trail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(trail_frame, command=self.trail_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trail_text.configure(yscrollcommand=v_scroll.set)

        h_scroll = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.trail_text.xview)
        h_scroll.pack(fill=tk.X, padx=16, pady=(0, 8))
        self.trail_text.configure(xscrollcommand=h_scroll.set)

        # ── RIGHT SIDE — Calculator Panel ──────────────────────────────────
        self._build_calc_panel(body_frame)

    def _build_calc_panel(self, parent):
        """Builds the on-screen calculator panel on the right side."""
        calc_frame = tk.LabelFrame(
            parent, text="  Input Helper  ",
            font=self.font_label,
            bg="#E8E8E8", padx=8, pady=8,
            relief=tk.GROOVE, bd=2
        )
        calc_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 12), pady=12)

        buttons = [
            [("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("tan(x)", "tan(x)")],
            [("exp(x)", "exp(x)"), ("ln(x)",  "log(x)"), ("sqrt(x)","sqrt(x)")],
            [("x²",    "x^2"),    ("x³",    "x^3"),    ("1/x",   "1/x")],
            [("π",     "pi"),     ("e",     "E"),       ("( )",   "()")],
            None,
            [("7", "7"), ("8", "8"), ("9", "9"), ("+", "+")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("-", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("*", "*")],
            [("0", "0"), (".", "."), ("x", "x"), ("/", "/")],
            [("^", "^"), ("(", "("), (")", ")"), ("⌫", "DEL")],
        ]

        for row_data in buttons:
            if row_data is None:
                tk.Label(calc_frame, text="── numbers & operators ──",
                         font=tkfont.Font(family="Arial", size=8),
                         fg="#999999", bg="#E8E8E8").pack(pady=(6, 2))
                continue

            row_frame = tk.Frame(calc_frame, bg="#E8E8E8")
            row_frame.pack(fill=tk.X, pady=1)

            for label, insert in row_data:
                is_operator = insert in ("+", "-", "*", "/", "^", "DEL")
                btn = tk.Button(
                    row_frame,
                    text=label,
                    font=self.font_calc,
                    width=5,
                    relief=tk.FLAT,
                    bd=1,
                    pady=4,
                    bg="#E0E0E0" if is_operator else "#FFFFFF",
                    fg="#1A1A1A",
                    activebackground="#2E75B6",
                    activeforeground="white",
                    command=lambda ins=insert: self._calc_insert(ins)
                )
                btn.pack(side=tk.LEFT, padx=1)

    def _calc_insert(self, text):
        """Inserts calculator button text at the current cursor position."""
        if text == "DEL":
            # If there's a selection, delete it; otherwise delete char before cursor
            try:
                self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                pos = self.entry.index(tk.INSERT)
                if pos > 0:
                    self.entry.delete(pos - 1, pos)
        elif text == "()":
            pos = self.entry.index(tk.INSERT)
            self.entry.insert(pos, "()")
            self.entry.icursor(pos + 1)
        else:
            pos = self.entry.index(tk.INSERT)
            self.entry.insert(pos, text)

        self.entry.focus_set()
        self._on_input_change()

    def _update_history(self, raw: str):
        """Adds a successful input to the history dropdown, max 5 items."""
        if raw in self._history:
            self._history.remove(raw)
        self._history.insert(0, raw)
        self._history = self._history[:5]
        self.history_dropdown.configure(values=self._history)

    def _on_history_select(self, event=None):
        """Fills the entry field with the selected history item."""
        selected = self.history_var.get()
        if selected:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected)
            self.entry.focus_set()
            self._on_input_change()
            self.history_dropdown.selection_clear()

    def _on_input_change(self, event=None):
        """Clears stale result whenever the user edits the input field."""
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

        # Save to history on success
        self._update_history(raw)

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