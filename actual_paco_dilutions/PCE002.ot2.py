from opentrons import protocol_api

config = {
    "PLATES": {"PCE002": {"A1": 0, "B1": 0, "C1": 8.4, "D1": 0, "E1": 0, "F1": 0, "G1": 0, "H1": 0, "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 10.8, "F2": 0, "G2": 0, "H2": 0, "A3": 0, "B3": 0, "C3": 0, "D3": 0, "E3": 8.4, "F3": 7.4, "G3": 0, "H3": 0, "A4": 0, "B4": 0, "C4": 0, "D4": 0, "E4": 7.3, "F4": 11.9, "G4": 0, "H4": 6.0, "A5": 0, "B5": 0, "C5": 0, "D5": 0, "E5": 9.3, "F5": 0, "G5": 0, "H5": 0, "A6": 7.6, "B6": 7.9, "C6": 0, "D6": 0, "E6": 0, "F6": 0, "G6": 0, "H6": 0, "A7": 0, "B7": 0, "C7": 5.5, "D7": 5.2, "E7": 5.1, "F7": 0, "G7": 0, "H7": 0, "A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 9.5, "F8": 0, "G8": 0, "H8": 0, "A9": 0, "B9": 0, "C9": 0, "D9": 0, "E9": 0, "F9": 0, "G9": 0, "H9": 0, "A10": 0, "B10": 0, "C10": 8.5, "D10": 5.4, "E10": 0, "F10": 0, "G10": 5.6, "H10": 0, "A11": 16.6, "B11": 0, "C11": 0, "D11": 0, "E11": 0, "F11": 0, "G11": 0, "H11": 0, "A12": 14.9, "B12": 0, "C12": 0, "D12": 0, "E12": 0, "F12": 5.1, "G12": 0, "H12": 0}},
    "WELL_MAX_VOLUME": 190.0,
}

metadata = {
        'protocolName': "PCE002",
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
