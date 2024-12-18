#!/usr/bin/env python3
import os
import curses

def main(stdscr):
    # Curses setup
    curses.curs_set(1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    left_width = width // 4
    right_width = width - left_width - 1
    bottom_height = 15

    # Create windows
    left_win = curses.newwin(height - bottom_height - 1, left_width, 0, 0)
    right_win = curses.newwin(height - bottom_height - 1, right_width, 0, left_width + 1)
    bottom_win = curses.newwin(bottom_height, width, height - bottom_height, 0)

    options = [
        "1. return_your_home",
        "2. go_to_your_school",
        "3. go_to_shop"
    ]

    descriptions = [
        "This option will take you back to your home.",
        "This option will take you to your school.",
        "This option will take you to the shop."
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
        stdscr.vline(0, left_width, '|', height - bottom_height - 1)
        stdscr.hline(height - bottom_height - 1, 0, '-', width)
        stdscr.refresh()

        if current_window == 'left':
            curses.curs_set(1)
            left_win.clear()
            draw_menu(left_win, options, current_row)
            left_win.move(current_row, 0)
            left_win.refresh()

            # Display description in the right window
            right_win.clear()
            right_win.addstr(0, 0, descriptions[current_row])
            right_win.refresh()

            # Display current selection in the bottom window
            bottom_win.clear()
            bottom_win.addstr(0, 0, f"Current selection: {current_row + 1}")
            bottom_win.refresh()

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
            elif key == 9:  # Tab key
                current_window = 'right'
            elif key == 27:  # ESC key
                current_window = 'right'
                current_col = 0

        elif current_window == 'right':
            curses.curs_set(1)
            right_win.clear()
            draw_menu(right_win, exit_options, current_col, horizontal=True)
            right_win.move(0, current_col * 10)
            right_win.refresh()
            key = stdscr.getch()

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

