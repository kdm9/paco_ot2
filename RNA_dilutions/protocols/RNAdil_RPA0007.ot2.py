from opentrons import protocol_api

config = {
    "PLATE_NAME": "RPA0007",
    "VOLUMES": {"A1": {"rna": 5.0, "h2o": 45.0}, "B1": {"rna": 5.0, "h2o": 45.0}, "C1": {"rna": 8.0, "h2o": 42.0}, "D1": {"rna": 5.0, "h2o": 45.0}, "E1": {"rna": 6.0, "h2o": 44.0}, "F1": {"rna": 2.0, "h2o": 48.0}, "G1": {"rna": 5.0, "h2o": 45.0}, "H1": {"rna": 2.0, "h2o": 48.0}, "A2": {"rna": 25.0, "h2o": 25.0}, "B2": {"rna": 10.0, "h2o": 40.0}, "C2": {"rna": 7.0, "h2o": 43.0}, "D2": {"rna": 17.0, "h2o": 33.0}, "E2": {"rna": 2.0, "h2o": 48.0}, "F2": {"rna": 6.0, "h2o": 44.0}, "G2": {"rna": 8.0, "h2o": 42.0}, "H2": {"rna": 10.0, "h2o": 40.0}, "A3": {"rna": 20.0, "h2o": 30.0}, "B3": {"rna": 15.0, "h2o": 35.0}, "C3": {"rna": 4.0, "h2o": 46.0}, "D3": {"rna": 10.0, "h2o": 40.0}, "E3": {"rna": 7.0, "h2o": 43.0}, "F3": {"rna": 25.0, "h2o": 25.0}, "G3": {"rna": 25.0, "h2o": 25.0}, "H3": {"rna": 18.0, "h2o": 32.0}, "A4": {"rna": 9.0, "h2o": 41.0}, "B4": {"rna": 10.0, "h2o": 40.0}, "C4": {"rna": 3.0, "h2o": 47.0}, "D4": {"rna": 10.0, "h2o": 40.0}, "E4": {"rna": 4.0, "h2o": 46.0}, "F4": {"rna": 25.0, "h2o": 25.0}, "G4": {"rna": 25.0, "h2o": 25.0}, "H4": {"rna": 15.0, "h2o": 35.0}, "A5": {"rna": 3.0, "h2o": 47.0}, "B5": {"rna": 5.0, "h2o": 45.0}, "C5": {"rna": 25.0, "h2o": 25.0}, "D5": {"rna": 7.0, "h2o": 43.0}, "E5": {"rna": 5.0, "h2o": 45.0}, "F5": {"rna": 8.0, "h2o": 42.0}, "G5": {"rna": 20.0, "h2o": 30.0}, "H5": {"rna": 4.0, "h2o": 46.0}, "A6": {"rna": 6.0, "h2o": 44.0}, "B6": {"rna": 6.0, "h2o": 44.0}, "C6": {"rna": 7.0, "h2o": 43.0}, "D6": {"rna": 20.0, "h2o": 30.0}, "E6": {"rna": 7.0, "h2o": 43.0}, "F6": {"rna": 15.0, "h2o": 35.0}, "G6": {"rna": 17.0, "h2o": 33.0}, "H6": {"rna": 8.0, "h2o": 42.0}, "A7": {"rna": 4.0, "h2o": 46.0}, "B7": {"rna": 4.0, "h2o": 46.0}, "C7": {"rna": 25.0, "h2o": 25.0}, "D7": {"rna": 7.0, "h2o": 43.0}, "E7": {"rna": 25.0, "h2o": 25.0}, "F7": {"rna": 3.0, "h2o": 47.0}, "G7": {"rna": 7.0, "h2o": 43.0}, "H7": {"rna": 25.0, "h2o": 25.0}, "A8": {"rna": 7.0, "h2o": 43.0}, "B8": {"rna": 5.0, "h2o": 45.0}, "C8": {"rna": 17.0, "h2o": 33.0}, "D8": {"rna": 25.0, "h2o": 25.0}, "E8": {"rna": 21.0, "h2o": 29.0}, "F8": {"rna": 10.0, "h2o": 40.0}, "G8": {"rna": 6.0, "h2o": 44.0}, "H8": {"rna": 4.0, "h2o": 46.0}, "A9": {"rna": 25.0, "h2o": 25.0}, "B9": {"rna": 3.0, "h2o": 47.0}, "C9": {"rna": 18.0, "h2o": 32.0}, "D9": {"rna": 3.0, "h2o": 47.0}, "E9": {"rna": 10.0, "h2o": 40.0}, "F9": {"rna": 25.0, "h2o": 25.0}, "G9": {"rna": 25.0, "h2o": 25.0}, "H9": {"rna": 25.0, "h2o": 25.0}, "A10": {"rna": 7.0, "h2o": 43.0}, "B10": {"rna": 3.0, "h2o": 47.0}, "C10": {"rna": 3.0, "h2o": 47.0}, "D10": {"rna": 3.0, "h2o": 47.0}, "E10": {"rna": 10.0, "h2o": 40.0}, "F10": {"rna": 23.0, "h2o": 27.0}, "G10": {"rna": 10.0, "h2o": 40.0}, "H10": {"rna": 4.0, "h2o": 46.0}, "A11": {"rna": 3.0, "h2o": 47.0}, "B11": {"rna": 10.0, "h2o": 40.0}, "C11": {"rna": 4.0, "h2o": 46.0}, "D11": {"rna": 25.0, "h2o": 25.0}, "E11": {"rna": 5.0, "h2o": 45.0}, "F11": {"rna": 4.0, "h2o": 46.0}, "G11": {"rna": 15.0, "h2o": 35.0}, "H11": {"rna": 15.0, "h2o": 35.0}, "A12": {"rna": 20.0, "h2o": 30.0}, "B12": {"rna": 6.0, "h2o": 44.0}, "C12": {"rna": 15.0, "h2o": 35.0}, "D12": {"rna": 10.0, "h2o": 40.0}, "E12": {"rna": 20.0, "h2o": 30.0}, "F12": {"rna": 19.0, "h2o": 31.0}, "G12": {"rna": 15.0, "h2o": 35.0}, "H12": {"rna": 3.0, "h2o": 47.0}},
}

