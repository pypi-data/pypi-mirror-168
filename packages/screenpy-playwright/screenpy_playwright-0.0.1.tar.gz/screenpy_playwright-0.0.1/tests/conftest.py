from unittest import mock

import pytest
from playwright.sync_api import Browser
from screenpy import AnActor

from screenpy_playwright.abilities import BrowseTheWebSynchronously


@pytest.fixture(scope="function")
def Tester() -> AnActor:
    """Provide an Actor with mocked web browsing abilities."""
    BrowseTheWeb_Mocked = mock.Mock(spec=BrowseTheWebSynchronously)
    BrowseTheWeb_Mocked.pages = []
    BrowseTheWeb_Mocked.current_page = None
    BrowseTheWeb_Mocked.browser = mock.Mock(spec=Browser)

    return AnActor.named("Tester").who_can(BrowseTheWeb_Mocked)
