from opentrons import protocol_api

config = {
    "PLATES": {"VaccIsolP1": {"A1": 74.6, "B1": 0, "C1": 63.4, "D1": 111.3, "E1": 56.2, "F1": 28.5, "G1": 54.2, "H1": 98.7, "A2": 44.7, "B2": 55.7, "C2": 113.6, "D2": 79.3, "E2": 77.6, "F2": 52.1, "G2": 76.8, "H2": 99.4, "A3": 29.4, "B3": 11.7, "C3": 0, "D3": 0, "E3": 55.1, "F3": 81.4, "G3": 35.4, "H3": 35.6, "A4": 78.3, "B4": 54.5, "C4": 48.9, "D4": 95.2, "E4": 28.8, "F4": 101.4, "G4": 79.0, "H4": 72.9, "A5": 26.4, "B5": 43.6, "C5": 45.1, "D5": 0, "E5": 33.1, "F5": 64.9, "G5": 28.2, "H5": 42.9, "A6": 40.1, "B6": 55.7, "C6": 0, "D6": 65.5, "E6": 31.2, "F6": 70.6, "G6": 58.0, "H6": 113.0, "A7": 29.6, "B7": 52.9, "C7": 42.6, "D7": 39.0, "E7": 104.9, "F7": 103.0, "G7": 0, "H7": 0, "A8": 0, "B8": 56.9, "C8": 14.5, "D8": 59.8, "E8": 103.0, "F8": 32.7, "G8": 0, "H8": 74.4, "A9": 0, "B9": 22.2, "C9": 112.0, "D9": 64.7, "E9": 108.1, "F9": 0, "G9": 80.5, "H9": 108.4, "A10": 0, "B10": 0, "C10": 40.6, "D10": 52.7, "E10": 51.2, "F10": 39.0, "G10": 65.9, "H10": 0, "A11": 0, "B11": 59.6, "C11": 48.0, "D11": 60.1, "E11": 43.0, "F11": 30.0, "G11": 32.9, "H11": 45.5, "A12": 47.3, "B12": 41.3, "C12": 40.7, "D12": 43.3, "E12": 26.4, "F12": 45.7, "G12": 0, "H12": 0}, "VaccIsolP2": {"A1": 94.4, "B1": 16.8, "C1": 0, "D1": 37.8, "E1": 0, "F1": 37.2, "G1": 131.5, "H1": 47.0, "A2": 35.9, "B2": 81.3, "C2": 79.8, "D2": 77.5, "E2": 81.1, "F2": 46.0, "G2": 72.3, "H2": 45.2, "A3": 24.3, "B3": 87.1, "C3": 56.6, "D3": 52.4, "E3": 21.0, "F3": 25.4, "G3": 0, "H3": 69.7, "A4": 69.0, "B4": 112.4, "C4": 78.6, "D4": 71.7, "E4": 72.3, "F4": 24.2, "G4": 24.3, "H4": 84.3, "A5": 89.0, "B5": 40.0, "C5": 92.2, "D5": 0, "E5": 0, "F5": 93.5, "G5": 82.9, "H5": 0, "A6": 43.9, "B6": 38.3, "C6": 85.6, "D6": 29.6, "E6": 13.3, "F6": 60.5, "G6": 74.2, "H6": 40.9, "A7": 47.3, "B7": 38.6, "C7": 38.2, "D7": 30.3, "E7": 0, "F7": 68.4, "G7": 49.9, "H7": 10.2, "A8": 45.3, "B8": 38.6, "C8": 59.4, "D8": 50.9, "E8": 89.7, "F8": 79.4, "G8": 37.5, "H8": 76.7, "A9": 83.5, "B9": 82.1, "C9": 52.0, "D9": 87.8, "E9": 0, "F9": 45.2, "G9": 78.2, "H9": 50.4, "A10": 84.1, "B10": 79.7, "C10": 72.1, "D10": 16.4, "E10": 8.5, "F10": 0, "G10": 51.2, "H10": 32.0, "A11": 76.0, "B11": 83.2, "C11": 32.8, "D11": 68.7, "E11": 30.3, "F11": 13.2, "G11": 90.1, "H11": 0, "A12": 0, "B12": 125.3, "C12": 26.5, "D12": 22.4, "E12": 39.6, "F12": 21.1, "G12": 10.2, "H12": 12.3}},
    "WELL_MAX_VOLUME": 180,
}

metadata = {
        'protocolName': "VaccIsolP1__VaccIsolP2",
        'author': 'Kevin Murray',
        'apiLevel': '2.9',
}

def dispense_water_to(plate, water, well_vols, pipette):
    pipette.pick_up_tip()
    for well, volume in well_vols.items():
        if volume < pipette.min_volume:
            continue
        if volume > config["WELL_MAX_VOLUME"]:
            raise ValueError(f"ERROR! overfull well {well} on plate {plate}")
        transferred = 0
        while transferred < volume:
            todo = volume-transferred
            if todo > pipette.max_volume and todo <= pipette.max_volume*2:
                vol = todo/2
            else:
                vol = min(todo, pipette.max_volume)
            pipette.aspirate(vol, water["A1"], rate=1)
            pipette.dispense(vol, plate[well], rate=1)
            transferred += vol
        pipette.blow_out(plate[well])
        pipette.touch_tip(plate[well])
    pipette.drop_tip()


def run(protocol: protocol_api.ProtocolContext):
    water = protocol.load_labware('integra_1_reservoir_150ml', 11)

    tiprack_p200 = protocol.load_labware('standard_96_tiprack_200ul', 10)
    p50 = protocol.load_instrument('p50_single', 'left', tip_racks=[tiprack_p200])
    p50.well_bottom_clearance.aspirate = 0
    p50.well_bottom_clearance.dispense = 0

    #tiprack_p10 = protocol.load_labware('standard_96_tiprack_10ul', 9)
    #p10 = protocol.load_instrument('p10_single', 'right', tip_racks=[tiprack_p10])
    #p10.well_bottom_clearance.aspirate = 0.5
    #p10.well_bottom_clearance.dispense = 0.5

    pos = 1
    for plate_name, well_vols in config["PLATES"].items():
        dest_plate = protocol.load_labware('axygen_96_wellplate_200ul', pos, label=plate_name)
        dispense_water_to(dest_plate, water, well_vols, p50)
        pos += 1
