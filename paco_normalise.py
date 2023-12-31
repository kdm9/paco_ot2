from opentrons import protocol_api

metadata = {
        'protocolName': 'NormPlatePrepPaco',
        'author': 'Kevin Murray',
        'apiLevel': '2.9',
}

CONFIG = {}

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
