import sys

from menu import main_menu
if __name__ == "__main__":

    # USE_PYGAME = True
    # BOARD_SIZE = 10

    # if USE_PYGAME:
    #     run_pygame(board_size=BOARD_SIZE, cell_size=32, fps=8)
    ret = main_menu()
    if ret == -1:
        sys.exit(0)
