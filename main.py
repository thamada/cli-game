#!/usr/bin/env python3
import os
import curses

def main(stdscr):
    # Curses setup
    curses.curs_set(0)
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    left_width = width // 4
    right_width = width - left_width - 1

    # Create windows
    left_win = curses.newwin(height, left_width, 0, 0)
    right_win = curses.newwin(height, right_width, 0, left_width + 1)

    options = [
        "return_your_home",
        "go_to_your_school",
        "go_to_shop"
    ]

    exit_options = [
        "Exit",
        "Cancel"
    ]

    current_row = 0
    current_col = 0
    current_window = 'left'

    while True:
        # Draw window borders
        stdscr.clear()
        stdscr.vline(0, left_width, '|', height)
        stdscr.refresh()

        if current_window == 'left':
            curses.curs_set(1)
            draw_menu(left_win, options, current_row)
            key = left_win.getch()

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
            elif key == 9:  # Tab key
                current_window = 'right'

        elif current_window == 'right':
            curses.curs_set(1)
            draw_menu(right_win, exit_options, current_col, horizontal=True)
            key = right_win.getch()

            if key == curses.KEY_LEFT and current_col > 0:
                current_col -= 1
            elif key == curses.KEY_RIGHT and current_col < len(exit_options) - 1:
                current_col += 1
            elif key == ord('\n'):
                if current_col == 0:  # Exit selected
                    break
                elif current_col == 1:  # Cancel selected
                    current_window = 'left'
            elif key == 9:  # Tab key
                current_window = 'left'

        left_win.refresh()
        right_win.refresh()

def draw_menu(win, options, selected_idx, horizontal=False):
    win.clear()
    if horizontal:
        x_position = 0
        for idx, option in enumerate(options):
            if idx == selected_idx:
                win.addstr(0, x_position, option, curses.A_REVERSE)
            else:
                win.addstr(0, x_position, option)
            x_position += len(option) + 5
    else:
        for idx, option in enumerate(options):
            if idx == selected_idx:
                win.addstr(idx, 0, option, curses.A_REVERSE)
            else:
                win.addstr(idx, 0, option)
    win.refresh()

def create_file(filename, content):
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"\nファイル '{filepath}' が作成されました。")

if __name__ == "__main__":
    curses.wrapper(main)
