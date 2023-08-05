from typer import Typer

# Local
from PyMusicOrganizer.utils import rename_album_and_artist_by_folder_name

TIDAL_DIR = ""

app = Typer()


@app.command()
def main(main_path: str):
    rename_album_and_artist_by_folder_name(main_path)


if __name__ == "__main__":
    app()
