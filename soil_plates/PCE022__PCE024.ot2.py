from opentrons import protocol_api

config = {
    "PLATES": {"PCE022": {"A1": 153.2, "B1": 0, "C1": 100.8, "D1": 147.5, "E1": 155.8, "F1": 0, "G1": 156.8, "H1": 125.0, "A2": 161.5, "B2": 14.1, "C2": 0, "D2": 176.5, "E2": 153.0, "F2": 141.1, "G2": 61.1, "H2": 13.2, "A3": 124.9, "B3": 152.0, "C3": 157.7, "D3": 158.8, "E3": 158.5, "F3": 52.1, "G3": 156.0, "H3": 121.6, "A4": 98.9, "B4": 138.5, "C4": 66.5, "D4": 125.7, "E4": 146.4, "F4": 45.6, "G4": 137.0, "H4": 151.4, "A5": 103.8, "B5": 123.6, "C5": 95.4, "D5": 137.9, "E5": 131.7, "F5": 131.7, "G5": 0, "H5": 134.2, "A6": 82.9, "B6": 151.3, "C6": 154.5, "D6": 147.1, "E6": 0, "F6": 144.4, "G6": 146.2, "H6": 0, "A7": 135.1, "B7": 87.3, "C7": 170.1, "D7": 137.0, "E7": 163.0, "F7": 68.2, "G7": 141.6, "H7": 31.1, "A8": 148.6, "B8": 120.1, "C8": 63.7, "D8": 137.9, "E8": 120.6, "F8": 166.0, "G8": 142.2, "H8": 130.8, "A9": 102.8, "B9": 133.5, "C9": 160.7, "D9": 127.3, "E9": 145.5, "F9": 122.6, "G9": 31.5, "H9": 128.3, "A10": 142.8, "B10": 35.8, "C10": 149.2, "D10": 111.1, "E10": 65.9, "F10": 68.3, "G10": 136.3, "H10": 109.3, "A11": 127.2, "B11": 119.0, "C11": 160.2, "D11": 165.1, "E11": 151.2, "F11": 161.2, "G11": 112.7, "H11": 36.8, "A12": 154.5, "B12": 165.7, "C12": 169.2, "D12": 169.4, "E12": 165.1, "F12": 145.0, "G12": 77.4, "H12": 128.8}, "PCE024": {"A1": 0, "B1": 178.6, "C1": 146.4, "D1": 166.6, "E1": 83.6, "F1": 170.3, "G1": 165.2, "H1": 41.2, "A2": 151.5, "B2": 135.3, "C2": 24.1, "D2": 142.3, "E2": 0, "F2": 158.5, "G2": 52.7, "H2": 102.9, "A3": 20.3, "B3": 0, "C3": 127.4, "D3": 138.9, "E3": 159.9, "F3": 0, "G3": 36.6, "H3": 137.9, "A4": 25.0, "B4": 138.2, "C4": 158.3, "D4": 145.5, "E4": 146.2, "F4": 106.5, "G4": 75.5, "H4": 0, "A5": 0, "B5": 165.9, "C5": 0, "D5": 77.2, "E5": 7.2, "F5": 158.7, "G5": 166.2, "H5": 183.8, "A6": 142.7, "B6": 149.3, "C6": 154.8, "D6": 172.6, "E6": 170.7, "F6": 0, "G6": 154.8, "H6": 178.0, "A7": 166.7, "B7": 173.2, "C7": 167.4, "D7": 150.3, "E7": 64.9, "F7": 0, "G7": 0, "H7": 0, "A8": 154.1, "B8": 161.0, "C8": 51.7, "D8": 161.3, "E8": 12.3, "F8": 176.4, "G8": 145.7, "H8": 0, "A9": 130.8, "B9": 139.3, "C9": 0, "D9": 113.8, "E9": 0, "F9": 137.5, "G9": 119.4, "H9": 62.9, "A10": 0, "B10": 115.2, "C10": 169.6, "D10": 177.2, "E10": 121.0, "F10": 160.4, "G10": 0, "H10": 188.9, "A11": 12.9, "B11": 173.1, "C11": 131.8, "D11": 177.8, "E11": 171.8, "F11": 156.0, "G11": 79.1, "H11": 148.5, "A12": 184.3, "B12": 19.5, "C12": 0, "D12": 165.8, "E12": 23.3, "F12": 0, "G12": 53.7, "H12": 70.3}},
    "WELL_MAX_VOLUME": 190.0,
}

metadata = {
        'protocolName': "PCE022__PCE024",
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
