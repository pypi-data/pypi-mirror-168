import glob
import re
import sys
from pathlib import Path

import intake
import pandas
import xarray as xr

BOLD = "\033[1m"
END = "\033[0m"


def query_parser(query):
    # parse json query to meaningful args for OPeNDAP
    query_dict = {}
    query_dict["opendap_product_id"] = query.get("datasetId").split(":")[-2]
    query_dict["opendap_dataset_id"] = query.get("datasetId").split(":")[-1]
    ds = connect_to_wekeo(query_dict)
    query_dict["query_vars"] = query.get("multiStringSelectValues")[0].get("value")
    try:
        query_dict["query_start_date"] = query.get("dateRangeSelectValues")[0].get(
            "start"
        )[:-1]
        query_dict["query_end_date"] = query.get("dateRangeSelectValues")[0].get("end")[
            :-1
        ]
    except TypeError as e:
        query_dict["query_start_date"] = str(
            ds.time[-1].dt.strftime("%d-%m-%Y %H:%M:%S").data
        )
        query_dict["query_end_date"] = query_dict["query_start_date"]
    query_dict["query_minimum_longitude"] = query.get("boundingBoxValues")[0].get(
        "bbox"
    )[0]
    query_dict["query_maximum_longitude"] = query.get("boundingBoxValues")[0].get(
        "bbox"
    )[2]
    query_dict["query_minimum_latitude"] = query.get("boundingBoxValues")[0].get(
        "bbox"
    )[1]
    query_dict["query_maximum_latitude"] = query.get("boundingBoxValues")[0].get(
        "bbox"
    )[3]
    try:
        query_dict["query_start_depth"] = query.get("depthRangeSelectValues")[0].get(
            "start"
        )
        query_dict["query_end_depth"] = query.get("depthRangeSelectValues")[0].get(
            "end"
        )
    except TypeError as e:
        if "depth" in ds.dims:
            query_dict["query_start_depth"] = float(ds.depth[0].data) - 0.01
            query_dict["query_end_depth"] = float(ds.depth[0].data) + 0.01
        else:
            query_dict["query_start_depth"] = None
    return query_dict


def connect_to_wekeo(query_dict, force=None):
    opendap_server_name = "wekeo-cmems-opendap-catalog"
    opendap_catalog_urls = [
        "https://cmems-opendap1.wekeo.eu/thredds/catalog.xml",
        "https://cmems-opendap2.wekeo.eu/thredds/catalog.xml",
    ]
    # set connection to catalog
    if not force:
        try:
            catalog = intake.open_thredds_cat(
                opendap_catalog_urls[0], name=opendap_server_name
            )
        except Exception as e:
            catalog = intake.open_thredds_cat(
                opendap_catalog_urls[1], name=opendap_server_name
            )
    else:
        catalog = intake.open_thredds_cat(
            opendap_catalog_urls[1], name=opendap_server_name
        )

    # open whole dataset -> should be instant but can take up to 3-5 minutes in (really) rare occasion
    datacube = xr.open_dataset(
        catalog[
            f"{query_dict['opendap_product_id']}/{query_dict['opendap_dataset_id']}"
        ].urlpath
    )
    return datacube


