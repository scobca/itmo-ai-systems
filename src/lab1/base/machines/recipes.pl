% available_on/2: local availability without interplanetary transport.
% A foundry may be shipped elsewhere in the full game; transport is outside
% this educational model.
available_on(stone_furnace, nauvis).
available_on(steel_furnace, nauvis).
available_on(electric_furnace, nauvis).
available_on(assembling_machine_1, nauvis).
available_on(assembling_machine_2, nauvis).
available_on(chemical_plant, nauvis).
available_on(stone_furnace, vulcanus).
available_on(steel_furnace, vulcanus).
available_on(electric_furnace, vulcanus).
available_on(assembling_machine_1, vulcanus).
available_on(assembling_machine_2, vulcanus).
available_on(chemical_plant, vulcanus).
available_on(foundry, vulcanus).

% machine_ingredient/3: selected construction recipes.
machine_ingredient(stone_furnace, stone, 5).
machine_ingredient(steel_furnace, steel_plate, 6).
machine_ingredient(steel_furnace, stone_brick, 10).
machine_ingredient(electric_furnace, steel_plate, 10).
machine_ingredient(electric_furnace, stone_brick, 10).
machine_ingredient(electric_furnace, electronic_circuit, 5).
