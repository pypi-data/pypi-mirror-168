from playwright.sync_api import sync_playwright, Playwright, Browser


class BrowseTheWebSynchronously:
    """Use a synchronous Playwright instance to browse the web.

    Examples::

        the_actor.can(BrowseTheWebSynchronously.using_firefox())

        the_actor.can(BrowseTheWebSynchronously.using_webkit())

        the_actor.can(BrowseTheWebSynchronously.using_chromium())

        the_actor.can(
            BrowseTheWebSynchronously.using(playwright, cust_browser)
        )
    """

    @staticmethod
    def using(playwright: Playwright, browser: Browser) -> "BrowseTheWebSynchronously":
        """Supply a pre-defined Playwright browser to use."""
        return BrowseTheWebSynchronously(playwright, browser)

    @staticmethod
    def using_firefox() -> "BrowseTheWebSynchronously":
        """Use a synchronous Firefox browser."""
        playwright = sync_playwright().start()
        browser = playwright.firefox.launch()
        return BrowseTheWebSynchronously(playwright, browser)

    @staticmethod
    def using_chromium() -> "BrowseTheWebSynchronously":
        """Use a synchronous Chromium (i.e. Chrome, Edge, Opera, etc.) browser."""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        return BrowseTheWebSynchronously(playwright, browser)

    @staticmethod
    def using_webkit() -> "BrowseTheWebSynchronously":
        """Use a synchronous WebKit (i.e. Safari, etc.) browser."""
        playwright = sync_playwright().start()
        browser = playwright.webkit.launch()
        return BrowseTheWebSynchronously(playwright, browser)

    def forget(self) -> None:
        """Forget everything you knew about being a playwright."""
        self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def __init__(self, playwright: Playwright, browser: Browser) -> None:
        self.playwright = playwright
        self.browser = browser
        self.current_page = None
        self.pages = []