def load_datacube(query, opendap_server_name=None, download=None, **kwargs):

    # parse json query to meaningful args for OPeNDAP
    query = query_parser(query)

    # for proofchecking against copernicus marine servers
    if opendap_server_name == "cmems":
        opendap_catalog_urls = [
            "https://nrt.cmems-du.eu/thredds/dodsC/",
            "https://my.cmems-du.eu/thredds/dodsC/",
        ]
        versioned = re.findall(r"\d{6}", query["opendap_dataset_id"].split("_")[-1])
        if versioned:
            query["opendap_dataset_id"] = query["opendap_dataset_id"][:-7]
        try:
            datacube = xr.open_dataset(
                f"{opendap_catalog_urls[0]}/{query['opendap_dataset_id']}"
            )
        except Exception as e:
            datacube = xr.open_dataset(
                f"{opendap_catalog_urls[1]}/{query['opendap_dataset_id']}"
            )
    else:
        # init args to default values matching WEkEO configuration for the workaround
        datacube = connect_to_wekeo(query)

    # post-process coordinates to homogenize datacube results
    for coords in datacube.coords:
        if coords == "lon":
            datacube = datacube.rename({"lon": "longitude"})
        if coords == "lat":
            datacube = datacube.rename({"lat": "latitude"})
        if coords == "nv":
            datacube = datacube.drop_dims("nv")

    # remotely subset datacube to expected json query parameters
    datacube = datacube.drop_vars(
        [v for v in datacube.data_vars if v not in query["query_vars"]]
    ).sel(
        time=slice(query["query_start_date"], query["query_end_date"]),
        longitude=slice(
            query["query_minimum_longitude"], query["query_maximum_longitude"]
        ),
        latitude=slice(
            query["query_minimum_latitude"], query["query_maximum_latitude"]
        ),
    )
    # dedicated handling for depth dimension
    if ("depth" in datacube.dims) and (query["query_start_depth"] is not None):
        datacube = datacube.sel(
            depth=slice(query["query_start_depth"], query["query_end_depth"])
        )

    # to allow downloading directly
    if download:
        if "output_filename" in kwargs:
            output_filename = kwargs["output_filename"]
        else:
            output_filename = None
        if "overwrite" in kwargs:
            overwrite = kwargs["overwrite"]
            download_datacube(datacube, output_filename, overwrite=overwrite)
        else:
            download_datacube(datacube, output_filename)

    # return datacube
    return datacube


def compute_datacube_stats(datacube):
    return datacube.to_dataframe().describe().style.format("{:.5f}")


def download_datacube(datacube, output=None, check_sample=True, overwrite=None):
    if not output:
        # [TODO] To generate output filename based on dataset content if not provided
        output = "datacube.nc"
    else:
        output = Path(output)
        if not output.exists():
            if output.suffix == ".nc":
                output.parent.mkdir(parents=True, exist_ok=True)
            else:
                print(
                    f"[WARNING] Downloaded datacube should be saved in NetCDF format. Please provide {str(output)} with .nc extension."
                )
        else:
            if not overwrite:
                check_overwrite = question(
                    f"[ACTION] The file {output} already exists. Do you want "
                    f"{BOLD}to overwrite{END} it?",
                    "no",
                )
                if not check_overwrite:
                    msg = (
                        "[INFO] Skipping downloading. "
                        "Please provide a new output filename "
                        "or put overwrite=True before calling the function."
                    )
                    sys.exit(msg)

    if check_sample:
        import matplotlib.pyplot as plt

        try:
            datacube[list(datacube.data_vars)[0]].isel(time=0, depth=0).plot()
        except ValueError as e:
            datacube[list(datacube.data_vars)[0]].isel(time=0).plot()
        plt.title(f"Sample plot of data to be saved in {output}")
        plt.show()
        print(
            "[INFO] Please cancel the download function if this sample does not match with your data needs."
        )
    print("[INFO] Download starts...")
    try:
        datacube.to_netcdf(output)
        print("[INFO] Download ends successfully.")
        download_status = True
    except Exception as e:
        print(
            f"[ERROR] Download failed due to {e}. Please reduced (usually over daterange) {datacube}"
        )
        download_status = False
    return download_status


def question(question, default="yes"):
    """
    Returns answer from a yes/no question, read from user\'s input.

    Parameters
    ----------
    question : str
        String written as a question, displayed to user.
    default : str, optional
        String value to be presented to user to help . The default is "yes".

    Raises
    ------
    ValueError
        Raise error to continue asking question until user inputs one of the valid choice.

    Returns
    -------
    bool
        Returns ``True`` if user validates question, ``False`` otherwise.

    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"[ERROR] Invalid default answer: '{default}'")
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "[ACTION] Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n"
            )


def list_dir(path):
    listing_directory = []
    if path[-1] == '/':
        path = f'{path}*'
    else:
        path = path.replace(path.split('/')[-1], '*')
    for file in glob.glob(path, recursive=True):
        listing_directory.append(file)
    return listing_directory