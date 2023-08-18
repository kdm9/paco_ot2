from opentrons import protocol_api

config = {
    "TRANSFERS": __TRANSFERS__,
    "DEST_PLATE_NAME": "__DEST_PLATE_NAME__",
}

metadata = {
    'protocolName': "__PROTOCOL_NAME__",
    'author': 'Kevin Murray',
    'apiLevel': '2.9',
}


def do_transfer(transfer, dst_plate, source_plates, pipette):
    pipette.pick_up_tip()
    volume = transfer["volume"]
    src_plate = source_plates[transfer["src_plate"]]
    src_well = transfer["src_well"]
    dst_well = transfer["dst_well"]
    if volume < pipette.min_volume:
        volume = pipette.min_volume
    if volume > 200:
        raise ValueError(f"ERROR! overfull well {dst_well} on dest plate")
    transferred = 0
    while transferred < volume:
        todo = volume-transferred
        if todo > pipette.max_volume and todo <= pipette.max_volume*2:
            vol = todo/2
        else:
            vol = min(todo, pipette.max_volume)
        pipette.aspirate(vol, src_plate[src_well], rate=1)
        pipette.dispense(vol, dst_plate[dst_well], rate=1)
        pipette.blow_out(dst_plate[dst_well])
        pipette.touch_tip(dst_plate[dst_well])
        transferred += vol
    pipette.drop_tip()


def run(protocol: protocol_api.ProtocolContext):
    tiprack_p10 = protocol.load_labware('standard_96_tiprack_10ul', 1)
    p10 = protocol.load_instrument('p10_single', 'right', tip_racks=[tiprack_p10])
    p10.well_bottom_clearance.aspirate = 0.5
    p10.well_bottom_clearance.dispense = 0.5

    dest_plate = protocol.load_labware('axygen_96_wellplate_200ul', 2, label=config["DEST_PLATE_NAME"])

    pos = 3
    source_plates = {}
    all_sources = list(sorted(set(t["src_plate"] for t in config["TRANSFERS"])))
    for src in all_sources:
        if src in source_plates:
            continue
        source_plates[src] = protocol.load_labware('axygen_96_wellplate_200ul', pos, label=src)
        print("PMAP:", src, pos, sep='\t')
        pos += 1

    for transfer in config["TRANSFERS"]:
        do_transfer(transfer, dest_plate, source_plates, p10)
