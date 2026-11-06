# Модуль 1: Factorio

Учебная модель производственной цепочки Factorio для лабораторных 1 и 2.

## Запуск

```sh
swipl -q -s src/lab1/factorio.pl
python3 src/lab2/dss.py
python3 src/lab2/dss.py --text 'product: iron_plate; planet: nauvis; priority: speed; energy: electricity'
```

В интерактивном режиме DSS запрашивает недостающие `product`, `planet` и
`priority`. Поле `energy` необязательно: по умолчанию используется `any`.
Ввод и ответы программы — на английском; значения продуктов и планет
совпадают с атомами Prolog из лабораторной 1 (`iron_plate`, `nauvis` и т. д.).
Поля отделяются точкой с запятой. Допустимые значения перечисляются в
сообщении об ошибке; поиск по подстроке не выполняется.

Примеры запросов в SWI-Prolog:

```prolog
?- resource(iron_ore).
?- findall(M, can_craft(M, iron_plate, nauvis), Machines).
?- setof(R, raw_material(electronic_circuit, R), Resources).
?- powered_crafter(M, iron_plate, nauvis, electricity).
?- solid_resource(R), \+ fluid_resource(R).
?- (can_craft(foundry, molten_iron, vulcanus) ; can_craft(chemical_plant, molten_iron, vulcanus)).
```

## Структура

- `base/resources.pl`: сырье, жидкости.
- `base/intermediates.pl`: продукты.
- `base/recipes.pl`: ингредиенты, выход, тип рецепта.
- `base/machines/machines.pl`: машины, классы, энергия, скорость и электрическая мощность.
- `base/machines/recipes.pl`: доступность машин по планетам и примеры рецептов самих машин.
- `rules.pl`: семь правил, в том числе рекурсивный вывод сырья и отрицание.
- `ontology/factorio.ttl`: OWL-онтология для открытия в Protégé.
- `ontology/build_ontology.py`: пересоздает OWL из фактов Prolog.

Онтология содержит классы, иерархию, несовместимость, свойства с доменами и
диапазонами, числовые типы и ограничения кардинальности. Факты синхронизированы
генератором; правила Prolog не переводятся автоматически в OWL-вывод.
Проверка HermiT/ELK выполняется отдельно в Protégé.

`available_on/2` означает локальную доступность без межпланетной перевозки:
литейную можно изготовить на Вулканусе, а транспортировка на другие планеты
остается вне модели.

## Проверка

```sh
python3 src/lab1/ontology/build_ontology.py
swipl -q -s tests/test_lab1.pl -g 'run_tests,halt'
swipl -q -s tests/test_ontology.pl -g 'run_tests,halt'
python3 -m unittest discover -s tests -p 'test_dss.py' -v
```

Приоритет `electricity` минимизирует только электрическую мощность в кВт.
Для топливных печей она равна нулю, но это не оценка расхода топлива.
