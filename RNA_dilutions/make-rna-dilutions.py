#!/usr/bin/env python3
import pandas as pd
import json
import csv
import argparse
import re
from pathlib import Path
from itertools import islice
try:
    from tqdm.auto import tqdm
except ImportError:
    def tqdm(i, *args, **kwargs):
        return i

def R(decimal, place=2):
    return round(decimal, place)

def template_script(jsondat, file="dilution_template.py"):
    with open(file) as fh:
        script = fh.read()
    for key, val in jsondat.items():
        needle = f"__{key}__"
        if isinstance(val, dict):
            val = json.dumps(val)
        script = re.sub(needle, str(val), script)
    return script


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--protocol-script-dir", type=Path, required=True, 
            help="OT2 Protocol script output directory")
    ap.add_argument("-q", "--quantfile", type=argparse.FileType("r"), required=True,
            help="Quantification file (csv)")
    args = ap.parse_args(argv)

    plate_pos = {}
    quant = pd.read_csv(args.quantfile)
    data = {}
    for well in tqdm(quant.itertuples()):
        if well.plate not in data:
            data[well.plate] = {}
        rna = well.rna_vol
        h2o = well.h2o_vol
        print(well.plate, well.well, rna, h2o)
        well_no0 = re.sub(r"([A-H])0(\d)", r"\1\2", well.well)
        data[well.plate][well_no0] = {"rna": R(rna, 1), "h2o": R(h2o, 1)}

    if not args.protocol_script_dir.is_dir():
        args.protocol_script_dir.mkdir()
    for plate in data:
        name = f"RNAdil_{plate}"
        script = template_script({
            "VOLUMES": data[plate],
            "PROTOCOL_NAME": name,
        })
        with open(args.protocol_script_dir / f"{name}.ot2.py", 'w') as fh:
            fh.write(script)

if __name__ == "__main__":
    main()
