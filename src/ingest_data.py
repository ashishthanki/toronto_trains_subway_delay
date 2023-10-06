"File used to ingest raw Toronto train data from URL."
import logging
import re
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()

output_path = Path().absolute() / "data/raw/"


def get_data(
    output_folder: Path,
    base_url: str = "https://ckan0.cf.opendata.inter.prod-toronto.ca",
    year_limit: int = 2020,
) -> None:
    """_summary_

    Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
    https://docs.ckan.org/en/latest/api/

    Args:
        output_folder (Path): Where to save the data.
        base_url (_type_, optional): To hit our API, you'll be making requests to:
            Defaults to "https://ckan0.cf.opendata.inter.prod-toronto.ca".
    """
    # Datasets are called "packages". Each package can contain many "resources"
    # To retrieve the metadata for this package and its resources,
    # use the package name in this page's URL:
    url = base_url + "/api/3/action/package_show"
    params = {"id": "ttc-subway-delay-data"}
    package = requests.get(url, params=params).json()

    # To get resource data:
    for _, resource in enumerate(package["result"]["resources"]):
        # To get metadata for non datastore_active resources:
        if resource["datastore_active"]:
            continue
        file_name = resource["name"]
        data_url = resource["url"]

        # only store results from 2019 onwards
        match = re.match(".*([1-3][0-9]{3})", file_name)
        if match is not None:
            year = int(match.group(1))
            if year < year_limit:
                continue

        # Get raw data
        data = requests.get(data_url)

        if data.status_code != 200:
            logger.info(f"{file_name} failed to download.")
            continue

        # Download files
        with open(f"{output_folder/file_name}.xlsx", "wb") as output:
            output.write(data.content)


if __name__ == "__main__":
    get_data(output_path)
