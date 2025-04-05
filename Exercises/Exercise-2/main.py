import requests
import pandas as pd
import re

from bs4 import BeautifulSoup

URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"


def use_bs4() -> str | None:
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return

    soup_data = BeautifulSoup(response.text, "html.parser")
    table = soup_data.find("table")

    trs = table.find_all("tr")

    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 4:
            if tds[1].text.strip() == "2024-01-19 10:27":
                return tds[0].text.strip()

def use_regex() -> str | None:
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return

    links = re.search(
        "<tr><td><a href=\"[a-zA-Z0-9]*.csv\">[a-zA-Z0-9]*.csv</a></td><td align=\"right\">2024-01-19\s10:27\s*</td><td align=\"right\">\s*\d+.\d+[MK]</td><td>&nbsp;</td></tr>",
        response.text
    )

    if links.group(0):
        name = re.search("[a-zA-Z0-9]*.csv", links.group(0)).group(0)
        return name

def download(name: str):
    link = f"{URL}{name}"
    response = requests.get(link)

    with open(f"./{name}", "wb") as file:
        file.write(response.content)

def main():
    # Two methods to find the file name: using regex or BeautifulSoup
    name = use_bs4() # or use_regex()
    if name:
        download(name)
        df = pd.read_csv(f"./{name}")
        max_temp = df["HourlyDryBulbTemperature"].max()
        print(df[df["HourlyDryBulbTemperature"] == max_temp])
    else:
        print("File name could not be found.")

if __name__ == "__main__":
    main()
