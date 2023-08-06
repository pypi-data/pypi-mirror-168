from typing import Optional

from screenpy import Actor
from playwright.sync_api import Locator

from .abilities import BrowseTheWebSynchronously
from .exceptions import TargetingError


class Target:
    """A described element on a webpage.

    Examples::

        Target.the('"Log In" button').located_by("button:has-text('Log In')")

        Target.the("toast message").located_by("//toast")

        Target.the('"Pick up Milk" todo item").located_by(
            "_vue=list-item[text *= 'milk' i]"
        )

        Target().located_by("#enter-todo-field")
    """

    @staticmethod
    def the(name: str) -> "Target":
        """Provide a human-readable description of the target."""
        return Target(name)

    def located_by(self, locator: str) -> "Target":
        """Provide the Playwright locator which describes the element."""
        self.locator = locator
        return self

    @property
    def target_name(self):
        return self._description if self._description is not None else self.locator

    @target_name.setter
    def target_name(self, value):
        self._description = value

    @target_name.deleter
    def target_name(self):
        del self._description

    def found_by(self, the_actor: Actor) -> Locator:
        browse_the_web = the_actor.ability_to(BrowseTheWebSynchronously)
        if browse_the_web.current_page is None:
            raise TargetingError(
                #                          v              deep              v
                f"There is no active page! {the_actor} cannot find the {self}."
            )

        return browse_the_web.current_page.locator(self.locator)

    def __repr__(self) -> str:
        return self.target_name

    def __init__(self, name: Optional[str] = None) -> None:
        self._description = name
        self.locator = None
