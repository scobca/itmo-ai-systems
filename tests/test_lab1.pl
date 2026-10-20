:- begin_tests(factorio).
:- consult('../src/lab1/factorio.pl').

test(unary_fact_count) :-
    findall(X, resource(X), Resources), length(Resources, N), N >= 20.
test(binary_relation_count) :-
    findall(M-T, machine_type(M,T), Relations), length(Relations, N), N >= 7.
test(simple_fact) :- resource(iron_ore).
test(variables, true(Machines == [stone_furnace,steel_furnace,electric_furnace])) :-
    findall(M, can_craft(M,iron_plate,nauvis), Machines).
test(conjunction) :- powered_crafter(electric_furnace,iron_plate,nauvis,electricity).
test(negation) :- solid_resource(iron_ore), \+ solid_resource(water).
test(recursion, true(Materials == [copper_ore,iron_ore])) :-
    setof(M, raw_material(electronic_circuit,M), Materials).
test(fluid) :- once(uses_fluid(sulfur)), \+ uses_fluid(steel_plate).
test(disjunction) :- once((can_craft(foundry,molten_iron,vulcanus);
                      can_craft(chemical_plant,molten_iron,vulcanus))).
test(planets, [fail]) :- can_craft(foundry,molten_iron,nauvis).
test(speed) :- faster_than(steel_furnace,stone_furnace).
test(all_products_have_recipe) :-
    forall(intermediate_product(P),
           (recipe_yield(P,Y), Y > 0, recipe_type(P,T),
            machine_type(_,T), ingredient(P,_,_))).
test(all_ingredients_grounded) :-
    forall(ingredient(_,M,Q), (Q > 0, (resource(M); intermediate_product(M)))).

:- end_tests(factorio).
