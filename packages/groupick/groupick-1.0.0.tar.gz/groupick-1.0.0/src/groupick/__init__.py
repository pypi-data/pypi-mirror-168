import curses
import functools
from dataclasses import dataclass, field
from typing import (Any, Dict, Generic, List, Optional, Sequence, Set, Tuple,
                    TypeVar)

__all__ = ["Picker", "groupick", "Option"]


@dataclass
class Option:
    label: str
    value: Any


# Key consts moved to within run_loop

OPTION_T = TypeVar("OPTION_T", str, Option)
PICK_RETURN_T = Tuple[OPTION_T, int]


@dataclass
class Picker(Generic[OPTION_T]):
    options: Sequence[OPTION_T]
    groups: Set[int|str]
    instructions: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    handle_all: bool = False
    selected_indexes: Dict[str,List[int]] = field(init=False, default_factory=dict)
    index: int = field(init=False, default=0)
    scroll_top: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        if len(self.options) == 0:
            raise ValueError("options should not be an empty list")

        if self.default_index >= len(self.options):
            raise ValueError("default_index should be less than the length of options")

        for g in self.groups:
            g = str(g)
            if len(g) != 1:
                raise ValueError("groups must be exactly one character each")
            self.selected_indexes[g] = []

        self.index = self.default_index

    def move_up(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self) -> None:
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def mark_index(self,keypress) -> None:
        grp = self.selected_indexes.get(chr(keypress))
        
        if grp is not None:
            if self.index in grp:
                grp.remove(self.index)
            else:
                for k in self.selected_indexes.keys():
                    try:
                        kgrp = self.selected_indexes.get(k)
                        if kgrp is not None:
                            kgrp.remove(self.index)
                    except:
                        pass
                grp.append(self.index)

    def get_selected(self) -> Dict[str, List[PICK_RETURN_T]]:
        """return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """

        return_groups:dict = {}
        for k in self.selected_indexes.keys():
            return_groups[k] = []
            grp = self.selected_indexes.get(k)
            if grp is not None:
                for selected in grp:
                    return_groups[k].append((self.options[selected], selected))
        return return_groups

    def get_title_lines(self) -> List[str]:
        if self.instructions:
            return self.instructions.split("\n") + [""]
        return []

    def get_option_lines(self) -> List[str]:
        lines: List[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            for k in self.selected_indexes.keys():
                if index in self.selected_indexes[k]:
                    symbol = f"[{k}]"
                    break
                else:
                    symbol = "[ ]"
            prefix = f"{prefix} {symbol} "

            option_as_str = option.label if isinstance(option, Option) else option
            lines.append(f"{prefix} {option_as_str}")

        return lines

    def get_lines(self) -> Tuple[List, int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, screen) -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        if current_line <= self.scroll_top:
            self.scroll_top = 0
        elif current_line - self.scroll_top > max_rows:
            self.scroll_top = current_line - max_rows

        lines_to_draw = lines[self.scroll_top : self.scroll_top + max_rows]

        for line in lines_to_draw:
            screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()

    def run_loop(self, screen) -> Optional[Dict[str, List[PICK_RETURN_T]]]:
        KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
        KEYS_UP = (curses.KEY_UP, ord("k"))
        KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
        KEYS_SELECT = [ord(str(x)) for x in self.groups]
        KEYS_ESC = (curses.KEY_BACKSPACE,curses.KEY_LEFT)

        while True:
            self.draw(screen)
            c = screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                total_selected = functools.reduce(lambda total,k: total + len(self.selected_indexes[k]), self.selected_indexes, 0)
                
                if (
                    self.handle_all
                    and total_selected < len(self.options)
                ):
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT:
                self.mark_index(c)
            elif c in KEYS_ESC:
                return None

    def config_curses(self) -> None:
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen):
        self.config_curses()
        return self.run_loop(screen)

    def start(self):
        return curses.wrapper(self._start)


def groupick(
    options: Sequence[OPTION_T],
    groups: Set[int|str],
    instructions: Optional[str] = None,
    indicator: str = "*",
    default_index: int = 0,
    handle_all: bool = False,
):
    picker: Picker = Picker(
        options,
        groups,
        instructions,
        indicator,
        default_index,
        handle_all,
    )
    return picker.start()
