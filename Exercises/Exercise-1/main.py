import os
import shutil
import asyncio
import aiohttp
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


async def download_uri(session: aiohttp.ClientSession, uri: str):
    filename = uri.split("/")[-1]

    download_dir = os.path.join(cur_path, "downloads")
    zip_file = os.path.join(download_dir, filename)

    try:
        async with session.get(uri) as response:
            response.raise_for_status()

            with open(zip_file, "wb") as file:
                async for chunk in response.content.iter_chunked(512 * 1024):
                    file.write(chunk)

        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(download_dir)

        if os.path.isfile(zip_file):
            os.remove(zip_file)

    except aiohttp.ClientResponseError as err:
        print(f"err\n"
              f"{uri} is not a valid URI.")
    except zipfile.BadZipFile:
        print(f"File {zip_file} is not a valid zip file.")
    except Exception as e:
        print(e)


async def main():
    create_download_dir()

    async with aiohttp.ClientSession() as session:
        tasks = [download_uri(session, uri) for uri in download_uris]
        await asyncio.gather(*tasks)

    # The folder __MACOSX are created by macOS, try to remove it
    exercise_dir = cur_path
    macosx = os.path.join(exercise_dir, "__MACOSX")
    if os.path.isdir(macosx):
        shutil.rmtree(macosx)

    download_dir = os.path.join(cur_path, f"downloads")
    macosx = os.path.join(download_dir, "__MACOSX")
    if os.path.isdir(macosx):
        shutil.rmtree(macosx)


if __name__ == "__main__":
    asyncio.run(main())
