import typer
import time
import pdf_file_creation


def main() -> None:
    typer.run(pdf_file_creation.make_pdf_file)


if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        main()
    except Exception as e:
        raise e
    finally:
        print(
            f"Program completed in {round(time.perf_counter() - start_time, 4)} seconds"
        )
