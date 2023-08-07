import pandas as pd
import json
import csv
import argparse
import re
from pathlib import Path
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
    script2 = re.sub("CONFIG_HERE", f"config={json.dumps(jsondat)}", script)
    return script2

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conc", default=5, type=float,
            help="Target concentration in ng/uL")
    ap.add_argument("-v", "--volume", default=20, type=float,
            help="Constant volume of source DNA to transfer (uL)")
    ap.add_argument("-m", "--min-transfer-volume", default=5, type=float,
            help="Smallest volume of diluent that we can transfer (uL)")
    ap.add_argument("-x", "--max-transfer-volume", default=180, type=float,
            help="Largest volume of diluent that we can transfer (uL)")
    ap.add_argument("-n", "--name", type=str,
            help="Name the run (makes it easier to find in the OT2 interface")
    ap.add_argument("-s", "--protocol-script", type=Path, required=True, 
            help="OT2 Protocol script output file")
    ap.add_argument("-q", "--quantfile", type=argparse.FileType("r"), required=True,
            help="Quantification file (csv)")
    ap.add_argument("-t", "--summary-table", type=argparse.FileType("w"), required=True,
            help="Summary of actions table (tsv)")
    args = ap.parse_args(argv)

    if args.name is None:
        args.name = args.protocol_script.stem

    plate_pos = {}
    plate_i = 0
    quant = pd.read_csv(args.quantfile)
    data = {}
    print("plate", "well", "opentron_position", "status", "stock_conc", "diluent_vol", "final_vol", "final_conc", sep="\t", file=args.summary_table)
    for well in tqdm(quant.itertuples()):
        if well.plate_name not in plate_pos:
            plate_i += 1
            plate_pos[well.plate_name] = plate_i
            data[plate_i] = {}
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
        pp = plate_pos[well.plate_name]
        print(well.plate_name, well.well, pp, status, R(well.conc), R(tfr_vol, 1), R(final_vol), R(final_conc), sep="\t", file=args.summary_table)
        well_no0 = re.sub(r"([A-H])0(\d)", r"\1\2", well.well)
        data[pp][well_no0] = R(tfr_vol, 1)
    script = template_script({
        "PLATES": data,
        "WELL_MAX_VOLUME": args.max_transfer_volume,
        "PROTOCOL_NAME": args.name,
    })
    with args.protocol_script.open('w') as fh:
        fh.write(script)

if __name__ == "__main__":
    main()
