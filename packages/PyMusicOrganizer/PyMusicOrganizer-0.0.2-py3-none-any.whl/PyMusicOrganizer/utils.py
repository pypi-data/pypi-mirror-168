from os import walk

from os import walk
from mutagen.flac import FLAC
from pathlib import Path
from rich.progress import track

def folder_count(path: str) -> int:
    count1 = 0
    for root, dirs, files in walk(path):
        count1 += len(dirs)

    return count1


def rename_album_and_artist_by_folder_name(main_path: str):
    """
    Rename the album and artist tags by the folder name. Inside the main path there should
    be folder with the artist name and inside that folder there should be folders with the
    album name. The album folder should contain the FLAC files.

    Args:
    -   main_path: the path to the folder containing the music
    """

    main_dir = Path(main_path)

    for root, dirs, files in track(walk(main_path), total=(folder_count(main_path) + 1)):
        for file in files:
            if file.startswith("."):
                continue

            if file.endswith(".flac"):
                path = Path(root, file)
                audio = FLAC(path)

                index = path.parents.index(main_dir)

                # Album Name
                album_name = path.parents[index - 2].name.strip()

                audio["album"] = album_name

                if audio.get("artist"):
                    audio["albumartist"] = audio["artist"]

                # Artist Name
                artist_name = path.parents[index - 1].name.strip()

                if artist_name == "Various Artists":
                    # artist_name = audio["album"]
                    continue

                audio["artist"] = artist_name

                # print(main_dir, album_name, artist_name)
                audio.save()
