import sys

from menu import main_menu
if __name__ == "__main__":
    ret = main_menu()
    if ret == -1:
        sys.exit(0)
