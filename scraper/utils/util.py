import os
import json
from pathlib import Path


def check_folder(base) -> str:
    base_path = base if base is str else str(base)
    if not os.path.isdir(base_path):
        print("{} not found! Creating folder...".format(base_path))
        try:
            if len(base_path.split("/")) == 1:
                os.mkdir(base_path)
            else:
                tmp_path, file_path = os.path.split(base_path)
                while not os.path.exists(tmp_path):
                    check_folder(tmp_path)
                os.mkdir(base_path)
        except FileExistsError:
            print("Race condition caught on creating folder {}".format(base_path))
            print("Returning existing folder...")
    return base_path


def agg_jsonls(folder_path):
    files = [file for file in Path(folder_path).rglob("*.jl")]
    ad_ls = []
    for file in files:
        for ad in file.open("r", encoding="utf-8"):
            ad_ls.append(json.loads(ad))
    return ad_ls
