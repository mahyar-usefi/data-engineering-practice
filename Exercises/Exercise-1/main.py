import requests

import os
import shutil

import zipfile


download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

cur_path = os.path.dirname(__file__)


def create_download_dir():
    os.makedirs("downloads", exist_ok=True)

def download_uri(uri: str):
    filename = uri.split("/")[-1]

    zip_file = os.path.join(cur_path, f"downloads/{filename}")
    download = os.path.join(cur_path, f"downloads")

    response = requests.get(uri)

    with open(zip_file, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(download)

    if os.path.isfile(zip_file):
        os.remove(zip_file)

    # The folder __MACOSX are created by macOS, try to remove it
    macosx = os.path.join(download, "__MACOSX")
    if os.path.isdir(macosx):
        shutil.rmtree(macosx)

def main():
    create_download_dir()
    for uri in download_uris:
        download_uri(uri)


if __name__ == "__main__":
    main()
