from opentrons import protocol_api

config = {
    "PLATES": {"PCE038": {"A1": 190.0, "B1": 185.4, "C1": 190.0, "D1": 190.0, "E1": 190.0, "F1": 190.0, "G1": 190.0, "H1": 190.0, "A2": 190.0, "B2": 190.0, "C2": 190.0, "D2": 190.0, "E2": 190.0, "F2": 190.0, "G2": 190.0, "H2": 190.0, "A3": 190.0, "B3": 190.0, "C3": 47.8, "D3": 47.0, "E3": 190.0, "F3": 190.0, "G3": 190.0, "H3": 190.0, "A4": 190.0, "B4": 190.0, "C4": 190.0, "D4": 190.0, "E4": 190.0, "F4": 190.0, "G4": 88.6, "H4": 190.0, "A5": 190.0, "B5": 190.0, "C5": 190.0, "D5": 190.0, "E5": 190.0, "F5": 190.0, "G5": 190.0, "H5": 190.0, "A6": 190.0, "B6": 190.0, "C6": 190.0, "D6": 190.0, "E6": 190.0, "F6": 64.8, "G6": 190.0, "H6": 190.0}},
    "WELL_MAX_VOLUME": 190.0,
}

metadata = {
        'protocolName': "PCE038",
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
