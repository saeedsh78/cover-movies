# Shared progress/cancel plumbing so helper modules can report to the GUI
# without importing each other (avoids a circular import).

_progress_cb = None    # fn(status_key, detail, current, total)
_check_cancel = None   # fn() -> bool


class CancelledError(Exception):
    pass


def set_progress_cb(cb):
    global _progress_cb
    _progress_cb = cb


def set_cancel_checker(fn):
    global _check_cancel
    _check_cancel = fn


def report(status_key, detail="", current=0, total=0):
    if _progress_cb:
        try:
            _progress_cb(status_key, detail, current, total)
        except Exception:
            pass


def check_cancelled():
    if _check_cancel and _check_cancel():
        raise CancelledError()
