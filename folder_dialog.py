"""Native folder picker for local Streamlit runs (desktop only)."""

from __future__ import annotations


def pick_folder_path() -> str | None:
    """
    Open the OS folder-selection dialog.

    Works when Streamlit runs on **your PC** (same session as the browser). On a **remote**
    or headless server there is no display — returns None and the UI should fall back to typing.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        return None

    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except tk.TclError:
            pass
        try:
            root.update_idletasks()
        except tk.TclError:
            pass

        path = filedialog.askdirectory(
            title="Select folder containing PDFs",
            parent=root,
        )
        return path if path else None
    except Exception:
        return None
    finally:
        if root is not None:
            try:
                root.destroy()
            except tk.TclError:
                pass
