# Presenturpy - a python tool for terminal presentations

[Файл презентації](https://github.com/TheAmmiR/presenturpy/blob/a4a9f5e572c785022a6b793e8b63e5325a46abe1/braille.pres)

## What is it?

A library, coded in 24 hours or so for a school project. Allows to place text blocks in 2D coordinates and make individual slides out of them.
No pip dependencies btw

## Why?

Because check this out:
![image](https://github.com/TheAmmiR/presenturpy/blob/master/screenshots/screenshot1.png?raw=true)
[terminal, default settings](https://github.com/Swordfish90/cool-retro-term)

## Usage

Loading from file (file syntax ↡):

```py
from presenturpy import Presentation

presentation = Presentation.load_from_file("path")
presentation.show()
```

Direct usage:

```py
from presenturpy import Alignment, Presentation, SlideBuilder

slides = []
slides.append(
    SlideBuilder() # (x, y),    (0,0) is upper left
    .add_text("Hello, world!", (Alignment.MIDDLE, Alignment.MIDDLE))
    .set_duration(5) # seconds
    .build()
)
slides.append(
    SlideBuilder()
    .add_text(
        "Thanks for watching!", (Alignment.MIDDLE, Alignment.BOTTOM),
        transition=True 
    )
    .set_confirmation(True)
    .build()
)

# If the final slide has a set duration, the slide will be shown until the time runs out.

presentation = Presentation(slides)
presentation.show()
```

### File syntax

Example file:

```fix
[5[,0|.0] s|sec|seconds]        # Duration, needs confirmation if none

```lu m;10[;0]                  # Pivot corner (the one you write coordinates for) 
Example text                    # (lu|ld|ru|rd)
Because I have to explain       # Side indentation - wraps every line in a number of spaces on each side
a bunch of stuff here           # xpos;ypos - allows negative absolute values.
yeah                            # l|m|r for horizontal alignment, u|m|d for vertical
```+                            # + allows word wrapping if you don't mind having 1 letter of the word on the next line sometimes
                                # If you do, try to adjust side indentation.

---                             # Slide delimiter

# Next slide here

```

___

## To-do (maybe)

- [x] Refactoring (kinda)
- [ ] Even more refactoring
- [ ] Renaming corners
- [ ] Easy slide duplication
