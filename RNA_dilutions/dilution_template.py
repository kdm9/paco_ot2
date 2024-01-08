from opentrons import protocol_api

config = {
    "PLATE_NAME": "__PLATE_NAME__",
    "VOLUMES": __VOLUMES__,
}

metadata = {
        'protocolName': "__PROTOCOL_NAME__",
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
