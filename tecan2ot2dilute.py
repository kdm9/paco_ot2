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

def template_script(jsondat, file="paco_normalise.txt"):
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
    ap.add_argument("-b", "--batchsize", default=9, type=int,
            help="Number of plates per batch")
    ap.add_argument("-c", "--conc", default=5, type=float,
            help="Target concentration in ng/uL")
    ap.add_argument("-v", "--volume", default=20, type=float,
            help="Constant volume of source DNA to transfer (uL)")
    ap.add_argument("-m", "--min-transfer-volume", default=5, type=float,
            help="Smallest volume of diluent that we can transfer (uL)")
    ap.add_argument("-x", "--max-transfer-volume", default=180, type=float,
            help="Largest volume of diluent that we can transfer (uL)")
    ap.add_argument("-s", "--protocol-script-dir", type=Path, required=True, 
            help="OT2 Protocol script output directory")
    ap.add_argument("-q", "--quantfile", type=argparse.FileType("r"), required=True,
            help="Quantification file (csv)")
    ap.add_argument("-t", "--summary-table", type=argparse.FileType("w"), required=True,
            help="Summary of actions table (tsv)")
    args = ap.parse_args(argv)

    plate_pos = {}
    quant = pd.read_csv(args.quantfile)
    data = {}
    print("plate", "well", "status", "stock_conc", "diluent_vol", "final_vol", "final_conc", sep="\t", file=args.summary_table)
    for well in tqdm(quant.itertuples()):
        if well.plate_name not in data:
            data[well.plate_name] = {}
        final_vol = well.conc/args.conc * args.volume
        tfr_vol = final_vol - args.volume
        if well.conc < args.conc:
            tfr_vol = 0
            status = "conc below target"
        elif tfr_vol < args.min_transfer_volume:
            tfr_vol = 0
            status = "transfer too small"
        elif tfr_vol > args.max_transfer_volume:
            tfr_vol = args.max_transfer_volume
            status = "transfer too large"
        else:
            status = "OK"
        final_vol =args.volume + tfr_vol
        final_conc = well.conc * (args.volume/final_vol)
        well_no0 = re.sub(r"([A-H])0(\d)", r"\1\2", well.well)
        print(well.plate_name, well_no0, status, R(well.conc), R(tfr_vol, 1), R(final_vol), R(final_conc), sep="\t", file=args.summary_table)
        data[well.plate_name][well_no0] = R(tfr_vol, 1)

    for plates in batched(data, n=args.batchsize):
        name = "__".join(plates)
        dat = {p: data[p] for p in plates}
        script = template_script({
            "PLATES": dat,
            "WELL_MAX_VOLUME": args.max_transfer_volume,
            "PROTOCOL_NAME": name,
        })
        with open(args.protocol_script_dir / f"{name}.ot2.py", 'w') as fh:
            fh.write(script)

if __name__ == "__main__":
    main()
