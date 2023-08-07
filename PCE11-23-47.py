from opentrons import protocol_api

config={"PLATES": {"1": {"A1": 0, "B1": 0, "C1": 0, "D1": 103.1, "E1": 19.6, "F1": 0, "G1": 45.9, "H1": 0, "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 0, "F2": 0, "G2": 0, "H2": 71.8, "A3": 131.4, "B3": 0, "C3": 13.4, "D3": 68.9, "E3": 0, "F3": 0, "G3": 0, "H3": 65.9, "A4": 119.3, "B4": 55.7, "C4": 0, "D4": 116.3, "E4": 0, "F4": 44.1, "G4": 49.1, "H4": 92.3, "A5": 31.2, "B5": 54.9, "C5": 96.4, "D5": 0, "E5": 0, "F5": 0, "G5": 48.8, "H5": 0, "A6": 0, "B6": 107.1, "C6": 0, "D6": 36.5, "E6": 0, "F6": 0, "G6": 0, "H6": 65.2, "A7": 0, "B7": 0, "C7": 0, "D7": 0, "E7": 0, "F7": 48.5, "G7": 0, "H7": 0, "A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 0, "F8": 86.0, "G8": 0, "H8": 11.9, "A9": 0, "B9": 0, "C9": 0, "D9": 0, "E9": 0, "F9": 0, "G9": 0, "H9": 0, "A10": 80.0, "B10": 51.7, "C10": 0, "D10": 0, "E10": 85.3, "F10": 0, "G10": 0, "H10": 0, "A11": 78.5, "B11": 0, "C11": 0, "D11": 68.7, "E11": 0, "F11": 0, "G11": 0, "H11": 0, "A12": 7.0, "B12": 0, "C12": 0, "D12": 27.7, "E12": 0, "F12": 66.1, "G12": 0, "H12": 0}, "2": {"A1": 0, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 0, "G1": 5.7, "H1": 111.6, "A2": 0, "B2": 0, "C2": 0, "D2": 70.6, "E2": 0, "F2": 0, "G2": 0, "H2": 47.3, "A3": 0, "B3": 70.7, "C3": 29.3, "D3": 0, "E3": 0, "F3": 0, "G3": 0, "H3": 0, "A4": 45.0, "B4": 0, "C4": 61.5, "D4": 0, "E4": 102.2, "F4": 0, "G4": 0, "H4": 0, "A5": 0, "B5": 76.9, "C5": 0, "D5": 8.7, "E5": 11.9, "F5": 0, "G5": 11.8, "H5": 0, "A6": 60.4, "B6": 144.9, "C6": 47.0, "D6": 0, "E6": 0, "F6": 0, "G6": 0, "H6": 0, "A7": 44.7, "B7": 0, "C7": 0, "D7": 0, "E7": 0, "F7": 9.7, "G7": 60.8, "H7": 0, "A8": 0, "B8": 29.8, "C8": 0, "D8": 102.0, "E8": 0, "F8": 15.9, "G8": 70.3, "H8": 0, "A9": 0, "B9": 95.7, "C9": 0, "D9": 0, "E9": 0, "F9": 65.1, "G9": 0, "H9": 59.2, "A10": 8.0, "B10": 46.2, "C10": 0, "D10": 0, "E10": 0, "F10": 0, "G10": 120.2, "H10": 107.7, "A11": 0, "B11": 0, "C11": 0, "D11": 16.4, "E11": 0, "F11": 10.2, "G11": 0, "H11": 135.3, "A12": 0, "B12": 0, "C12": 0, "D12": 0, "E12": 77.0, "F12": 0, "G12": 25.5, "H12": 0}, "3": {"A1": 86.4, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 0, "G1": 66.2, "H1": 0, "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 85.8, "F2": 0, "G2": 0, "H2": 0, "A3": 0, "B3": 149.2, "C3": 85.1, "D3": 0, "E3": 35.4, "F3": 0, "G3": 0, "H3": 0, "A4": 0, "B4": 115.9, "C4": 0, "D4": 0, "E4": 0, "F4": 0, "G4": 0, "H4": 0, "A5": 116.8, "B5": 0, "C5": 53.8, "D5": 0, "E5": 13.9, "F5": 54.7, "G5": 0, "H5": 23.2, "A6": 0, "B6": 0, "C6": 0, "D6": 0, "E6": 0, "F6": 55.9, "G6": 24.9, "H6": 0, "A7": 0, "B7": 82.9, "C7": 159.6, "D7": 0, "E7": 0, "F7": 0, "G7": 0, "H7": 8.7, "A8": 0, "B8": 38.1, "C8": 103.0, "D8": 35.2, "E8": 0, "F8": 0, "G8": 40.4, "H8": 0, "A9": 55.5, "B9": 0, "C9": 15.0, "D9": 0, "E9": 13.5, "F9": 95.1, "G9": 0, "H9": 0, "A10": 0, "B10": 0, "C10": 79.0, "D10": 0, "E10": 129.1, "F10": 0, "G10": 0, "H10": 71.1, "A11": 81.1, "B11": 0, "C11": 14.3, "D11": 0, "E11": 0, "F11": 0, "G11": 0, "H11": 0, "A12": 0, "B12": 0, "C12": 0, "D12": 0, "E12": 0, "F12": 0, "G12": 0, "H12": 0}}, "WELL_MAX_VOLUME": 180, "PROTOCOL_NAME": "PCE11-23-47"}

metadata = {
        'protocolName': config["PROTOCOL_NAME"],
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
            vol = min(volume-transferred, pipette.max_volume)
            pipette.aspirate(vol, water["A1"], rate=0.2)
            pipette.dispense(vol, plate[well], rate=0.5)
            transferred += vol
        pipette.blow_out(plate[well])
        pipette.touch_tip(plate[well])
    pipette.drop_tip()


def run(protocol: protocol_api.ProtocolContext):
    water = protocol.load_labware('nest_1_reservoir_195ml', 11)

    tiprack_p200 = protocol.load_labware('standard_96_tiprack_200ul', 10)
    p50 = protocol.load_instrument('p50_single', 'left', tip_racks=[tiprack_p200])
    p50.well_bottom_clearance.aspirate = 0
    p50.well_bottom_clearance.dispense = 0

    #tiprack_p10 = protocol.load_labware('standard_96_tiprack_10ul', 9)
    #p10 = protocol.load_instrument('p10_single', 'right', tip_racks=[tiprack_p10])
    #p10.well_bottom_clearance.aspirate = 0.5
    #p10.well_bottom_clearance.dispense = 0.5

    for plate_pos, well_vols in config["PLATES"].items():
        dest_plate = protocol.load_labware('axygen_96_wellplate_200ul', plate_pos)
        dispense_water_to(dest_plate, water, well_vols, p50)
