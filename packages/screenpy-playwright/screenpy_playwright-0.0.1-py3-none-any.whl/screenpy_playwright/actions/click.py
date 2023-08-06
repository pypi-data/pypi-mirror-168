from screenpy import Actor
from screenpy.pacing import beat

from ..target import Target


class Click:
    """Click on an element!

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(Click.on_the(LOG_IN_BUTTON))
    """

    @staticmethod
    def on_the(target: Target) -> "Click":
        """Specify the element on which to click."""
        return Click(target)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Click on the {self.target}."

    @beat("{} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to click on the element."""
        self.target.found_by(the_actor).click()

    def __init__(self, target: Target) -> None:
        self.target = target
