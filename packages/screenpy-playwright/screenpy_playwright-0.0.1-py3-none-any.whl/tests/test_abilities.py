from screenpy.protocols import Forgettable

from screenpy_playwright.abilities import BrowseTheWebSynchronously


class TestBrowseTheWebSynchronously:
    def test_can_be_instantiated(self):
        b = BrowseTheWebSynchronously.using(None, None)

        assert isinstance(b, BrowseTheWebSynchronously)

    def test_implements_protocol(self):
        assert isinstance(BrowseTheWebSynchronously(None, None), Forgettable)
