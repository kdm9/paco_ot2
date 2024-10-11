from opentrons import protocol_api

config = {
    "PLATE_NAME": "RPA014",
    "VOLUMES": {"A1": {"rna": 5.9, "h2o": 44.1}, "B1": {"rna": 5.1, "h2o": 44.9}, "C1": {"rna": 21.6, "h2o": 28.4}, "D1": {"rna": 25.0, "h2o": 25.0}, "E1": {"rna": 1.9, "h2o": 48.1}, "F1": {"rna": 25.0, "h2o": 25.0}, "G1": {"rna": 9.4, "h2o": 40.6}, "H1": {"rna": 16.5, "h2o": 33.5}, "A2": {"rna": 16.1, "h2o": 33.9}, "B2": {"rna": 16.9, "h2o": 33.1}, "C2": {"rna": 25.0, "h2o": 25.0}, "D2": {"rna": 9.9, "h2o": 40.1}, "E2": {"rna": 15.8, "h2o": 34.2}, "F2": {"rna": 12.4, "h2o": 37.6}, "G2": {"rna": 11.3, "h2o": 38.7}, "H2": {"rna": 12.5, "h2o": 37.5}, "A3": {"rna": 9.9, "h2o": 40.1}, "B3": {"rna": 25.0, "h2o": 25.0}, "C3": {"rna": 8.9, "h2o": 41.1}, "D3": {"rna": 3.4, "h2o": 46.6}, "E3": {"rna": 25.0, "h2o": 25.0}, "F3": {"rna": 2.6, "h2o": 47.4}, "G3": {"rna": 13.3, "h2o": 36.7}, "H3": {"rna": 4.2, "h2o": 45.8}, "A4": {"rna": 15.1, "h2o": 34.9}, "B4": {"rna": 3.9, "h2o": 46.1}, "C4": {"rna": 25.0, "h2o": 25.0}, "D4": {"rna": 25.0, "h2o": 25.0}, "E4": {"rna": 25.0, "h2o": 25.0}, "F4": {"rna": 25.0, "h2o": 25.0}, "G4": {"rna": 10.1, "h2o": 39.9}, "H4": {"rna": 5.5, "h2o": 44.5}, "A5": {"rna": 25.0, "h2o": 25.0}, "B5": {"rna": 14.7, "h2o": 35.3}, "C5": {"rna": 25.0, "h2o": 25.0}, "D5": {"rna": 20.7, "h2o": 29.3}, "E5": {"rna": 19.6, "h2o": 30.4}, "F5": {"rna": 3.4, "h2o": 46.6}, "G5": {"rna": 25.0, "h2o": 25.0}, "H5": {"rna": 24.9, "h2o": 25.1}, "A6": {"rna": 12.7, "h2o": 37.3}, "B6": {"rna": 13.3, "h2o": 36.7}, "C6": {"rna": 18.0, "h2o": 32.0}, "D6": {"rna": 14.0, "h2o": 36.0}, "E6": {"rna": 3.9, "h2o": 46.1}, "F6": {"rna": 25.0, "h2o": 25.0}, "G6": {"rna": 17.7, "h2o": 32.3}, "H6": {"rna": 9.3, "h2o": 40.7}, "A7": {"rna": 1.8, "h2o": 48.2}, "B7": {"rna": 21.3, "h2o": 28.7}, "C7": {"rna": 25.0, "h2o": 25.0}, "D7": {"rna": 14.3, "h2o": 35.7}, "E7": {"rna": 24.9, "h2o": 25.1}, "F7": {"rna": 50.0, "h2o": 0.0}, "G7": {"rna": 54.1, "h2o": -4.1}, "H7": {"rna": 8.9, "h2o": 41.1}, "A8": {"rna": 25.0, "h2o": 25.0}, "B8": {"rna": 3.4, "h2o": 46.6}, "C8": {"rna": 7.5, "h2o": 42.5}, "D8": {"rna": 18.1, "h2o": 31.9}, "E8": {"rna": 12.8, "h2o": 37.2}, "F8": {"rna": 21.6, "h2o": 28.4}, "G8": {"rna": 0.8, "h2o": 49.2}, "H8": {"rna": 3.3, "h2o": 46.7}, "A9": {"rna": 6.1, "h2o": 43.9}, "B9": {"rna": 13.6, "h2o": 36.4}, "C9": {"rna": 14.6, "h2o": 35.4}, "D9": {"rna": 71.9, "h2o": -21.9}, "E9": {"rna": 11.1, "h2o": 38.9}, "F9": {"rna": 10.3, "h2o": 39.7}, "G9": {"rna": 18.3, "h2o": 31.7}, "H9": {"rna": 7.0, "h2o": 43.0}, "A10": {"rna": 21.7, "h2o": 28.3}, "B10": {"rna": 25.0, "h2o": 25.0}, "C10": {"rna": 7.1, "h2o": 42.9}, "D10": {"rna": 7.7, "h2o": 42.3}, "E10": {"rna": 5.1, "h2o": 44.9}, "F10": {"rna": 6.5, "h2o": 43.5}, "G10": {"rna": 25.0, "h2o": 25.0}, "H10": {"rna": 3.8, "h2o": 46.2}, "A11": {"rna": 12.4, "h2o": 37.6}, "B11": {"rna": 20.2, "h2o": 29.8}, "C11": {"rna": 25.0, "h2o": 25.0}},
}

metadata = {
        'protocolName': "RNAdil_RPA014",
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
        pipette.aspirate(vol, src, rate=1)
        pipette.dispense(vol, dst, rate=1)
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
