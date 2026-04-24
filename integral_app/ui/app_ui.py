import tkinter as tk
from tkinter import font as tkfont, ttk

from core.validator import validate_input
from core.engine import compute_integral
from core.trail_logger import build_trail
from core.verifier import verify
from core.formatter import fmt
from core.audit_log import AuditLog

# ── Colour palette ─────────────────────────────────────────────────────────────
BG_MAIN    = "#0f0f1a"
BG_PANEL   = "#1a1a2e"
BG_CARD    = "#16213e"
BG_INPUT   = "#0f3460"
ACCENT     = "#4cc9f0"
ACCENT2    = "#7209b7"
SUCCESS    = "#4ade80"
ERROR_COL  = "#f72585"
TEXT_MAIN  = "#e2e8f0"
TEXT_DIM   = "#94a3b8"
TEXT_CODE  = "#7dd3fc"
BTN_INT    = "#4361ee"
BTN_CLR    = "#334155"
BTN_COPY   = "#0f766e"
BTN_LOG    = "#6b21a8"
DIVIDER    = "#1e293b"


class IntegrationApp(tk.Tk):
    """Main application window — dark professional theme with audit log."""

    def __init__(self):
        super().__init__()
        self.title("IntegralSolver")
        self.geometry("1100x720")
        self.minsize(1000, 580)
        self.configure(bg=BG_MAIN)
        self._history  = []
        self._audit    = AuditLog()
        self._build_fonts()
        self._build_styles()
        self._build_ui()

    def _build_fonts(self):
        self.font_title   = tkfont.Font(family="Arial",       size=15, weight="bold")
        self.font_sub     = tkfont.Font(family="Arial",       size=9)
        self.font_label   = tkfont.Font(family="Arial",       size=10)
        self.font_input   = tkfont.Font(family="Courier New", size=12)
        self.font_answer  = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.font_trail   = tkfont.Font(family="Courier New", size=10)
        self.font_btn     = tkfont.Font(family="Arial",       size=10, weight="bold")
        self.font_status  = tkfont.Font(family="Arial",       size=9,  slant="italic")
        self.font_calc    = tkfont.Font(family="Courier New", size=9)
        self.font_section = tkfont.Font(family="Arial",       size=8,  weight="bold")

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
            fieldbackground=BG_INPUT, background=BG_PANEL,
            foreground=TEXT_MAIN, selectbackground=BTN_INT,
            selectforeground="white", borderwidth=0)
        style.map("Dark.TCombobox",
            fieldbackground=[("readonly", BG_INPUT)],
            foreground=[("readonly", TEXT_MAIN)])

    def _build_ui(self):
        # ── Header ─────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_PANEL, pady=14)
        header.pack(fill=tk.X)
        tk.Frame(header, bg=ACCENT, width=4).pack(side=tk.LEFT, fill=tk.Y, padx=(16, 12))
        title_block = tk.Frame(header, bg=BG_PANEL)
        title_block.pack(side=tk.LEFT)
        tk.Label(title_block, text="IntegralSolver",
                 font=self.font_title, fg=ACCENT, bg=BG_PANEL).pack(anchor="w")
        tk.Label(title_block,
                 text="Indefinite Integration Generator  ·  Step-by-Step Solution Trail",
                 font=self.font_sub, fg=TEXT_DIM, bg=BG_PANEL).pack(anchor="w")
        self.status_var = tk.StringVar(value="● Ready")
        self.status_dot = tk.Label(header, textvariable=self.status_var,
                                   font=self.font_status, fg=TEXT_DIM, bg=BG_PANEL)
        self.status_dot.pack(side=tk.RIGHT, padx=20)

        # ── Body ───────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(body, bg=BG_MAIN)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 8), pady=12)

        # ── Input card ─────────────────────────────────────────────────────
        input_card = tk.Frame(left, bg=BG_CARD, pady=14, padx=16,
                              highlightbackground=ACCENT, highlightthickness=1)
        input_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(input_card, text="FUNCTION INPUT",
                 font=self.font_section, fg=ACCENT, bg=BG_CARD).grid(
                 row=0, column=0, columnspan=5, sticky="w", pady=(0, 8))

        tk.Label(input_card, text="f(x) =",
                 font=self.font_label, fg=TEXT_DIM, bg=BG_CARD).grid(
                 row=1, column=0, sticky="w", padx=(0, 10))

        self.entry = tk.Entry(input_card, font=self.font_input,
                              bg=BG_INPUT, fg=TEXT_CODE,
                              insertbackground=ACCENT, relief=tk.FLAT,
                              highlightthickness=1, highlightcolor=ACCENT,
                              highlightbackground=DIVIDER, width=34)
        self.entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), ipady=6)
        self.entry.bind("<Return>", lambda e: self._on_integrate())
        self.entry.bind("<KeyRelease>", self._on_input_change)
        self.entry.focus_set()

        self.integrate_btn = tk.Button(
            input_card, text="INTEGRATE", font=self.font_btn,
            bg=BTN_INT, fg="white", relief=tk.FLAT, padx=14, pady=6,
            activebackground="#3451d1", activeforeground="white",
            cursor="hand2", command=self._on_integrate)
        self.integrate_btn.grid(row=1, column=2, padx=(0, 6))

        tk.Button(input_card, text="CLEAR", font=self.font_btn,
                  bg=BTN_CLR, fg=TEXT_DIM, relief=tk.FLAT, padx=14, pady=6,
                  activebackground="#475569", activeforeground="white",
                  cursor="hand2", command=self._on_clear).grid(row=1, column=3, padx=(0, 6))

        # Copy trail button
        tk.Button(input_card, text="COPY TRAIL", font=self.font_btn,
                  bg=BTN_COPY, fg="white", relief=tk.FLAT, padx=10, pady=6,
                  activebackground="#0d9488", activeforeground="white",
                  cursor="hand2", command=self._on_copy_trail).grid(row=1, column=4)

        input_card.columnconfigure(1, weight=1)

        tk.Label(input_card,
                 text="e.g.  3*x^2    sin(x)    exp(x)    x*sin(x)    3*x^2 + sin(x) - 4/x + exp(x)",
                 font=self.font_status, fg=TEXT_DIM, bg=BG_CARD).grid(
                 row=2, column=0, columnspan=5, sticky="w", pady=(8, 4))

        hist_frame = tk.Frame(input_card, bg=BG_CARD)
        hist_frame.grid(row=3, column=0, columnspan=5, sticky="w", pady=(4, 0))
        tk.Label(hist_frame, text="History:",
                 font=self.font_status, fg=TEXT_DIM, bg=BG_CARD).pack(side=tk.LEFT, padx=(0, 8))
        self.history_var = tk.StringVar(value="")
        self.history_dropdown = ttk.Combobox(
            hist_frame, textvariable=self.history_var,
            font=tkfont.Font(family="Courier New", size=9),
            style="Dark.TCombobox", state="readonly", width=44, values=[])
        self.history_dropdown.pack(side=tk.LEFT)
        self.history_dropdown.bind("<<ComboboxSelected>>", self._on_history_select)

        # ── Result card ────────────────────────────────────────────────────
        result_card = tk.Frame(left, bg=BG_CARD, pady=12, padx=16,
                               highlightbackground=DIVIDER, highlightthickness=1)
        result_card.pack(fill=tk.X, pady=(0, 10))
        tk.Label(result_card, text="RESULT",
                 font=self.font_section, fg=ACCENT, bg=BG_CARD).pack(anchor="w", pady=(0, 6))
        self.answer_var = tk.StringVar(value="—")
        self.answer_label = tk.Label(result_card, textvariable=self.answer_var,
                                     font=self.font_answer, fg=SUCCESS, bg=BG_CARD,
                                     wraplength=1200, justify=tk.LEFT)
        self.answer_label.pack(anchor="w")

        # ── Trail / Audit tab area ──────────────────────────────────────────
        tab_frame = tk.Frame(left, bg=BG_MAIN)
        tab_frame.pack(fill=tk.BOTH, expand=True)

        # Tab buttons
        tab_btn_frame = tk.Frame(tab_frame, bg=BG_MAIN)
        tab_btn_frame.pack(fill=tk.X, pady=(0, 0))

        self._active_tab = tk.StringVar(value="trail")

        self.tab_trail_btn = tk.Button(
            tab_btn_frame, text="SOLUTION TRAIL",
            font=self.font_section, relief=tk.FLAT, padx=16, pady=6,
            bg=ACCENT, fg=BG_MAIN, cursor="hand2",
            command=lambda: self._switch_tab("trail"))
        self.tab_trail_btn.pack(side=tk.LEFT, padx=(0, 2))

        self.tab_audit_btn = tk.Button(
            tab_btn_frame, text="AUDIT LOG",
            font=self.font_section, relief=tk.FLAT, padx=16, pady=6,
            bg=BG_PANEL, fg=TEXT_DIM, cursor="hand2",
            command=lambda: self._switch_tab("audit"))
        self.tab_audit_btn.pack(side=tk.LEFT)

        # Clear audit log button
        tk.Button(tab_btn_frame, text="CLEAR LOG",
                  font=self.font_section, relief=tk.FLAT, padx=12, pady=6,
                  bg=BTN_CLR, fg=TEXT_DIM, cursor="hand2",
                  command=self._on_clear_log).pack(side=tk.RIGHT, padx=(0, 0))

        # Trail text
        trail_card = tk.Frame(tab_frame, bg=BG_CARD,
                              highlightbackground=DIVIDER, highlightthickness=1)
        trail_card.pack(fill=tk.BOTH, expand=True)

        trail_inner = tk.Frame(trail_card, bg=BG_CARD, padx=8)
        trail_inner.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self.trail_text = tk.Text(
            trail_inner, font=self.font_trail,
            bg=BG_PANEL, fg=TEXT_MAIN,
            insertbackground=ACCENT, relief=tk.FLAT,
            wrap=tk.NONE, state=tk.DISABLED,
            padx=12, pady=10,
            selectbackground=BTN_INT, selectforeground="white")
        self.trail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(trail_inner, command=self.trail_text.yview,
                                bg=BG_PANEL, troughcolor=BG_MAIN,
                                activebackground=ACCENT)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trail_text.configure(yscrollcommand=v_scroll.set)

        h_scroll = tk.Scrollbar(trail_card, orient=tk.HORIZONTAL,
                                command=self.trail_text.xview,
                                bg=BG_PANEL, troughcolor=BG_MAIN)
        h_scroll.pack(fill=tk.X, padx=8, pady=(0, 6))
        self.trail_text.configure(xscrollcommand=h_scroll.set)

        # Text tags
        self.trail_text.tag_configure("header",  foreground=ACCENT,    font=self.font_btn)
        self.trail_text.tag_configure("rule",     foreground="#a78bfa")
        self.trail_text.tag_configure("result",   foreground=SUCCESS)
        self.trail_text.tag_configure("note",     foreground="#fbbf24")
        self.trail_text.tag_configure("error",    foreground=ERROR_COL)
        self.trail_text.tag_configure("verify",   foreground=SUCCESS)
        self.trail_text.tag_configure("dim",      foreground=TEXT_DIM)
        self.trail_text.tag_configure("audit_pass", foreground=SUCCESS)
        self.trail_text.tag_configure("audit_err",  foreground=ERROR_COL)

        # ── RIGHT — Calculator panel ───────────────────────────────────────
        self._build_calc_panel(body)

    def _build_calc_panel(self, parent):
        calc = tk.Frame(parent, bg=BG_PANEL,
                        highlightbackground=ACCENT, highlightthickness=1)
        calc.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 16), pady=12)
        tk.Label(calc, text="  INPUT HELPER  ",
                 font=self.font_section, fg=ACCENT, bg=BG_PANEL, pady=8).pack(fill=tk.X)
        tk.Frame(calc, bg=ACCENT, height=1).pack(fill=tk.X, padx=8)

        btn_area = tk.Frame(calc, bg=BG_PANEL, padx=8, pady=8)
        btn_area.pack()

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
                tk.Label(btn_area, text="─── numbers & ops ───",
                         font=tkfont.Font(family="Arial", size=8),
                         fg=TEXT_DIM, bg=BG_PANEL).pack(pady=(6, 2))
                continue
            row_frame = tk.Frame(btn_area, bg=BG_PANEL)
            row_frame.pack(fill=tk.X, pady=1)
            for label, insert in row_data:
                is_op = insert in ("+", "-", "*", "/", "^", "DEL")
                is_fn = insert in ("sin(x)","cos(x)","tan(x)","exp(x)","log(x)","sqrt(x)")
                bg_col = ERROR_COL if insert == "DEL" else \
                         ACCENT2   if is_fn            else \
                         BTN_INT   if is_op            else \
                         BG_CARD
                tk.Button(row_frame, text=label, font=self.font_calc,
                          width=5, pady=5, relief=tk.FLAT, bd=0,
                          bg=bg_col, fg="white",
                          activebackground=ACCENT, activeforeground=BG_MAIN,
                          cursor="hand2",
                          command=lambda ins=insert: self._calc_insert(ins)
                          ).pack(side=tk.LEFT, padx=1)

    # ── Tab switching ───────────────────────────────────────────────────────

    def _switch_tab(self, tab: str):
        self._active_tab.set(tab)
        if tab == "trail":
            self.tab_trail_btn.configure(bg=ACCENT, fg=BG_MAIN)
            self.tab_audit_btn.configure(bg=BG_PANEL, fg=TEXT_DIM)
        else:
            self.tab_trail_btn.configure(bg=BG_PANEL, fg=TEXT_DIM)
            self.tab_audit_btn.configure(bg=BTN_LOG, fg="white")
            self._refresh_audit_view()

    def _refresh_audit_view(self):
        """Renders the audit log into the text widget."""
        self.trail_text.configure(state=tk.NORMAL)
        self.trail_text.delete("1.0", tk.END)
        log_text = self._audit.get_log_text()
        for line in log_text.splitlines(keepends=True):
            stripped = line.strip()
            if "AUDIT LOG" in stripped or stripped.startswith("---"):
                self.trail_text.insert(tk.END, line, "header")
            elif "PASS" in stripped:
                self.trail_text.insert(tk.END, line, "audit_pass")
            elif "ERROR" in stripped:
                self.trail_text.insert(tk.END, line, "audit_err")
            elif stripped.startswith("Total") or stripped.startswith("Passed") or stripped.startswith("Errors"):
                self.trail_text.insert(tk.END, line, "dim")
            else:
                self.trail_text.insert(tk.END, line)
        self.trail_text.configure(state=tk.DISABLED)
        self.trail_text.see("1.0")

    # ── Actions ─────────────────────────────────────────────────────────────

    def _calc_insert(self, text):
        if text == "DEL":
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
        if raw in self._history:
            self._history.remove(raw)
        self._history.insert(0, raw)
        self._history = self._history[:5]
        self.history_dropdown.configure(values=self._history)

    def _on_history_select(self, event=None):
        selected = self.history_var.get()
        if selected:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected)
            self.entry.focus_set()
            self._on_input_change()
            self.history_dropdown.selection_clear()

    def _on_input_change(self, event=None):
        if event and event.keysym in (
            "Shift_L","Shift_R","Control_L","Control_R",
            "Alt_L","Alt_R","Caps_Lock","Tab",
            "Left","Right","Up","Down","Home","End"
        ):
            return
        self.answer_var.set("—")
        self.answer_label.configure(fg=SUCCESS)
        if self._active_tab.get() == "trail":
            self._set_trail("")
        self._set_status("● Ready", TEXT_DIM)

    def _on_integrate(self):
        raw = self.entry.get()

        is_valid, err_msg, expr = validate_input(raw)
        if not is_valid:
            self._show_error(err_msg)
            self._audit.record(raw, "", False, err_msg.splitlines()[0])
            return

        self.integrate_btn.configure(state=tk.DISABLED, text="WORKING...")
        self._set_status("● Computing...", "#fbbf24")
        self.update_idletasks()

        try:
            antiderivative = compute_integral(expr)
        except ValueError as e:
            self._show_error(str(e))
            self._audit.record(raw, "", False, str(e).splitlines()[0])
            return
        except Exception as e:
            self._show_error(f"Unexpected error: {e}")
            self._audit.record(raw, "", False, str(e))
            return
        finally:
            self.integrate_btn.configure(state=tk.NORMAL, text="INTEGRATE")

        try:
            verified, verification_msg = verify(expr, antiderivative)
        except Exception as e:
            verification_msg = f"Verification failed: {e}"
            verified = False

        try:
            trail = build_trail(expr, antiderivative, verification_msg)
        except Exception as e:
            trail = f"Error building trail: {e}"

        result_str = f"{fmt(antiderivative)} + C"
        self._update_history(raw)
        self._audit.record(raw, result_str, verified)

        self.answer_var.set(f"∫ ( {fmt(expr)} ) dx   =   {fmt(antiderivative)}  +  C")
        self.answer_label.configure(fg=SUCCESS)
        self._set_status("● Done", SUCCESS)

        # Switch to trail tab and show result
        self._switch_tab("trail")
        self._set_trail(trail)

    def _on_clear(self):
        self.entry.delete(0, tk.END)
        self.answer_var.set("—")
        self.answer_label.configure(fg=SUCCESS)
        self._set_status("● Ready", TEXT_DIM)
        self._switch_tab("trail")
        self._set_trail("")
        self.entry.focus_set()

    def _on_copy_trail(self):
        """Copies the current trail content to the clipboard."""
        content = self.trail_text.get("1.0", tk.END).strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self._set_status("● Copied to clipboard", ACCENT)
            self.after(2000, lambda: self._set_status("● Ready", TEXT_DIM))

    def _on_clear_log(self):
        """Clears the audit log."""
        self._audit.clear()
        if self._active_tab.get() == "audit":
            self._refresh_audit_view()
        self._set_status("● Audit log cleared", TEXT_DIM)

    def _show_error(self, message: str):
        self.answer_var.set("⚠  " + message.splitlines()[0])
        self.answer_label.configure(fg=ERROR_COL)
        self._set_status("● Error", ERROR_COL)
        self.integrate_btn.configure(state=tk.NORMAL, text="INTEGRATE")
        self._switch_tab("trail")
        self._set_trail(message, error=True)

    def _set_status(self, text: str, color: str):
        self.status_var.set(text)
        self.status_dot.configure(fg=color)

    def _set_trail(self, text: str, error: bool = False):
        self.trail_text.configure(state=tk.NORMAL)
        self.trail_text.delete("1.0", tk.END)
        if error:
            self.trail_text.insert(tk.END, text, "error")
        else:
            for line in text.splitlines(keepends=True):
                stripped = line.strip()
                if stripped.startswith("---"):
                    self.trail_text.insert(tk.END, line, "dim")
                elif any(stripped.startswith(k) for k in
                         ("GIVEN","STEP","FINAL","VERIFICATION")):
                    self.trail_text.insert(tk.END, line, "header")
                elif stripped.startswith("Rule"):
                    self.trail_text.insert(tk.END, line, "rule")
                elif stripped.startswith("Formula"):
                    self.trail_text.insert(tk.END, line, "rule")
                elif stripped.startswith("Result"):
                    self.trail_text.insert(tk.END, line, "result")
                elif stripped.startswith("Note"):
                    self.trail_text.insert(tk.END, line, "note")
                elif "PASSED" in stripped or "[OK]" in stripped:
                    self.trail_text.insert(tk.END, line, "verify")
                else:
                    self.trail_text.insert(tk.END, line)
        self.trail_text.configure(state=tk.DISABLED)
        self.trail_text.see("1.0")