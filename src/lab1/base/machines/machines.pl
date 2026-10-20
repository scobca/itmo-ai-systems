% machine/1 lists production devices considered by the DSS.
machine(stone_furnace).
machine(steel_furnace).
machine(electric_furnace).
machine(assembling_machine_1).
machine(assembling_machine_2).
machine(chemical_plant).
machine(foundry).

% machine_type/2 relates a machine to its recipe category.
machine_type(stone_furnace, furnace).
machine_type(steel_furnace, furnace).
machine_type(electric_furnace, furnace).
machine_type(assembling_machine_1, assembler).
machine_type(assembling_machine_2, assembler).
machine_type(chemical_plant, chemical_plant).
machine_type(foundry, foundry).

% power_source/2, machine_speed/2 and machine_power/2 are attributes.
% machine_power is electrical draw in kW; fuel machines draw zero electricity.
power_source(stone_furnace, fuel).
power_source(steel_furnace, fuel).
power_source(electric_furnace, electricity).
power_source(assembling_machine_1, electricity).
power_source(assembling_machine_2, electricity).
power_source(chemical_plant, electricity).
power_source(foundry, electricity).

machine_speed(stone_furnace, 1.0).
machine_speed(steel_furnace, 2.0).
machine_speed(electric_furnace, 2.0).
machine_speed(assembling_machine_1, 0.5).
machine_speed(assembling_machine_2, 0.75).
machine_speed(chemical_plant, 1.0).
machine_speed(foundry, 4.0).

machine_power(stone_furnace, 0).
machine_power(steel_furnace, 0).
machine_power(electric_furnace, 180).
machine_power(assembling_machine_1, 75).
machine_power(assembling_machine_2, 150).
machine_power(chemical_plant, 210).
machine_power(foundry, 2500).
