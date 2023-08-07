import pandas as pd
import json
import csv
import argparse
import re

def template_script(jsondat, file="paco_normalise.txt"):
    with open(file) as fh:
        script = fh.read()
    script2 = re.sub("CONFIG_HERE", f"CONFIG={json.dumps(jsondat)}", script)
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
    ap.add_argument("-s", "--protocol-script",type=argparse.FileType("w"), required=True, 
            help="OT2 Protocol script output file")
    ap.add_argument("-q", "--quantfile", type=argparse.FileType("r"), required=True,
            help="Quantification file (csv)")
    args = ap.parse_args(argv)

    plate_pos = {}
    plate_i = 0
    quant = pd.read_csv(args.quantfile)
    data = {}
    print("plate", "well", "status", "stock_conc", "diluent_vol", "final_vol", "final_conc", sep="\t")
    for well in quant.itertuples():
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
        print(well.plate_name, well.well, status, well.conc, tfr_vol, final_vol, final_conc, sep="\t")
        pp = plate_pos[well.plate_name]
        data[pp][well.well] = tfr_vol

    script = template_script(data)
    args.protocol_script.write(script)
    args.protocol_script.close()

if __name__ == "__main__":
    main()
