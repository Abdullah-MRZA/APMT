from collections import defaultdict
from datetime import datetime
from pypdf.generic import IndirectObject
import logging
import os
import pypdf
import typer


# def test(teststr: str) -> None:
#     logging.debug(f"{teststr=}")


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

        logging.error(f"Failed to read from file {filename}")
        logging.error("Enter the data into the file 'bookmark_data.txt'")
        # logging.error(
        #     "make sub-bookmarks with indenting, and write ', ...' for the  (at the end)"
        # )
        raise FileNotFoundError

    with open(filename, "r", encoding="UTF-8") as file:
        shift_page_numbers: int = 0

        while current_line := file.readline().rstrip():
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

    return data


def make_pdf_file(
    input_file: str,
    output_file: str,
    copy_metadata: bool,
    bookmark_file_name: str,
) -> None:
    """
    Adds custom bookmarks to the input file,
    to produce an output file with the bookmarks
    """

    reader: pypdf.PdfReader = pypdf.PdfReader(input_file)
    writer: pypdf.PdfWriter = pypdf.PdfWriter(input_file)

    logging.info("Copying files")
    for page in reader.pages:
        _ = writer.add_page(page)

    logging.info("Writing metadata")
    if copy_metadata:
        if (data := reader.metadata) is not None:
            writer.add_metadata(data)
        else:
            print("Original file had no metadata!")
    else:
        writer.add_metadata(  # Check how well this works
            {
                "/Author": "Abdullah Mirza",
                "/Producer": "APMT manipulation software",
                # "/Title": "Title",
                # "/Subject": "Subject",
                # "/Keywords": "Keywords",
                "/CreationDate": datetime.now().strftime(
                    f"D\072%Y%m%d%H%M%S{"-05'00'"}"
                ),
                # "/ModDate": time,
                # "/Creator": "Creator",
                # "/CustomField": "CustomField",
            }
        )

    logging.info("Adding bookmarks to output file")
    bookmarks = load_bookmarks_from_file(bookmark_file_name)

    bookmark_parents: defaultdict[int, IndirectObject] = defaultdict()

    for current_bookmark in bookmarks:
        parent_bookmark = (
            bookmark_parents[current_bookmark[2] - 1]
            if current_bookmark[2] != 0
            else None
        )

        # This has a bug!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # now that I changed it, check if it still does...
        bookmark_parents[current_bookmark[2]] = writer.add_outline_item(
            title=current_bookmark[1],
            page_number=current_bookmark[0],
            parent=parent_bookmark,
        )

    with open(output_file, "wb") as file:
        _ = writer.write(file)


def main() -> None:
    # typer.run(test)
    typer.run(make_pdf_file)


if __name__ == "__main__":
    main()
