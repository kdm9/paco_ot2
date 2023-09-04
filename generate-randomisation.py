#!/usr/bin/env python3
import pandas as pd
import json
import csv
import argparse
import re
from pathlib import Path
from itertools import islice
from collections import defaultdict
try:
    from tqdm.auto import tqdm
except ImportError:
    def tqdm(i, *args, **kwargs):
        return i

def R(decimal, place=2):
    return round(decimal, place)

def no0(well):
    return re.sub(r"([A-H])0(\d)", r"\1\2", well)

def template_script(jsondat, file="paco_transfer_template.py"):
    with open(file) as fh:
        script = fh.read()
    for key, val in jsondat.items():
        needle = f"__{key}__"
        if isinstance(val, dict):
            val = json.dumps(val)
        script = re.sub(needle, str(val), script)
    return script

def batched(iterable, n=1):
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--volume", default=20, type=float,
            help="default volume of source DNA to transfer (uL)")
    ap.add_argument("-s", "--protocol-script-dir", type=Path, required=True, 
            help="OT2 Protocol script output directory")
    ap.add_argument("-m", "--fromtomap", type=argparse.FileType("r"), required=True,
            help="Map with columns plate_name_old, well_old, plate_name_new, well_new. Optionally batch and volume (csv)")
    args = ap.parse_args(argv)

    fromto = pd.read_csv(args.fromtomap)
    if "batch" not in fromto:
        fromto["batch"] = "1"
    if "volume" not in fromto:
        fromto["volume"] = args.volume

    batches = {}
    for batch, df in fromto.groupby("batch"):
        bydstplate = defaultdict(list)
        for well in df.itertuples():
            bydstplate[well.plate_name_new].append({
                "src_plate": well.plate_name_old,
                "src_well": no0(well.well_old),
                "dst_plate": well.plate_name_new,
                "dst_well": no0(well.well_new),
                "volume": well.volume,
            })
        batches[batch] = {k:v for k, v in bydstplate.items()}

    for batch, bydst in batches.items():
        for dstplate, transfers in bydst.items():
            name = f"{batch}__{dstplate}"
            script = template_script({
                "TRANSFERS": transfers,
                "DEST_PLATE_NAME": dstplate,
                "PROTOCOL_NAME": name,
            })
            with open(args.protocol_script_dir / f"{name}.ot2.py", 'w') as fh:
                fh.write(script)

if __name__ == "__main__":
    main()
