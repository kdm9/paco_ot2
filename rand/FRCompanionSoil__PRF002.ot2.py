from opentrons import protocol_api

config = {
    "TRANSFERS": [{'src_plate': 'PCE026', 'src_well': 'B7', 'dst_plate': 'PRF002', 'dst_well': 'B1', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'H6', 'dst_plate': 'PRF002', 'dst_well': 'C1', 'volume': 20}, {'src_plate': 'PCE048', 'src_well': 'D4', 'dst_plate': 'PRF002', 'dst_well': 'D1', 'volume': 20}, {'src_plate': 'PCE048', 'src_well': 'B8', 'dst_plate': 'PRF002', 'dst_well': 'E1', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'G6', 'dst_plate': 'PRF002', 'dst_well': 'F1', 'volume': 20}, {'src_plate': 'PCE048', 'src_well': 'B5', 'dst_plate': 'PRF002', 'dst_well': 'H1', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'H11', 'dst_plate': 'PRF002', 'dst_well': 'A2', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'B8', 'dst_plate': 'PRF002', 'dst_well': 'B2', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'H7', 'dst_plate': 'PRF002', 'dst_well': 'C2', 'volume': 20}, {'src_plate': 'PCE034', 'src_well': 'A1', 'dst_plate': 'PRF002', 'dst_well': 'D2', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'C4', 'dst_plate': 'PRF002', 'dst_well': 'E2', 'volume': 20}, {'src_plate': 'PCE033', 'src_well': 'G5', 'dst_plate': 'PRF002', 'dst_well': 'G2', 'volume': 20}, {'src_plate': 'PCE048', 'src_well': 'B9', 'dst_plate': 'PRF002', 'dst_well': 'H2', 'volume': 20}, {'src_plate': 'PCE033', 'src_well': 'E1', 'dst_plate': 'PRF002', 'dst_well': 'A3', 'volume': 20}, {'src_plate': 'PCE033', 'src_well': 'B2', 'dst_plate': 'PRF002', 'dst_well': 'B3', 'volume': 20}, {'src_plate': 'PCE034', 'src_well': 'A2', 'dst_plate': 'PRF002', 'dst_well': 'D3', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'F8', 'dst_plate': 'PRF002', 'dst_well': 'E3', 'volume': 20}, {'src_plate': 'PCE026', 'src_well': 'H2', 'dst_plate': 'PRF002', 'dst_well': 'F3', 'volume': 20}, {'src_plate': 'PCE034', 'src_well': 'H4', 'dst_plate': 'PRF002', 'dst_well': 'G3', 'volume': 20}, {'src_plate': 'PCE033', 'src_well': 'H3', 'dst_plate': 'PRF002', 'dst_well': 'H3', 'volume': 20}],
    "DEST_PLATE_NAME": "PRF002",
}

metadata = {
    'protocolName': "FRCompanionSoil__PRF002",
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
        pipette.aspirate(vol, src_plate[src_well], rate=0.4)
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
