import logging
import os
from rich import print
# import logging


def load_bookmarks_from_file(filename: str) -> list[tuple[int, str, int]]:
    """
    This parses the file to get the data of the bookmarks
    It also performs (some) checks to ensure it is valid data

    Structure of files:
    - comments are written with `#` at the beginning of a line
    - the command word `SHIFTAMOUNT` at the beginning of a line tells the program what
      page to shift all of the bookmarks by.

      In the future, this should also shift the page numbers, but I couldn't get this
      to work at the moment

    - The program strictly uses 4 spaces for indents!!
    """

    # page number, then bookmark name, then indent value (SPACES)
    data: list[tuple[int, str, int]] = []

    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            _ = file.write("")

        print(f"Failed to read from file {filename}")
        print("Enter the data into the file 'bookmark_data.txt'")
        raise FileNotFoundError

    with open(filename, "r", encoding="UTF-8") as file:
        shift_page_numbers: int = 0

        while current_line := file.readline():
            current_line = (
                current_line.rstrip()
            )  # CHECK WHY THIS LINE CAN'T BE MERGED WITH THE PREVIOUS

            if current_line.strip() == "" or current_line.strip().startswith("#"):
                # blank lines are okay, and comments start with #
                continue
            if current_line.lstrip().startswith("SHIFTAMOUNT"):
                shift_page_numbers = int(current_line.strip().split()[1])
                continue

            # print(current_line)

            line_split_at_comma: list[str] = [
                x.strip() for x in current_line.strip().rsplit(",", 1)
            ]

            data.append(
                (
                    int(line_split_at_comma[1]) - 1 + shift_page_numbers,
                    # as the first page is position "0" in the program
                    line_split_at_comma[0],
                    len(current_line.split(line_split_at_comma[0], 1)[0])
                    // 4,  # CHECK IF THIS WORKS!! (for 4 spaced indents)
                )
            )

    # print(data)
    return data
