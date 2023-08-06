from screenpy import Actor
from screenpy.pacing import beat

from ..target import Target


class Text:
    """Get the text from a target.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!"))
        )
    """

    @staticmethod
    def of_the(target: Target) -> "Text":
        return Text(target)

    def describe(self) -> str:
        """Describe the Question."""
        return f"The text from the {self.target}."

    @beat("{} examines the text of the {target}.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to read the text from the target."""
        return self.target.found_by(the_actor).text_content()

    def __init__(self, target: Target) -> None:
        self.target = target
