"""Build the module 1 R&D report as a Cyrillic-capable A4 PDF."""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "module1_factorio_report.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT_ROOT = Path(
    "/Users/scobca/.cache/codex-runtimes/codex-primary-runtime/dependencies/"
    "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/"
    "Resources/fonts/truetype"
)
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_ROOT / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_ROOT / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuMono", str(FONT_ROOT / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#24608E")
PALE = colors.HexColor("#EAF1F6")
GRAY = colors.HexColor("#56616D")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="BodyRu", fontName="DejaVu", fontSize=9.4, leading=14.3,
    spaceAfter=7, textColor=NAVY,
))
styles.add(ParagraphStyle(
    name="HeadingRu", fontName="DejaVu-Bold", fontSize=16, leading=21,
    spaceBefore=4, spaceAfter=12, textColor=NAVY,
))
styles.add(ParagraphStyle(
    name="SubRu", fontName="DejaVu-Bold", fontSize=11.2, leading=16,
    spaceBefore=11, spaceAfter=7, textColor=BLUE,
))
styles.add(ParagraphStyle(
    name="SmallRu", parent=styles["BodyRu"], fontSize=8.2, leading=12,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="CodeRu", fontName="DejaVuMono", fontSize=7.3, leading=11,
    spaceAfter=0, textColor=NAVY,
))
styles.add(ParagraphStyle(
    name="TitleRu", fontName="DejaVu-Bold", fontSize=24, leading=32,
    alignment=TA_CENTER, textColor=NAVY,
))
styles.add(ParagraphStyle(
    name="CenterRu", fontName="DejaVu", fontSize=11, leading=17,
    alignment=TA_CENTER, textColor=NAVY,
))

story = []


def p(text, style="BodyRu"):
    story.append(Paragraph(text, styles[style]))


def h(text):
    story.append(Paragraph(text, styles["HeadingRu"]))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))


def sub(text):
    p(text, "SubRu")


def bullets(items):
    for item in items:
        p("• " + item)


