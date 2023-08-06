"""
Exceptions thrown by screenpy_playwright.
"""

from screenpy.exceptions import ScreenPyError


class TargetingError(ScreenPyError):
    """There was an issue targeting an element."""
