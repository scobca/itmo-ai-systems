"""Generate a Protégé-compatible Turtle ontology from the Prolog fact files."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name("factorio.ttl")
VALUE = r"([^,()\s]+)"


def facts(path: str, name: str, arity: int) -> list[tuple[str, ...]]:
    source = (ROOT / path).read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^{name}\(" + r",\s*".join([VALUE] * arity) + r"\)\.$",
        re.MULTILINE,
    )
    matches = pattern.findall(source)
    return [(match,) if isinstance(match, str) else match for match in matches]


resources = [item for (item,) in facts("base/resources.pl", "resource", 1)]
products = [item for (item,) in facts("base/intermediates.pl", "intermediate_product", 1)]
machines = [item for (item,) in facts("base/machines/machines.pl", "machine", 1)]
types = dict(facts("base/machines/machines.pl", "machine_type", 2))
power = dict(facts("base/machines/machines.pl", "power_source", 2))
speeds = dict(facts("base/machines/machines.pl", "machine_speed", 2))
powers = dict(facts("base/machines/machines.pl", "machine_power", 2))
recipe_types = dict(facts("base/recipes.pl", "recipe_type", 2))
available = facts("base/machines/recipes.pl", "available_on", 2)
ingredients = facts("base/recipes.pl", "ingredient", 3)
yields = dict(facts("base/recipes.pl", "recipe_yield", 2))
fluids = {item for (item,) in facts("base/resources.pl", "fluid_resource", 1)}

assert len(resources) >= 20 and len(products) == len(recipe_types) == len(yields)
assert set(machines) == set(types) == set(power) == set(speeds) == set(powers)
assert all(material in resources + products for _, material, _ in ingredients)
assert all(product in products for product, _, _ in ingredients)
assert all(machine in machines for machine, _ in available)

header = """@prefix : <https://example.org/factorio#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/factorio> a owl:Ontology ;
  rdfs:comment "Educational Factorio production subset derived from the Prolog facts."@en .

:ProductionEntity a owl:Class .
:Material a owl:Class ; rdfs:subClassOf :ProductionEntity .
:RawResource a owl:Class ; rdfs:subClassOf :Material ;
  owl:disjointWith :IntermediateProduct .
:FluidResource a owl:Class ; rdfs:subClassOf :RawResource .
:SolidResource a owl:Class ; rdfs:subClassOf :RawResource ;
  owl:disjointWith :FluidResource .
:IntermediateProduct a owl:Class ; rdfs:subClassOf :Material .
:MetalPlate a owl:Class ; rdfs:subClassOf :IntermediateProduct .
:Machine a owl:Class ; rdfs:subClassOf :ProductionEntity ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :poweredBy ;
                    owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                    owl:onClass :PowerSource ] .
:Furnace a owl:Class ; rdfs:subClassOf :Machine ; owl:disjointWith :Assembler .
:Assembler a owl:Class ; rdfs:subClassOf :Machine ; owl:disjointWith :ChemicalPlant .
:ChemicalPlant a owl:Class ; rdfs:subClassOf :Machine ; owl:disjointWith :Foundry .
:Foundry a owl:Class ; rdfs:subClassOf :Machine ; owl:disjointWith :Furnace .
:Planet a owl:Class .
:PowerSource a owl:Class .
:Recipe a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :produces ;
                    owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                    owl:onClass :IntermediateProduct ] .
:IngredientUse a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :material ;
                    owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                    owl:onClass :Material ] .

:availableOn a owl:ObjectProperty ; rdfs:domain :Machine ; rdfs:range :Planet ;
  rdfs:comment "Local availability without interplanetary transport."@en .
:poweredBy a owl:ObjectProperty ; rdfs:domain :Machine ; rdfs:range :PowerSource .
:supportsRecipe a owl:ObjectProperty ; rdfs:domain :Machine ; rdfs:range :Recipe .
:produces a owl:ObjectProperty ; rdfs:domain :Recipe ; rdfs:range :IntermediateProduct .
:hasIngredientUse a owl:ObjectProperty ; rdfs:domain :Recipe ; rdfs:range :IngredientUse .
:material a owl:ObjectProperty ; rdfs:domain :IngredientUse ; rdfs:range :Material .
:speed a owl:DatatypeProperty ; rdfs:domain :Machine ; rdfs:range xsd:decimal .
:powerKW a owl:DatatypeProperty ; rdfs:domain :Machine ; rdfs:range xsd:nonNegativeInteger .
:quantity a owl:DatatypeProperty ; rdfs:domain :IngredientUse ; rdfs:range xsd:positiveInteger .
:yield a owl:DatatypeProperty ; rdfs:domain :Recipe ; rdfs:range xsd:positiveInteger .

:nauvis a :Planet .
:vulcanus a :Planet .
:fuel a :PowerSource ; owl:differentFrom :electricity .
:electricity a :PowerSource .
"""

lines = [header]
for item in resources:
    lines.append(f":{item} a :{'FluidResource' if item in fluids else 'SolidResource'} .")
for item in products:
    kind = "MetalPlate" if item in {"iron_plate", "copper_plate", "steel_plate"} else "IntermediateProduct"
    lines.append(f":{item} a :{kind} .")

class_names = {
    "furnace": "Furnace", "assembler": "Assembler",
    "chemical_plant": "ChemicalPlant", "foundry": "Foundry",
}
for item in machines:
    locations = " ; ".join(f":availableOn :{planet}" for machine, planet in available if machine == item)
    lines.append(
        f":{item} a :{class_names[types[item]]} ; :poweredBy :{power[item]} ; "
        f":speed \"{speeds[item]}\"^^xsd:decimal ; "
        f":powerKW \"{powers[item]}\"^^xsd:nonNegativeInteger ; {locations} ."
    )
for item in products:
    recipe = f"{item}_recipe"
    lines.append(
        f":{recipe} a :Recipe ; :produces :{item} ; "
        f":yield \"{yields[item]}\"^^xsd:positiveInteger ."
    )
    for machine in machines:
        if types[machine] == recipe_types[item]:
            lines.append(f":{machine} :supportsRecipe :{recipe} .")

for index, (product, material, quantity) in enumerate(ingredients, 1):
    use = f"ingredient_use_{index}"
    lines.append(f":{product}_recipe :hasIngredientUse :{use} .")
    lines.append(
        f":{use} a :IngredientUse ; :material :{material} ; "
        f":quantity \"{quantity}\"^^xsd:positiveInteger ."
    )

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUT} ({len(products)} recipes, {len(ingredients)} ingredient uses)")