def table(headers, rows, widths=None):
    data = [[Paragraph(escape(x), styles["SmallRu"]) for x in headers]]
    for row in rows:
        data.append([Paragraph(escape(str(x)), styles["SmallRu"]) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, BLUE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#C8D4DD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 9))


def code(lines):
    data = [[Paragraph(escape(line).replace(" ", "&nbsp;"),
                       styles["CodeRu"])] for line in lines]
    t = Table(data, colWidths=[170 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7F8")),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5DD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


def page():
    story.append(PageBreak())


# 1. Title
story.append(Spacer(1, 38 * mm))
p("УНИВЕРСИТЕТ ИТМО", "CenterRu")
story.append(Spacer(1, 12 * mm))
p("Системы искусственного интеллекта", "CenterRu")
story.append(Spacer(1, 22 * mm))
p("ОТЧЕТ ПО МОДУЛЮ 1", "TitleRu")
story.append(Spacer(1, 5 * mm))
p("Базы знаний и онтологии", "CenterRu")
story.append(Spacer(1, 14 * mm))
p("Лабораторная работа 1: Prolog и OWL<br/>"
  "Лабораторная работа 2: система поддержки принятия решений", "CenterRu")
story.append(Spacer(1, 30 * mm))
p("Предметная область: производственные цепочки игры Factorio", "CenterRu")
story.append(Spacer(1, 38 * mm))
p("Санкт-Петербург · 2026", "CenterRu")
page()

# 2–3. Abstract and introduction
h("2. Аннотация")
p("В модуле разработана учебная база знаний о производственных цепочках Factorio "
  "на языке Prolog. Она описывает сырье, промежуточные продукты, рецепты, машины "
  "и доступность машин на двух планетах. На основе фактов построена OWL-онтология "
  "в формате Turtle, открываемая в Protégé. Для лабораторной работы 2 создана "
  "командная система поддержки принятия решений, которая после короткого диалога "
  "выбирает машину для заданного продукта. Рекомендация формируется запросом к "
  "Prolog и сопровождается объяснением критерия выбора. Корректность основных "
  "запросов, структурной модели OWL и сценариев DSS подтверждена автоматическими "
  "тестами; запуск внешнего OWL reasoner требует Protégé.")

h("3. Введение")
p("Цель модуля — освоить логическое моделирование, построение онтологий, "
  "проверяемый вывод и применение знаний в рекомендательной системе. В "
  "производственном планировании игры вопрос «чем изготовить продукт?» зависит "
  "сразу от рецепта, класса машины, планеты, энергии и выбранного критерия. "
  "Явные факты и правила позволяют повторно использовать эти знания, "
  "проследить основание ответа и проверить результат отдельными запросами.")
p("Граница модели намеренно узкая: 10 продуктов, 7 машин и две планеты. "
  "Модель служит демонстрацией метода; она не претендует на полный справочник "
  "всех рецептов и обновлений игры. Доступность означает местное получение "
  "машины без межпланетной перевозки. Все результаты ниже получены из файлов "
  "проекта в версии на дату отчета.")
sub("Артефакты")
table(["Артефакт", "Роль"], [
    ("src/lab1/factorio.pl и base/*.pl", "Факты, рецепты и точка загрузки Prolog"),
    ("src/lab1/rules.pl", "Логический вывод"),
    ("src/lab1/ontology/factorio.ttl", "OWL-онтология для Protégé"),
    ("src/lab2/dss.py", "Диалог и ранжирование рекомендаций"),
    ("tests/", "Проверка Prolog, OWL-структуры и DSS"),
], [69 * mm, 101 * mm])
page()

# 4. Knowledge base
h("4. База знаний в Prolog: дизайн и реализация")
sub("4.1. Словарь и структура")
p("Одноместные факты обозначают 22 вида сырья, 10 промежуточных продуктов и "
  "7 машин — всего 39 объектов. Двухместные отношения machine_type/2, "
  "power_source/2, machine_speed/2, machine_power/2, available_on/2 и "
  "recipe_type/2 связывают объекты со свойствами; одних только "
  "machine_type/2 и power_source/2 имеется 14 фактов. Трехместные "
  "ingredient/3 задают 14 пар «продукт — материал — количество».")
table(["Предикат", "Смысл", "Пример"], [
    ("resource/1", "Сырьевой ресурс", "resource(iron_ore)"),
    ("intermediate_product/1", "Изготавливаемый продукт", "intermediate_product(steel_plate)"),
    ("machine_type/2", "Категория устройства", "machine_type(steel_furnace,furnace)"),
    ("ingredient/3", "Материал и количество", "ingredient(steel_plate,iron_plate,5)"),
    ("recipe_type/2", "Категория для рецепта", "recipe_type(iron_plate,furnace)"),
    ("available_on/2", "Планета работы", "available_on(foundry,vulcanus)"),
], [43 * mm, 61 * mm, 66 * mm])
p("Исходный проект содержал неполную загрузку файлов, разнобой между "
  "craft_from и crafted_from, неверные аргументы и ссылки на отсутствующие "
  "продукты. Факты сведены к одному словарю; составной рецепт электронной "
  "схемы теперь проходит через медный кабель. Каждый представленный продукт "
  "имеет выход, ингредиенты и тип машины.")
sub("4.2. Правила")
p("Семь правил выводят твердые ресурсы, доступность производства, фильтр "
  "энергии, транзитивное сырье, использование жидкости, альтернативы машин "
  "и сравнение скорости. Правило solid_resource/1 использует отрицание "
  "fluid_resource/1. raw_material/2 имеет базовый и "
  "рекурсивный случаи, поэтому электронная схема приводит к iron_ore и "
  "copper_ore через промежуточные продукты.")
code([
    "can_craft(M,P,L) :- machine_type(M,T),",
    "    recipe_type(P,T), available_on(M,L).",
    "raw_material(P,R) :- ingredient(P,R,_), resource(R).",
    "raw_material(P,R) :- ingredient(P,C,_),",
    "    intermediate_product(C), raw_material(C,R).",
])
page()

h("4. База знаний в Prolog: запросы")
p("Ниже приведены ответы SWI-Prolog 10.0.2. Запросы охватывают прямые факты, "
  "переменные, конъюнкцию, дизъюнкцию, отрицание и срабатывание правил.")
table(["№ / запрос", "Фактический ответ"], [
    ("1. resource(iron_ore).", "true"),
    ("2. machine_type(steel_furnace,T).", "T = furnace"),
    ("3. findall(M,can_craft(M,iron_plate,nauvis),Ms).",
     "Ms = [stone_furnace,steel_furnace,electric_furnace]"),
    ("4. solid_resource(water).", "false"),
    ("5. powered_crafter(electric_furnace,iron_plate,nauvis,electricity).", "true"),
    ("6. setof(R,raw_material(electronic_circuit,R),Rs).",
     "Rs = [copper_ore,iron_ore]"),
    ("7. uses_fluid(sulfur).", "true"),
    ("8. faster_than(steel_furnace,stone_furnace).", "true"),
    ("9. can_craft(foundry,molten_iron,nauvis).", "false"),
    ("10. can_craft(foundry,molten_iron,vulcanus); "
     "can_craft(chemical_plant,molten_iron,vulcanus).", "true"),
], [104 * mm, 66 * mm])
p("Запрос 3 объединяет тип рецепта и доступность на Наувисе; запрос 5 "
  "добавляет источник энергии; запрос 6 делает многошаговый вывод по цепочке "
  "ингредиентов. Отрицательный ответ 9 следует из отсутствия факта "
  "available_on(foundry,nauvis). В Prolog применяется допущение о замкнутом "
  "мире: непредставленный факт считается недоказанным.")
page()

# 5. Ontology
h("5. Онтология в Protégé: моделирование")
p("Онтология создается скриптом build_ontology.py непосредственно из тех же "
  "фактов Prolog. Выход — Turtle-файл factorio.ttl с пространством имен "
  "https://example.org/factorio#. Его можно открыть в Protégé командой "
  "File → Open. В нем представлены 10 рецептов, 14 объектов IngredientUse, "
  "ресурсы, продукты, машины, планеты и источники энергии.")
sub("5.1. Классы и ограничения")
bullets([
    "Иерархия Material → IntermediateProduct → MetalPlate имеет три уровня; "
    "ProductionEntity → Machine → Furnace/Assembler/ChemicalPlant/Foundry "
    "задает иерархию оборудования.",
    "RawResource и IntermediateProduct несовместимы; SolidResource и "
    "FluidResource несовместимы. Для отдельных типов машин заданы "
    "owl:disjointWith.",
    "Machine ограничен ровно одним poweredBy из класса PowerSource; Recipe "
    "ограничен ровно одним produces из класса IntermediateProduct; "
    "IngredientUse — ровно одним material.",
    "quantity и yield имеют тип xsd:positiveInteger, powerKW — "
    "xsd:nonNegativeInteger, speed — xsd:decimal.",
])
sub("5.2. Перевод Prolog → OWL")
table(["Prolog", "OWL", "Пояснение"], [
    ("machine(stone_furnace)", "stone_furnace a Furnace", "Тип индивида"),
    ("machine_type(M,furnace)", "Furnace ⊑ Machine", "Категория как класс"),
    ("available_on(M,nauvis)", "M availableOn nauvis", "ObjectProperty"),
    ("power_source(M,fuel)", "M poweredBy fuel", "ObjectProperty"),
    ("machine_speed(M,2.0)", "M speed 2.0^^xsd:decimal", "DataProperty"),
    ("ingredient(P,R,Q)", "Recipe → IngredientUse → R; quantity Q",
     "Трехместное отношение как отдельный объект"),
], [55 * mm, 72 * mm, 43 * mm])
p("Генератор проверяет, что каждый ингредиент ссылается на известный ресурс "
  "или продукт, а все машины имеют тип, источник энергии, скорость и "
  "мощность. Правила can_craft/3 и raw_material/2 не переводятся в OWL "
  "автоматически: OWL хранит исходные связи, а вывод Prolog выполняется "
  "в DSS.")
sub("Источники предметных данных")
p("Рецепты и характеристики сверены по Factorio Wiki: "
  "<link href='https://wiki.factorio.com/Electronic_circuit'>Electronic circuit</link>, "
  "<link href='https://wiki.factorio.com/Steel_furnace'>Steel furnace</link>, "
  "<link href='https://wiki.factorio.com/Assembling_machine_1'>Assembling machine 1</link>, "
  "<link href='https://wiki.factorio.com/Foundry'>Foundry</link>. "
  "Критерии задания и форма отчета взяты из двух предоставленных PDF.")
page()

h("5. Онтология: запросы и проверки")
sub("5.3. Компетентностные DL-запросы")
p("Следующие запросы предназначены для вкладки DL Query после запуска "
  "HermiT в Protégé. Указаны ожидаемые ответы по материализованным фактам "
  "онтологии; фактический запуск HermiT/ELK в этой среде не выполнялся.")
table(["DL Query", "Ожидаемые индивиды"], [
    ("MetalPlate", "iron_plate, copper_plate, steel_plate"),
    ("Furnace and availableOn value nauvis",
     "stone_furnace, steel_furnace, electric_furnace"),
    ("Machine and poweredBy value fuel", "stone_furnace, steel_furnace"),
    ("Recipe and produces value molten_iron", "molten_iron_recipe"),
    ("IngredientUse and material value copper_cable", "ingredient_use_8"),
    ("Machine and supportsRecipe value sulfur_recipe", "chemical_plant"),
], [91 * mm, 79 * mm])
sub("5.4. Подтвержденные структурные проверки")
p("SWI-Prolog загрузил Turtle как RDF и проверил связь рецепта с продуктом, "
  "локальную доступность литейной только на Вулканусе, цепочку подклассов "
  "MetalPlate → IntermediateProduct → Material → ProductionEntity, "
  "ингредиенты электронной схемы, ограничение кардинальности poweredBy "
  "и отсутствие индивидов, явно отнесенных одновременно к несовместимым "
  "классам. Эти тесты проверяют структуру и некоторые логические "
  "предпосылки, но не заменяют полную проверку консистентности OWL reasoner.")
page()

# 6. DSS
h("6. DSS: архитектура и реализация")
p("Программа src/lab2/dss.py принимает одну строку фиксированного вида:")
code([
    "product: iron_plate; planet: nauvis;",
    "priority: speed; energy: electricity",
])
p("Поля product, planet и priority обязательны; отсутствующие значения "
  "система спрашивает отдельно. Поле energy необязательно и по умолчанию "
  "равно any. Ввод и ответы DSS — на английском. Значения продукта и планеты "
  "совпадают с атомами Prolog и проверяются по закрытому словарю; "
  "произвольный текст в запрос не подставляется. Неизвестное поле, "
  "значение или повтор поля вызывает понятную ошибку.")
sub("6.1. Конвейер")
table(["Шаг", "Реализация"], [
    ("1. Разбор", "Разделение по «;» и «:», проверка фиксированных слотов"),
    ("2. Уточнение", "Диалог о недостающем продукте, планете и приоритете"),
    ("3. Логический запрос", "can_craft(M,P,L), power_source(M,E), "
     "machine_speed(M,S), machine_power(M,W)"),
    ("4. Ранжирование", "Скорость: больше S, затем меньше W; "
     "электроэнергия: меньше W, затем больше S"),
    ("5. Ответ", "Имя машины, объяснение по фактам и альтернативы"),
], [42 * mm, 128 * mm])
sub("6.2. Формирование Prolog-запроса")
code([
    "findall(_{machine:M,speed:S,power_kw:W,power_source:E},",
    "  (can_craft(M,iron_plate,nauvis),",
    "   power_source(M,electricity),",
    "   machine_speed(M,S), machine_power(M,W),",
    "   power_source(M,E)), R).",
])
p("Запрос выполняется отдельным процессом SWI-Prolog, результат передается "
  "как JSON. Приоритет применяется к списку кандидатов после логической "
  "фильтрации. Нулевое значение powerKW у топливных машин означает "
  "отсутствие электрического потребления, а не нулевые общие затраты.")
page()

h("6. DSS: сценарии и обработка исключений")
p("Ниже показаны запуски CLI с заданной строкой; запрос во всех случаях "
  "основан на can_craft/3, при ограничении энергии дополнительно на "
  "power_source/2. В таблице указаны решающие условия и фактический ответ.")
table(["Вход: продукт / планета / приоритет / энергия", "Результат и основание"], [
    ("iron_plate / nauvis / speed / electricity",
     "Электрическая печь: furnace, Наувис, electricity, скорость 2.0."),
    ("iron_plate / nauvis / speed / fuel",
     "Стальная печь: скорость 2.0 против 1.0 у каменной."),
    ("iron_gear_wheel / nauvis / electricity / electricity",
     "Сборочный автомат 1: 75 кВт против 150 кВт."),
    ("molten_iron / vulcanus / speed / any",
     "Литейная: найден единственный совместимый тип, скорость 4.0."),
    ("electronic_circuit / nauvis / speed / any",
     "Сборочный автомат 2: скорость 0.75 против 0.5."),
    ("molten_iron / nauvis / speed / any",
     "Нет подходящей машины; предложено изменить условия или планету."),
], [88 * mm, 82 * mm])
sub("Нештатные случаи")
bullets([
    "Неизвестный продукт («product: unknown») отвергается с перечнем "
    "допустимых вариантов.",
    "Повтор «planet: nauvis; planet: vulcanus» распознается как конфликт "
    "ввода, даже если значения одинаковы.",
    "Пустой результат не подменяется случайной рекомендацией.",
    "Если введен только продукт, система задает два вопроса о планете и "
    "приоритете; завершение ввода до ответа дает ошибку.",
])
page()

# 7–9. Tests, evaluation, conclusion
h("7. Тестирование и отладка")
table(["Набор", "Объем", "Подтверждено"], [
    ("Prolog / tests/test_lab1.pl", "13 тестов",
     "Факты, переменные, и/или/не, рекурсия, планеты, целостность рецептов"),
    ("OWL / tests/test_ontology.pl", "6 тестов",
     "RDF-загрузка, связи, иерархия, ограничения, явная несовместимость"),
    ("DSS / tests/test_dss.py", "9 тестов",
     "5 положительных сценариев, пустой результат, неверные/повторные "
     "значения, диалог"),
], [54 * mm, 23 * mm, 93 * mm])
p("Все 28 автоматических тестов завершились успешно. Онтология была "
  "пересоздана после исправления рецепта электронной схемы. Отдельно "
  "проверен запуск CLI для шести сценариев таблицы: ответы совпали с "
  "ожидаемым ранжированием и содержат объяснение. Внешний reasoner "
  "Protégé не запускался; заключение о полной OWL-консистентности "
  "поэтому не делается.")
sub("Команды воспроизведения")
code([
    "python3 src/lab1/ontology/build_ontology.py",
    "swipl -q -s tests/test_lab1.pl -g 'run_tests,halt'",
    "swipl -q -s tests/test_ontology.pl -g 'run_tests,halt'",
    "python3 -m unittest discover -s tests -p test_dss.py",
])

h("8. Оценка и интерпретация")
p("В Prolog удобно записывать правила со связками и, или и не, а также "
  "рекурсивные зависимости материалов. OWL лучше фиксирует словарь "
  "классов, области свойств, диапазоны и ограничения кратности; "
  "онтологию можно расширять и изучать в Protégé. Для DSS выбран Prolog, "
  "поскольку выбор машины зависит от правил и численного ранжирования. "
  "Трассируемость поддерживает генератор: одинаковые имена продуктов, "
  "машин и ресурсов переходят из фактов в индивиды OWL.")
p("Дальнейшее развитие: дополнить рецепты, разделить электрические и "
  "топливные затраты в единой метрике, добавить реальные параметры "
  "производительности и выполнять проверку HermiT в CI или Protégé. "
  "При расширении словаря важно оставлять проверки ссылочной целостности.")
h("9. Заключение")
p("Работают загрузка и запросы к базе знаний, генерация онтологии и "
  "диалоговая рекомендация по продукту, планете, энергии и приоритету. "
  "Ограничения результата — учебное подмножество Factorio и отсутствие "
  "проведенной проверки внешним OWL reasoner. Подход показывает, как "
  "прозрачные правила и явные ограничения помогают получать "
  "проверяемые объяснения и повторно использовать знания между "
  "логической базой, онтологией и приложением.")


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#C7D1DA"))
    canvas.line(20 * mm, 18 * mm, width - 20 * mm, 18 * mm)
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(20 * mm, 12 * mm, "Модуль 1 · Factorio")
    canvas.drawRightString(width - 20 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
    topMargin=21 * mm, bottomMargin=25 * mm,
    title="Отчет по модулю 1 — Factorio",
    author="Проект ITMO AI Systems",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
