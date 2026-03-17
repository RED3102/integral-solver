import sys

try:
    import sympy  # noqa: F401
except ImportError:
    print("SymPy is not installed. Run: pip install sympy")
    sys.exit(1)

from ui.app_ui import IntegrationApp

if __name__ == "__main__":
    app = IntegrationApp()
    app.update_idletasks()
    w, h = 750, 620
    x = (app.winfo_screenwidth()  - w) // 2
    y = (app.winfo_screenheight() - h) // 2
    app.geometry(f"{w}x{h}+{x}+{y}")
    app.mainloop()