from opentrons import protocol_api

config = {
    "PLATES": {"PCE030": {"A1": 0, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 0, "G1": 0, "H1": 0, "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 0, "F2": 0, "G2": 0, "H2": 0, "A3": 0, "B3": 0, "C3": 0, "D3": 0, "E3": 0, "F3": 0, "G3": 0, "H3": 0, "A4": 0, "B4": 0, "C4": 0, "D4": 0, "E4": 0, "F4": 0, "G4": 0, "H4": 0, "A5": 0, "B5": 0, "C5": 0, "D5": 0, "E5": 0, "F5": 0, "G5": 0, "H5": 0, "A6": 0, "B6": 0, "C6": 0, "D6": 0, "E6": 0, "F6": 0, "G6": 0, "H6": 0, "A7": 0, "B7": 0, "C7": 0, "D7": 0, "E7": 0, "F7": 0, "G7": 0, "H7": 0, "A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 0, "F8": 0, "G8": 0, "H8": 0, "A9": 0, "B9": 0, "C9": 0, "D9": 0, "E9": 0, "F9": 0, "G9": 0, "H9": 0, "A10": 0, "B10": 0, "C10": 0, "D10": 0, "E10": 0, "F10": 0, "G10": 0, "H10": 0, "A11": 16.6, "B11": 0, "C11": 0, "D11": 0, "E11": 0, "F11": 0, "G11": 5.9, "H11": 0, "A12": 0, "B12": 0, "C12": 0, "D12": 0, "E12": 0, "F12": 0, "G12": 0, "H12": 29.7}, "PCE031": {"A1": 0, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 24.7, "G1": 16.3, "H1": 0, "A2": 0, "B2": 23.9, "C2": 0, "D2": 26.7, "E2": 16.7, "F2": 0, "G2": 0, "H2": 0, "A3": 0, "B3": 29.1, "C3": 32.4, "D3": 180, "E3": 0, "F3": 35.7, "G3": 12.3, "H3": 0, "A4": 33.0, "B4": 0, "C4": 0, "D4": 8.1, "E4": 114.5, "F4": 0, "G4": 0, "H4": 0, "A5": 0, "B5": 24.2, "C5": 0, "D5": 0, "E5": 0, "F5": 29.3, "G5": 0, "H5": 33.2, "A6": 13.6, "B6": 13.9, "C6": 0, "D6": 0, "E6": 0, "F6": 0, "G6": 25.0, "H6": 73.2, "A7": 29.2, "B7": 22.9, "C7": 0, "D7": 5.2, "E7": 0, "F7": 0, "G7": 0, "H7": 0, "A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 0, "F8": 0, "G8": 133.3, "H8": 0, "A9": 0, "B9": 0, "C9": 0, "D9": 0, "E9": 0, "F9": 0, "G9": 0, "H9": 0, "A10": 0, "B10": 0, "C10": 0, "D10": 0, "E10": 0, "F10": 0, "G10": 0, "H10": 0, "A11": 0, "B11": 0, "C11": 0, "D11": 0, "E11": 0, "F11": 0, "G11": 0, "H11": 0, "A12": 0, "B12": 0, "C12": 0, "D12": 0, "E12": 0, "F12": 0, "G12": 0, "H12": 0}},
    "WELL_MAX_VOLUME": 180,
}

metadata = {
        'protocolName': "PCE030__PCE031",
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
