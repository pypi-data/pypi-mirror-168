import os

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import BrowseTheWebSynchronously


class Open:
    """Go to a specific URL!

    This Action supports using the BASE_URL environment variable to
    set a base URL. If you set BASE_URL, the url passed in to this
    Action will be appended to the end of it. For example, if you
    have ``BASE_URL=http://localhost``, then ``Open("/home")`` will send
    your browser to "http://localhost/home".

    If you pass in an object, make sure the object has a ``url`` property
    that can be referenced by this Action.

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(Open("https://www.nintendo.com/"))
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Visit {self.url}"

    @beat("{} visits {url}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to Open a webpage."""
        browse_the_web = the_actor.ability_to(BrowseTheWebSynchronously)
        page = browse_the_web.browser.new_page()
        page.goto(self.url)
        browse_the_web.current_page = page
        browse_the_web.pages.append(page)

    def __init__(self, location: str) -> "Open":
        url = getattr(location, "url", location)
        url = f'{os.getenv("BASE_URL", "")}{url}'
        self.url = url
