"""
Enter text into an input field.
"""

from typing import Optional

from screenpy import Actor
from screenpy.pacing import beat
from screenpy.exceptions import UnableToAct

from ..target import Target


class Enter:
    """Enter text into an input field.

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(Enter("Hello!").into_the(GREETING_INPUT))

        the_actor.attempts_to(Enter.the_text("eggs").into_the(GROCERY_FIELD))

        the_actor.attempts_to(Enter.the_secret("12345").into_the(PASSWORD_FIELD))
    """

    target: Optional[Target]

    @staticmethod
    def the_text(text: str) -> "Enter":
        """Provide the text to enter into the field."""
        return Enter(text)

    @staticmethod
    def the_secret(text: str) -> "Enter":
        """
        Provide the text to enter into the field, but mark that the text
        should be masked in the log. The text will appear as "[CENSORED]".
        """
        return Enter(text, mask=True)

    the_password = the_secret

    def into_the(self, target: Target) -> "Enter":
        """Target the element to enter text into."""
        self.target = target
        return self

    into = into_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f'Enter "{self.text_to_log}" into the {self.target}.'

    @beat('{} enters "{text_to_log}" into the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into(), .into_the(), or into_the_first_of_the() method."
            )

        self.target.found_by(the_actor).fill(self.text)

    def __init__(self, text: str, mask: bool = False) -> None:
        self.text = text
        self.target = None

        if mask:
            self.text_to_log = "[CENSORED]"
        else:
            self.text_to_log = text
