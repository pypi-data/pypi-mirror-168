from screenpy import Actor
from screenpy.pacing import beat

from ..target import Target


class Number:
    """Get how many of an element are on the page.

    Examples::

        the_actor.should(See.the(Number.of(CONFETTI), IsEqualTo(10)))
    """

    @staticmethod
    def of(target: Target) -> "Number":
        return Number(target)

    def describe(self) -> str:
        """Describe the Question."""
        return f"The number of {self.target}."

    @beat("{} examines the Number of the {target}.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to read the Number from the target."""
        return self.target.found_by(the_actor).count()

    def __init__(self, target: Target) -> None:
        self.target = target
