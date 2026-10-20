% solid_resource/1: negation distinguishes solid inputs from fluids.
solid_resource(X) :- resource(X), \+ fluid_resource(X).

% can_craft/3: machine, product and planet satisfy recipe and location.
can_craft(Machine, Product, Planet) :-
    machine(Machine), intermediate_product(Product),
    machine_type(Machine, Type), recipe_type(Product, Type),
    available_on(Machine, Planet).

% powered_crafter/4: conjunction with the requested energy source.
powered_crafter(Machine, Product, Planet, Power) :-
    can_craft(Machine, Product, Planet), power_source(Machine, Power).

% raw_material/2: recursively trace a product to its raw inputs.
raw_material(Product, Material) :- ingredient(Product, Material, _), resource(Material).
raw_material(Product, Material) :-
    ingredient(Product, Component, _), intermediate_product(Component),
    raw_material(Component, Material).

% uses_fluid/1: a product has a fluid anywhere in its dependency chain.
uses_fluid(Product) :- raw_material(Product, Material), fluid_resource(Material).

% alternative_machine/3: another available machine for a product.
alternative_machine(Machine, Alternative, Product) :-
    can_craft(Machine, Product, Planet),
    can_craft(Alternative, Product, Planet), Machine \= Alternative.

% faster_than/2: compare two machines' crafting speeds.
faster_than(First, Second) :-
    machine_speed(First, FirstSpeed), machine_speed(Second, SecondSpeed),
    FirstSpeed > SecondSpeed.

