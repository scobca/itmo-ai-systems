% ingredient(Product, Material, Amount): input for one recipe execution.
% recipe_yield(Product, Count): output from one execution.
% recipe_type(Product, MachineType): required category of machine.
ingredient(iron_plate, iron_ore, 1).
ingredient(copper_plate, copper_ore, 1).
ingredient(steel_plate, iron_plate, 5).
ingredient(stone_brick, stone, 2).
ingredient(iron_gear_wheel, iron_plate, 2).
ingredient(copper_cable, copper_plate, 1).
ingredient(electronic_circuit, iron_plate, 1).
ingredient(electronic_circuit, copper_cable, 3).
ingredient(plastic_bar, petroleum_gas, 20).
ingredient(plastic_bar, coal, 1).
ingredient(sulfur, petroleum_gas, 30).
ingredient(sulfur, water, 30).
ingredient(molten_iron, iron_ore, 50).
ingredient(molten_iron, calcite, 1).

recipe_yield(iron_plate, 1).
recipe_yield(copper_plate, 1).
recipe_yield(steel_plate, 1).
recipe_yield(stone_brick, 1).
recipe_yield(iron_gear_wheel, 1).
recipe_yield(copper_cable, 2).
recipe_yield(electronic_circuit, 1).
recipe_yield(plastic_bar, 2).
recipe_yield(sulfur, 2).
recipe_yield(molten_iron, 500).

recipe_type(iron_plate, furnace).
recipe_type(copper_plate, furnace).
recipe_type(steel_plate, furnace).
recipe_type(stone_brick, furnace).
recipe_type(iron_gear_wheel, assembler).
recipe_type(copper_cable, assembler).
recipe_type(electronic_circuit, assembler).
recipe_type(plastic_bar, chemical_plant).
recipe_type(sulfur, chemical_plant).
recipe_type(molten_iron, foundry).
