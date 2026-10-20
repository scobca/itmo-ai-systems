:- begin_tests(ontology).
:- use_module(library(semweb/rdf11)).
:- use_module(library(semweb/turtle)).
:- rdf_register_prefix(ex, 'https://example.org/factorio#').
:- prolog_load_context(directory, Dir),
   directory_file_path(Dir, '../src/lab1/ontology/factorio.ttl', File),
   rdf_load(File, [format(turtle)]).

test(recipe_and_product) :-
    rdf(ex:iron_plate_recipe, ex:produces, ex:iron_plate).
test(machine_and_planet) :-
    rdf(ex:foundry, ex:availableOn, ex:vulcanus),
    \+ rdf(ex:foundry, ex:availableOn, ex:nauvis).
test(class_hierarchy) :-
    rdf_reachable(ex:'MetalPlate', rdfs:subClassOf, ex:'ProductionEntity'),
    rdf(ex:iron_plate, rdf:type, ex:'MetalPlate').
test(ingredient_quantities) :-
    findall(U, rdf(ex:electronic_circuit_recipe, ex:hasIngredientUse, U), Uses),
    length(Uses, 2),
    rdf(_, ex:material, ex:copper_cable).
test(power_cardinality_axiom) :-
    rdf(ex:'Machine', rdfs:subClassOf, Restriction),
    rdf(Restriction, owl:onProperty, ex:poweredBy),
    rdf(Restriction, owl:qualifiedCardinality, _).
test(individuals_not_explicitly_disjoint) :-
    \+ (rdf(I, rdf:type, ex:'RawResource'),
        rdf(I, rdf:type, ex:'IntermediateProduct')).

:- end_tests(ontology).
