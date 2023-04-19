import shutil

from .misc import Alignment


class Slide:
    def __init__(self, text: str, duration: float = 3.0, needs_confirmation: bool | None = None) -> None:
        """
        Represents a single presentation slide.

        @param duration: float - duration of the slide in seconds.
        @param needs_confirmation: bool - requires a keypress to continue.
        """
        self.text = text
        self.duration = duration
        self.needs_confirmation = needs_confirmation if needs_confirmation is not None else not self.duration

    def __str__(self) -> str:
        return (
            f"<Slide: {len(self.text)} letters, {self.duration} "
            f"{'needs' if self.needs_confirmation else 'does not need'} confirmation>"
        )

    __repr__ = __str__


class SlideBuilder:
    def __init__(self) -> None:
        self._termsize = shutil.get_terminal_size()

        self.screen_rows: list[str] = [" " * self._termsize[0]] * self._termsize[1]
        self._duration: float = 3
        self._needs_confirmation: bool = False

    def _get_abs_position(self, position: tuple[int, int], line: str, text: str) -> tuple[int, int]:
        abs_pos = tuple(
            self._termsize[index] + element
            if element < 0 and element not in Alignment.__dict__.values()
            else element
            for index, element in enumerate(position)
        )

        match position[0]:
            case Alignment.MIDDLE:
                abs_pos = (
                    max(0, self._termsize[0] // 2 - len(line) // 2),
                    abs_pos[1],
                )

            case Alignment.RIGHT:
                abs_pos = (max(0, self._termsize[0] - len(line)), abs_pos[1])

        match position[1]:
            case Alignment.MIDDLE:
                abs_pos = (
                    abs_pos[0],
                    max(0, self._termsize[1] // 2 - len(text.split("\n")) // 2),
                )

            case Alignment.BOTTOM:
                abs_pos = (
                    abs_pos[0],
                    max(0, self._termsize[1] - len(text.split("\n"))),
                )

        return abs_pos

    def add_text(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation: int = 0,
        _transition_steps: int = 0,
    ) -> "SlideBuilder":
        for index, line in enumerate(text.split("\n")):
            line = " " * side_indentation + line
            abs_pos = self._get_abs_position(position, line, text)

            if (abs_pos[1] + index + _transition_steps) > (len(self.screen_rows) - 1):
                return self

            edited_row = self.screen_rows[abs_pos[1] + index + _transition_steps]

            remaining_len = -min(0, len(edited_row) - abs_pos[0] - len(line))

            edited_row = (
                edited_row[: abs_pos[0]]
                + line[: len(line) - remaining_len - side_indentation]
                + edited_row[abs_pos[0] + len(line):]
            )

            self.screen_rows[abs_pos[1] + index + _transition_steps] = edited_row
            if transition:
                self.add_text(
                    line[len(line) - remaining_len - side_indentation:],
                    (min(position[0], 0), abs_pos[1] + index + 1),
                    transition,
                    _transition_steps=_transition_steps,
                )
                _transition_steps += 1

        return self

    add_text_lu = add_text

    def add_text_ld(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self.add_text(
            text,
            (
                position[0],
                position[1]
                if position[1] < 0 and position[1] in Alignment.__dict__.values()
                else position[1] - (len(text.split("\n")) - 1),
            ),
            transition,
            side_indentation=side_indentation_count,
        )

    def add_text_ru(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self.add_text(
            text,
            (
                position[0]
                if position[0] < 0 and position[0] in Alignment.__dict__.values()
                else position[0] - (len(text.split("\n")[0]) - 1),
                position[1],
            ),
            transition,
            side_indentation=side_indentation_count,
        )

    def add_text_rd(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self.add_text(
            text,
            (
                position[0]
                if position[0] < 0 and position[0] in Alignment.__dict__.values()
                else position[0] - (len(text.split("\n")[0]) - 1),
                position[1]
                if position[1] < 0 and position[1] in Alignment.__dict__.values()
                else position[1] - (len(text.split("\n")) - 1),
            ),
            transition,
            side_indentation=side_indentation_count,
        )

    @property
    def duration(self) -> float:
        return self._duration

    def set_duration(self, value: float) -> "SlideBuilder":
        self._duration = value
        return self

    @property
    def needs_confirmation(self) -> bool:
        return self._needs_confirmation

    def set_confirmation(self, value: bool) -> "SlideBuilder":
        self._needs_confirmation = value
        return self

    def build(self) -> Slide:
        return Slide(
            "\n".join(self.screen_rows),
            duration=self.duration,
            needs_confirmation=self.needs_confirmation,
        )
