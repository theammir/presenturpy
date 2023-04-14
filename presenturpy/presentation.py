import os
import re
import sys
import time
import typing

from .misc import Alignment
from .slide import Slide, SlideBuilder


def wait_key() -> str:
    """Wait for a key press on the console and return it."""
    result: str
    if os.name == "nt":
        import msvcrt

        result = msvcrt.getwch()
    else:
        import termios

        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def clear() -> int:
    return os.system("cls") if sys.platform == "win32" else os.system("clear")


SLIDE_REGEX = r"\s*(\d+[.,]?\d*)?\s*(?:s|sec|seconds)?\s+```([r|l][d|u])\s*([-~]?\d+|[lmrud]);([-~]?\d+|[lmrud]);?(-?\d+)?\s([\S\s]*?)(?:\n)```(\+|-)?"
PLACEMENT_FUNCTIONS: dict[str, typing.Callable[..., SlideBuilder]] = {
    "lu": SlideBuilder.add_text_lu,
    "ld": SlideBuilder.add_text_ld,
    "ru": SlideBuilder.add_text_ru,
    "rd": SlideBuilder.add_text_rd,
}


class Presentation:
    def __init__(self, slides: list[Slide]) -> None:
        self.slides = slides

    def show(self) -> None:
        clear()
        for slide in self.slides:
            print(slide.text)

            try:
                if slide.needs_confirmaion:
                    wait_key()
                if slide.duration:
                    time.sleep(slide.duration)
            except KeyboardInterrupt:
                return

        # wait_key()
        clear()

    @staticmethod
    def load_from_file(path: str) -> "Presentation":
        def process_pos(pos: str) -> int:
            if pos.startswith("~"):
                return Alignment.from_tilde_string(pos)
            if pos in "lmrud":
                return Alignment.from_direction_letter(pos)
            else:
                return int(pos)

        with open(path, "r", encoding="utf-8") as f:
            slide_list = []
            text = f.read()
            slide_text = text.split("---")

            for slide in slide_text:
                builder = SlideBuilder()

                duration = 0.0
                needs_confirmation = True
                for index, match in enumerate(
                    re.finditer(SLIDE_REGEX, slide, re.MULTILINE | re.IGNORECASE)
                ):
                    placement_func = PLACEMENT_FUNCTIONS[match.group(2)]
                    pos = (process_pos(match.group(3)), process_pos(match.group(4)))
                    side_indentation_count = int(match.group(5) or 0)
                    text = match.group(6)
                    transition = match.group(7) == "+"
                    if index == 0:
                        duration = float(match.group(1) or 0)
                        needs_confirmation = duration == 0

                    builder = (
                        placement_func(
                            builder,
                            text,
                            pos,
                            transition=transition,
                            side_indentation_count=side_indentation_count,
                        )
                        .set_duration(duration)
                        .set_confirmation(needs_confirmation)
                    )
                slide_list.append(builder.build())

            return Presentation(slide_list)
