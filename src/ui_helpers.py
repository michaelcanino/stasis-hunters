# src/ui_helpers.py
import sys
import time

def paginate_lines(text_lines, page_size=6):
    """
    Simple paginator: yields chunks of lines. Pause for -- more -- prompt.
    """
    for i in range(0, len(text_lines), page_size):
        chunk = text_lines[i:i+page_size]
        for l in chunk:
            print(l)
        if i + page_size < len(text_lines):
            input("-- more -- (press Enter) --")

def choice_menu(options):
    """
    options: list of tuples (key, text)
    returns chosen key
    """
    for idx, (key, text) in enumerate(options, start=1):
        print(f"{idx}) {text}")
    print("q) quit  s) save")
    while True:
        c = input("> ").strip().lower()
        if c in ("q", "s"):
            return c
        try:
            i = int(c)
            if 1 <= i <= len(options):
                return options[i-1][0]
        except:
            pass
        print("Invalid choice.")
