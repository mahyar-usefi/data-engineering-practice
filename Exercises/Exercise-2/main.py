import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"


def make_request() -> requests.Response:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        response = requests.request("GET", URL, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(e)


def use_bs4() -> str | None:
    if response := make_request():
        soup_data = BeautifulSoup(response.text, "html.parser")
        table = soup_data.find("table")

        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 4:
                if tds[1].text.strip() == "2024-01-19 10:27":
                    return tds[0].text.strip()
        return None
    else:
        return None


def use_regex() -> str | None:
    if response := make_request():
        links = re.search(
            "<tr><td><a href=\"[a-zA-Z0-9]*.csv\">[a-zA-Z0-9]*.csv</a></td><td align=\"right\">2024-01-19\s10:27\s*</td><td align=\"right\">\s*\d+.\d+[MK]</td><td>&nbsp;</td></tr>",
            response.text
        )

        if links.group(0):
            name = re.search("[a-zA-Z0-9]*.csv", links.group(0)).group(0)
            return name
        else:
            return None
    else:
        return None


def download(name: str):
    download_link = urljoin(URL, name)
    response = requests.get(download_link)

    with open(name, "wb") as file:
        file.write(response.content)


def main():
    # Two methods to find the file name: using regex or BeautifulSoup
    name = use_bs4()  # or use_regex()
    if name:
        download(name)
        df = pd.read_csv(name)
        max_temp = df["HourlyDryBulbTemperature"].max()
        print(df[df["HourlyDryBulbTemperature"] == max_temp])
    else:
        print("File name could not be found.")


if __name__ == "__main__":
    main()
