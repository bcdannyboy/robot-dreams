# emotion.py
import curses
import time
import random
import math


def pulse(t):
    return 0.5 + 0.5 * math.sin(t * 2.1)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        for i in range(1, 8):
            curses.init_pair(i, i, -1)

    text = "TREPIDATION"
    start = time.time()

    while True:
        now = time.time()
        dt = now - start

        amp = 1 + pulse(dt) * 4
        jitter_x = int(random.gauss(0, amp))
        jitter_y = int(random.gauss(0, amp))

        h, w = stdscr.getmaxyx()
        y = max(0, min(h - 1, h // 2 + jitter_y))
        x = max(0, min(w - len(text) - 1, w // 2 - len(text) // 2 + jitter_x))

        stdscr.erase()

        if curses.has_colors():
            idx = max(1, min(7, int(amp)))
            stdscr.attron(curses.color_pair(idx))

        stdscr.addstr(y, x, text)

        if curses.has_colors():
            stdscr.attroff(curses.color_pair(idx))

        stdscr.refresh()

        if random.random() < 0.03 * pulse(dt):
            curses.flash()
            curses.beep()

        time.sleep(0.05)

        ch = stdscr.getch()
        if ch in (ord('q'), ord('Q')):
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
