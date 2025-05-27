from opentrons import protocol_api

metadata = {
    "apiLevel": "2.11",
    "protocolName": "Diluciones en placa PCR para Mechi/ Ari",
    "description": """Agregar 5 uL de DMSO (excepto fila A) y realizar diluciones seriadas al 1/2 
    desde A hacia H en columnas 1 a 12, usando pipeta single.""",
    "author": "Aguero Franco Agustin"
}

def run(ctx: protocol_api.ProtocolContext):
    # LABWARE
    plate = ctx.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 8)
    plate.set_offset(x=0.00, y=2.00, z=0.00)
    tube_rack = ctx.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", 11)
    tube_rack.set_offset(x=0.00, y=2.00, z=2.00)
    tiprack = ctx.load_labware("opentrons_96_tiprack_20ul", 9)

    # PIPETA
    pipette = ctx.load_instrument("p20_single_gen2", "right", tip_racks=[tiprack])

    # FUENTE DE DMSO
    fuente = tube_rack.wells_by_name()["A1"]

    # PASO 1: Agregar 5 uL de DMSO en filas B a H
    pipette.pick_up_tip()
    for col in plate.columns():
        for well in col[1:]:  # fila B (1) a H (7)
            pipette.aspirate(5, fuente)
            pipette.dispense(5, well)
            pipette.blow_out(well)
            pipette.touch_tip(well, v_offset=-2)
    pipette.drop_tip()

    # PASO 2: Diluciones desde fila A hacia H en cada columna
    for col in plate.columns():
        pipette.pick_up_tip()
        for i in range(0, 7):  # desde fila A (0) a H (7)
            origen = col[i]
            destino = col[i + 1]
            pipette.aspirate(5, origen)
            pipette.dispense(5, destino)
            pipette.mix(2, 10, destino)
            pipette.blow_out(destino)
            pipette.touch_tip(destino, v_offset=-2)
        pipette.drop_tip()