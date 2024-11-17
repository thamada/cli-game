#!/usr/bin/env python3
import os
import curses

def main(stdscr):
    # Curses setup
    curses.curs_set(0)
    stdscr.clear()

    options = [
        "return_your_home",
        "go_to_your_school",
        "go_to_shop"
    ]

    current_row = 0

    while True:
        stdscr.clear()
        for idx, option in enumerate(options):
            if idx == current_row:
                stdscr.addstr(idx, 0, option, curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, option)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == ord('\n'):
            if current_row == 0:
                create_file("return_your_home.txt", "You chose to return to your home.")
            elif current_row == 1:
                create_file("go_to_your_school.txt", "You chose to go to your school.")
            elif current_row == 2:
                create_file("go_to_shop.txt", "You chose to go to shop.")
            break

    stdscr.refresh()

def create_file(filename, content):
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"\nファイル '{filepath}' が作成されました。")

if __name__ == "__main__":
    curses.wrapper(main)

