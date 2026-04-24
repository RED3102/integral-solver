from datetime import datetime


class AuditLog:
    """
    Maintains a running log of all integration attempts in the current session.
    Each entry records the input, result, verification status, and timestamp.
    """

    def __init__(self):
        self._entries = []

    def record(self, raw_input: str, result: str, verified: bool, error: str = ""):
        """
        Records a computation attempt.

        Parameters
        ----------
        raw_input : str   The raw expression the user entered.
        result    : str   The formatted result string, or empty on error.
        verified  : bool  Whether verification passed.
        error     : str   Error message if computation failed, else empty.
        """
        self._entries.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "input":     raw_input,
            "result":    result,
            "verified":  verified,
            "error":     error,
        })

    def get_log_text(self) -> str:
        """Returns the full audit log as a formatted plain-text string."""
        if not self._entries:
            return "No computations recorded yet."

        divider = "-" * 55
        lines = [divider, "SESSION AUDIT LOG", divider, ""]

        for i, entry in enumerate(self._entries, start=1):
            status = "ERROR" if entry["error"] else ("PASS" if entry["verified"] else "UNVERIFIED")
            lines.append(f"  [{i}]  {entry['timestamp']}  |  Status: {status}")
            lines.append(f"       Input  : {entry['input']}")
            if entry["error"]:
                lines.append(f"       Error  : {entry['error']}")
            else:
                lines.append(f"       Result : {entry['result']}")
            lines.append("")

        lines.append(divider)
        lines.append(f"  Total entries : {len(self._entries)}")
        passed  = sum(1 for e in self._entries if e["verified"] and not e["error"])
        errors  = sum(1 for e in self._entries if e["error"])
        lines.append(f"  Passed        : {passed}")
        lines.append(f"  Errors        : {errors}")
        lines.append(divider)

        return "\n".join(lines)

    def clear(self):
        """Clears all entries from the log."""
        self._entries = []

    @property
    def count(self) -> int:
        return len(self._entries)