from unittest import mock

from playwright.sync_api import Locator

from screenpy_playwright import Target


def get_mocked_target_and_element():
    """Get a mocked target which finds a mocked element."""
    target = mock.Mock(spec=Target)
    element = mock.Mock(spec=Locator)
    target.found_by.return_value = element

    return target, element