metadata = {
        'protocolName': "RNAdil_RPA0007",
        'author': 'Kevin Murray',
        'apiLevel': '2.9',
}

def dispense_with(pipette, src, dst, volume):
    transferred = 0
    while transferred < volume:
        todo = volume-transferred
        if todo > pipette.max_volume and todo <= pipette.max_volume*2:
            vol = todo/2
        else:
            vol = min(todo, pipette.max_volume)
        pipette.aspirate(vol, src, , rate=1)
        pipette.dispense(vol, plate[well], rate=1)
        transferred += vol

def run(protocol: protocol_api.ProtocolContext):
    water = protocol.load_labware('integra_1_reservoir_150ml', 11)

    tiprack_p200_10 = protocol.load_labware('standard_96_tiprack_200ul', 10)
    tiprack_p200_9 = protocol.load_labware('standard_96_tiprack_200ul', 9)
    p50 = protocol.load_instrument('p50_single', 'left', tip_racks=[tiprack_p200_10, tiprack_p200_9])
    p50.well_bottom_clearance.aspirate = 0
    p50.well_bottom_clearance.dispense = 0

    tiprack_p10 = protocol.load_labware('standard_96_tiprack_10ul', 8)
    p10 = protocol.load_instrument('p10_single', 'right', tip_racks=[tiprack_p10])
    p10.well_bottom_clearance.aspirate = 0.5
    p10.well_bottom_clearance.dispense = 0.5

    plate_name = config["PLATE_NAME"]
    src_plate = protocol.load_labware('axygen_96_wellplate_200ul', 1, label=plate_name)
    dest_plate = protocol.load_labware('axygen_96_wellplate_200ul', 2, label=plate_name + "_dilution")

    p50.pick_up_tip()
    for well, vols in config["VOLUMES"].items():
        water_ul = vols["h2o"]
        dispense_with(p50, water["A1"], dest_plate[well], water_ul)
        p50.blow_out(dest_plate[well])
        p50.touch_tip(dest_plate[well])
    p50.drop_tip()

    for well, vols in config["VOLUMES"].items():
        rna_ul = vols["rna"]
        if rna_ul < 15:
            pipette = p10
        else:
            pipette = p50
        pipette.pick_up_tip()
        dispense_with(pipette, src_plate[well], dest_plate[well], rna_ul)
        pipette.mix(repetitions=3, volume=min(pipette.max_volume, 25), location=dest_plate[well])
        pipette.blow_out(dest_plate[well])
        pipette.touch_tip(dest_plate[well])
        pipette.drop_tip()
