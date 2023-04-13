import os
import re
import sys
import time

from .slide import Slide, SlideBuilder


def wait_key():
    """Wait for a key press on the console and return it."""
    result = None
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


def clear() -> None:
    os.system("cls") if sys.platform == "win32" else os.system("clear")


SLIDE_REGEX = r"\s*(\d+[.,]?\d*)?\s*(?:s|sec|seconds)?\s+```([r|l][d|u])\s*(-?\d+);(-?\d+);?(-?\d+)?\s([\S\s]*?)(?:\n)```(\+|-)?"
PLACEMENT_FUNCTIONS = {
    "lu": SlideBuilder.add_text_lu,
    "ld": SlideBuilder.add_text_ld,
    "ru": SlideBuilder.add_text_ru,
    "rd": SlideBuilder.add_text_rd,
}


class Presentation:
    def __init__(self, slides: list[Slide]):
        self.slides = slides

    def show(self):
        clear()
        for slide in self.slides:
            print(slide.text)

            if slide.needs_confirmaion:
                wait_key()
                continue
            elif slide.duration:
                time.sleep(slide.duration)
                continue

        wait_key()
        clear()

    @staticmethod
    def load_from_file(path: str) -> "Presentation":
        with open(path, "r", encoding="utf-8") as f:
            slide_list = []
            text = f.read()
            slide_text = text.split("---")

            for slide in slide_text:
                builder = SlideBuilder()

                duration = 0
                needs_confirmation = True
                for index, match in enumerate(
                    re.finditer(SLIDE_REGEX, slide, re.MULTILINE)
                ):
                    placement_func = PLACEMENT_FUNCTIONS[match.group(2)]
                    pos = (int(match.group(3)), int(match.group(4)))
                    side_indentation_count = int(match.group(5) or 0)
                    text = match.group(6)
                    transition = True if match.group(7) == "+" else False
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
