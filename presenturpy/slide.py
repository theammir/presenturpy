import shutil

from .misc import Alignment


class Slide:
    def __init__(self, text: str, **kwargs) -> None:
        """
        Represents a single presentation slide.

        @param duration: float - duration of the slide in seconds.
        @param needs_confirmaion: bool - requires a keypress to continue.
        """
        self.text = text
        self.duration = kwargs.get("duration")
        self.needs_confirmaion = kwargs.get("needs_confirmaion", not self.duration)

    def __str__(self):
        return f"<Slide: {len(self.text)} letters, {self.duration} seconds, {'needs' if self.needs_confirmaion else 'does not need'} confirmation>"

    __repr__ = __str__


class SlideBuilder:
    def __init__(self):
        self._termsize = shutil.get_terminal_size()

        self.strings: list[str] = [" " * self._termsize[0]] * self._termsize[1]
        self.__duration: float = 3
        self.__needs_confirmaion: bool = False

    def _add_text(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
        _transition_count: int = 0,
    ) -> "SlideBuilder":
        abs_pos = position
        abs_pos = tuple(
            self._termsize[index] + element
            if element < 0 and element not in Alignment.__dict__.values()
            else element
            for index, element in enumerate(abs_pos)
        )

        for index, line in enumerate(text.split("\n")):
            line = " " * side_indentation_count + line
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

            if (abs_pos[1] + index + _transition_count) > (len(self.strings) - 1):
                return self

            edited_line = self.strings[abs_pos[1] + index + _transition_count]

            rest_len = -min(0, len(edited_line) - abs_pos[0] - len(line))

            edited_line = (
                edited_line[: abs_pos[0]]
                + line[: len(line) - rest_len - side_indentation_count]
                + edited_line[abs_pos[0] + len(line):]
            )

            self.strings[abs_pos[1] + index + _transition_count] = edited_line
            if transition:
                self._add_text(
                    line[len(line) - rest_len - side_indentation_count:],
                    (position[0] if position[0] < 0 else 0, abs_pos[1] + index + 1),
                    transition,
                    _transition_count=_transition_count,
                )
                _transition_count += 1

        return self

    add_text_lu = _add_text
    add_text = add_text_lu

    def add_text_ld(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self._add_text(
            text,
            (
                position[0],
                position[1]
                if position[1] < 0 and position[1] in Alignment.__dict__.values()
                else position[1] - (len(text.split("\n")) - 1),
            ),
            transition,
            side_indentation_count=side_indentation_count,
        )

    def add_text_ru(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self._add_text(
            text,
            (
                position[0]
                if position[0] < 0 and position[0] in Alignment.__dict__.values()
                else position[0] - (len(text.split("\n")[0]) - 1),
                position[1],
            ),
            transition,
            side_indentation_count=side_indentation_count,
        )

    def add_text_rd(
        self,
        text: str,
        position: tuple[int, int],
        transition: bool = False,
        side_indentation_count: int = 0,
    ) -> "SlideBuilder":
        return self._add_text(
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
            side_indentation_count=side_indentation_count,
        )

    @property
    def duration(self):
        return self.__duration

    def set_duration(self, value: float) -> "SlideBuilder":
        self.__duration = value
        return self

    @property
    def needs_confirmaion(self):
        return self.__needs_confirmaion

    def set_confirmation(self, value: bool) -> "SlideBuilder":
        self.__needs_confirmaion = value
        return self

    def build(self) -> Slide:
        return Slide(
            "\n".join(self.strings),
            duration=self.duration,
            needs_confirmaion=self.needs_confirmaion,
        )
