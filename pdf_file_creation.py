from typing import Annotated
from rich.progress import track
import pypdf
import typer
import datetime
from pypdf.generic import IndirectObject
import bookmarks_addition
from collections import defaultdict
import logging


def make_pdf_file(
    input_file: Annotated[str, typer.Argument(help="Name of the input file")],
    output_file: Annotated[str, typer.Argument(help="Name of the output file")],
    bookmark_file_name: Annotated[
        str,
        typer.Argument(
            help="Name of the bookmarks file. Check the README on how to format"
        ),
    ],
    copy_metadata: Annotated[
        bool, typer.Argument(help="Whether to copy the metadata of the input file")
    ] = True,
) -> None:
    """
    Adds custom bookmarks to the input file,
    to produce an output file with the bookmarks
    """

    reader: pypdf.PdfReader = pypdf.PdfReader(input_file)
    writer: pypdf.PdfWriter = pypdf.PdfWriter(input_file)

    logging.info("Copying files")
    for page in track(reader.pages, description="Copying PDF pages"):
        _ = writer.add_page(page)

    logging.info("Writing metadata")
    if (data := reader.metadata) is not None and copy_metadata:
        writer.add_metadata(data)
    else:
        if data is None:
            print("Original file had no metadata!")

        writer.add_metadata(  # Check how well this works
            {
                "/Author": "Abdullah Mirza",
                "/Producer": "APMT manipulation software",
                # "/Title": "Title",
                # "/Subject": "Subject",
                # "/Keywords": "Keywords",
                "/CreationDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                # "/ModDate": time,
                # "/Creator": "Creator",
                # "/CustomField": "CustomField",
            }
        )

    logging.info("Adding bookmarks to output file")
    bookmarks = bookmarks_addition.load_bookmarks_from_file(bookmark_file_name)

    bookmark_parents: defaultdict[int, IndirectObject] = defaultdict()

    for current_bookmark in track(bookmarks, description="Adding bookmarks"):
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

    logging.info("Writing the output file")
    with open(output_file, "wb") as file:
        _ = writer.write(file)
