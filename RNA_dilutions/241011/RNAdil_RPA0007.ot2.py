from opentrons import protocol_api

config = {
    "PLATE_NAME": "RPA0007",
    "VOLUMES": {"A1": {"rna": 5.9, "h2o": 44.1}, "B1": {"rna": 13.0, "h2o": 37.0}, "C1": {"rna": 12.2, "h2o": 37.8}, "D1": {"rna": 13.7, "h2o": 36.3}, "E1": {"rna": 9.4, "h2o": 40.6}, "F1": {"rna": 3.3, "h2o": 46.7}, "G1": {"rna": 8.7, "h2o": 41.3}, "H1": {"rna": 6.4, "h2o": 43.6}, "A2": {"rna": 25.0, "h2o": 25.0}, "B2": {"rna": 22.9, "h2o": 27.1}, "C2": {"rna": 8.6, "h2o": 41.4}, "D2": {"rna": 25.0, "h2o": 25.0}, "E2": {"rna": 17.8, "h2o": 32.2}, "F2": {"rna": 9.4, "h2o": 40.6}, "G2": {"rna": 9.2, "h2o": 40.8}, "H2": {"rna": 12.4, "h2o": 37.6}, "A3": {"rna": 14.9, "h2o": 35.1}, "B3": {"rna": 25.0, "h2o": 25.0}, "C3": {"rna": 14.3, "h2o": 35.7}, "D3": {"rna": 25.0, "h2o": 25.0}, "E3": {"rna": 17.2, "h2o": 32.8}, "F3": {"rna": 25.0, "h2o": 25.0}, "G3": {"rna": 25.0, "h2o": 25.0}, "H3": {"rna": 25.6, "h2o": 24.4}, "A4": {"rna": 11.7, "h2o": 38.3}, "B4": {"rna": 10.2, "h2o": 39.8}, "C4": {"rna": 10.0, "h2o": 40.0}, "D4": {"rna": 22.6, "h2o": 27.4}, "E4": {"rna": 26.2, "h2o": 23.8}, "F4": {"rna": 25.0, "h2o": 25.0}, "G4": {"rna": 25.0, "h2o": 25.0}, "H4": {"rna": 14.0, "h2o": 36.0}, "A5": {"rna": 2.7, "h2o": 47.3}, "B5": {"rna": 8.4, "h2o": 41.6}, "C5": {"rna": 25.0, "h2o": 25.0}, "D5": {"rna": 7.7, "h2o": 42.3}, "E5": {"rna": 9.7, "h2o": 40.3}, "F5": {"rna": 17.2, "h2o": 32.8}, "G5": {"rna": 27.5, "h2o": 22.5}, "H5": {"rna": 6.3, "h2o": 43.7}, "A6": {"rna": 4.4, "h2o": 45.6}, "B6": {"rna": 7.9, "h2o": 42.1}, "C6": {"rna": 7.7, "h2o": 42.3}, "D6": {"rna": 15.4, "h2o": 34.6}, "E6": {"rna": 17.5, "h2o": 32.5}, "F6": {"rna": 25.0, "h2o": 25.0}, "G6": {"rna": 18.4, "h2o": 31.6}, "H6": {"rna": 6.9, "h2o": 43.1}, "A7": {"rna": 13.4, "h2o": 36.6}, "B7": {"rna": 25.0, "h2o": 25.0}, "C7": {"rna": 25.0, "h2o": 25.0}, "D7": {"rna": 25.0, "h2o": 25.0}, "E7": {"rna": 25.0, "h2o": 25.0}, "F7": {"rna": 16.3, "h2o": 33.7}, "G7": {"rna": 9.0, "h2o": 41.0}, "H7": {"rna": 27.6, "h2o": 22.4}, "A8": {"rna": 11.3, "h2o": 38.7}, "B8": {"rna": 15.0, "h2o": 35.0}, "C8": {"rna": 25.0, "h2o": 25.0}, "D8": {"rna": 25.0, "h2o": 25.0}, "E8": {"rna": 25.0, "h2o": 25.0}, "F8": {"rna": 17.5, "h2o": 32.5}, "G8": {"rna": 9.5, "h2o": 40.5}, "H8": {"rna": 2.4, "h2o": 47.6}, "A9": {"rna": 25.0, "h2o": 25.0}, "B9": {"rna": 5.3, "h2o": 44.7}, "C9": {"rna": 23.4, "h2o": 26.6}, "D9": {"rna": 3.9, "h2o": 46.1}, "E9": {"rna": 8.9, "h2o": 41.1}, "F9": {"rna": 25.0, "h2o": 25.0}, "G9": {"rna": 25.0, "h2o": 25.0}, "H9": {"rna": 25.0, "h2o": 25.0}, "A10": {"rna": 9.3, "h2o": 40.7}, "B10": {"rna": 3.8, "h2o": 46.2}, "C10": {"rna": 8.4, "h2o": 41.6}, "D10": {"rna": 7.6, "h2o": 42.4}, "E10": {"rna": 8.3, "h2o": 41.7}, "F10": {"rna": 18.5, "h2o": 31.5}, "G10": {"rna": 18.5, "h2o": 31.5}, "H10": {"rna": 8.8, "h2o": 41.2}, "A11": {"rna": 3.7, "h2o": 46.3}, "B11": {"rna": 21.1, "h2o": 28.9}, "C11": {"rna": 5.1, "h2o": 44.9}, "D11": {"rna": 25.0, "h2o": 25.0}, "E11": {"rna": 5.8, "h2o": 44.2}, "F11": {"rna": 8.3, "h2o": 41.7}, "G11": {"rna": 25.0, "h2o": 25.0}, "H11": {"rna": 15.3, "h2o": 34.7}, "A12": {"rna": 14.6, "h2o": 35.4}, "B12": {"rna": 9.6, "h2o": 40.4}, "C12": {"rna": 25.0, "h2o": 25.0}, "D12": {"rna": 7.7, "h2o": 42.3}, "E12": {"rna": 19.2, "h2o": 30.8}, "F12": {"rna": 25.0, "h2o": 25.0}, "G12": {"rna": 17.5, "h2o": 32.5}, "H12": {"rna": 4.3, "h2o": 45.7}},
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
