from screenpy.protocols import Answerable, Describable

from screenpy_playwright.questions import Number, Text

from .useful_mocks import get_mocked_target_and_element


class TestNumber:
    def test_can_be_instantiated(self):
        n = Number.of(None)

        assert isinstance(n, Number)

    def test_implements_protocol(self):
        n = Number(None)

        assert isinstance(n, Answerable)
        assert isinstance(n, Describable)

    def test_describe(self):
        target, _ = get_mocked_target_and_element()
        target._description = "Somebody once told me"

        assert Number.of(target).describe() == f"The number of {target}."

    def test_ask_number(self, Tester):
        target, element = get_mocked_target_and_element()
        num_elements = 10
        element.count.return_value = num_elements

        assert Number.of(target).answered_by(Tester) == num_elements


class TestText:
    def test_can_be_instantiated(self):
        t = Text.of_the(None)

        assert isinstance(t, Text)

    def test_implements_protocol(self):
        t = Text(None)

        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_describe(self):
        target, _ = get_mocked_target_and_element()
        target._description = "the world is gonna roll me"

        assert Text.of_the(target).describe() == f"The text from the {target}."

    def test_ask_text(self, Tester):
        target, element = get_mocked_target_and_element()
        words = "Number 1, the larch."
        element.text_content.return_value = words

        assert Text.of_the(target).answered_by(Tester) == words
