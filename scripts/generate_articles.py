#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разовый генератор контент-банка сайта ПодарокГид.
Наполняет content/published/ (стартовые статьи) и content/queue/
(статьи, которые GitHub Actions будет публиковать по одной в неделю).
Запускать вручную при необходимости пополнить банк статей:
    python3 scripts/generate_articles.py
"""
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_DIR = os.path.join(ROOT, "content", "published")
QUEUE_DIR = os.path.join(ROOT, "content", "queue")

def oz(q):
    return "ozon://" + urllib.parse.quote(f"https://www.ozon.ru/search/?text={q}", safe="")

def wb(q):
    return "wb://" + urllib.parse.quote(f"https://www.wildberries.ru/catalog/0/search.aspx?search={q}", safe="")

# Банк идей: ключ -> (название, поисковый запрос, короткий комментарий-подсказка)
IDEAS = {
    "wireless_headphones": ("Беспроводные наушники", "беспроводные наушники",
        "универсальный подарок почти для любого человека — обратите внимание на время работы от батареи и наличие шумоподавления."),
    "thermo_mug": ("Термокружка с подогревом или обычная вакуумная термокружка", "термокружка",
        "приятная мелочь на каждый день, особенно для тех, кто много работает за компьютером или часто в дороге."),
    "power_bank": ("Внешний аккумулятор (power bank) большой ёмкости", "внешний аккумулятор powerbank",
        "практичный подарок для тех, кто много путешествует или работает вне дома."),
    "smart_watch": ("Смарт-часы или фитнес-браслет", "смарт часы фитнес браслет",
        "подойдёт тем, кто следит за активностью и здоровьем — выбирайте по совместимости с телефоном получателя."),
    "blanket": ("Плед с рукавами или мягкий плюшевый плед", "плед с рукавами",
        "уютный подарок на холодное время года, который почти никогда не залёживается без дела."),
    "aroma_diffuser": ("Аромадиффузор с эфирными маслами", "аромадиффузор увлажнитель воздуха",
        "создаёт атмосферу дома и хорошо смотрится как элемент декора."),
    "board_game": ("Настольная игра для компании", "настольная игра для компании",
        "отличный повод собраться с друзьями или семьёй — выбирайте по числу игроков и возрасту."),
    "cosmetics_set": ("Подарочный набор косметики или уходовых средств", "подарочный набор косметики",
        "беспроигрышный вариант, если вы примерно знаете предпочтения по типу кожи и ароматам."),
    "book": ("Книга по интересам получателя (бестселлер или коллекционное издание)", "подарочное издание книги",
        "персональный и не банальный вариант, если вы знаете вкусы человека в литературе."),
    "backpack": ("Стильный рюкзак или сумка для ноутбука", "рюкзак для ноутбука",
        "практичная вещь на каждый день для учёбы, офиса или путешествий."),
    "candle_set": ("Набор ароматических свечей", "набор ароматических свечей подарочный",
        "недорогой, но душевный вариант, подходит почти любому получателю."),
    "kitchen_gadget": ("Полезный кухонный гаджет (например, электрогриль, вафельница, мультипечь)", "кухонный гаджет подарок",
        "хороший выбор для тех, кто любит готовить и экспериментировать на кухне."),
    "portable_speaker": ("Портативная колонка", "портативная колонка блютуз",
        "универсальный подарок для меломанов и любителей активного отдыха."),
    "leather_wallet": ("Кожаное портмоне или картхолдер", "кожаное портмоне мужское",
        "классика, которая редко разочаровывает — обратите внимание на количество отделений."),
    "scarf_gloves": ("Тёплый шарф, шапка или перчатки", "шарф шапка комплект подарок",
        "практичный сезонный подарок, особенно приятен в фирменной подарочной упаковке."),
    "photo_frame_digital": ("Цифровая фоторамка", "цифровая фоторамка wifi",
        "трогательный подарок для родителей и бабушек с дедушками — можно загрузить семейные фото."),
    "cooking_master": ("Мастер-класс или сертификат на кулинарный курс", "сертификат мастер класс кулинария",
        "подарок-впечатление для тех, кому не нужны новые вещи."),
    "puzzle_3d": ("3D-пазл или конструктор для взрослых", "3d пазл конструктор для взрослых",
        "увлекательное занятие для вечера, подходит и как совместный подарок паре."),
    "yoga_mat": ("Коврик для йоги и аксессуары для домашних тренировок", "коврик для йоги набор",
        "хороший выбор для тех, кто следит за спортивной формой."),
    "perfume": ("Парфюм или парфюмерный набор из миниатюр", "парфюмерный набор миниатюры",
        "если не уверены в конкретном аромате — наборы миниатюр позволяют попробовать несколько."),
    "kids_constructor": ("Крупный конструктор по возрасту ребёнка", "конструктор для детей",
        "развивает мелкую моторику и логику — уточните рекомендованный возраст на упаковке."),
    "kids_creativity_set": ("Набор для творчества (рисование, лепка, рукоделие)", "набор для детского творчества",
        "занимает ребёнка надолго и подходит для разных возрастов — от 3 лет и старше."),
    "kids_scooter": ("Самокат или беговел", "детский самокат",
        "отличный подарок для активных прогулок — выбирайте по росту и возрасту ребёнка."),
    "board_game_kids": ("Детская настольная или обучающая игра", "детская обучающая настольная игра",
        "совмещает игру и обучение, подходит для семейных вечеров."),
    "night_light": ("Ночник в форме зверушки или проектор звёздного неба", "ночник проектор для детей",
        "уютная деталь для детской комнаты, которая нравится почти всем малышам."),
    "planner": ("Красивый ежедневник или планер", "ежедневник планер недатированный",
        "практичный подарок для тех, кто любит планировать дела и вести заметки от руки."),
    "office_organizer": ("Органайзер для рабочего стола", "органайзер для рабочего стола",
        "небольшая, но полезная вещь, которая наводит порядок на столе."),
    "tea_coffee_set": ("Подарочный набор чая или кофе", "подарочный набор чай кофе",
        "универсальный вариант почти для любого праздника и бюджета."),
    "phone_case": ("Чехол для телефона или защитное стекло", "чехол для телефона",
        "недорогая, но практичная мелочь — уточните модель телефона получателя."),
    "board_puzzle": ("Пазл с красивым изображением (1000+ деталей)", "пазл 1000 деталей",
        "спокойное занятие для вечеров, можно собирать всей семьёй."),
    "sports_bottle": ("Спортивная бутылка для воды", "спортивная бутылка для воды",
        "простой и полезный подарок для тех, кто ведёт активный образ жизни."),
    "wallet_card_holder": ("Картхолдер или обложка на документы", "обложка для документов подарочная",
        "компактный и практичный подарок на любой бюджет."),
    "grill_bbq": ("Портативный гриль или аксессуары для барбекю", "портативный гриль для дачи",
        "хороший вариант для дачников и любителей отдыха на природе."),
    "tool_set": ("Набор инструментов для дома", "набор инструментов подарочный",
        "практичный подарок для тех, кто любит мастерить своими руками."),
    "car_accessories": ("Автомобильный аксессуар (держатель, ароматизатор, органайзер в салон)", "автомобильные аксессуары подарок",
        "хороший выбор, если знаете, что человек часто за рулём."),
    "houseplant_kit": ("Набор для выращивания растения или готовое растение в горшке", "набор для выращивания растения",
        "живой подарок, который украшает дом и требует небольшой заботы."),
    "massager": ("Массажёр для шеи, спины или ног", "массажер портативный",
        "приятный подарок для расслабления после рабочего дня."),
    "led_lamp": ("Стильный светильник или LED-лампа с управлением по Bluetooth", "led лампа настроения",
        "интересный элемент декора, который меняет атмосферу комнаты."),
    "gift_certificate": ("Подарочный сертификат в любимый магазин или сервис", "подарочный сертификат",
        "универсальный вариант, если сложно угадать со вкусом."),
    "photo_book": ("Фотокнига с совместными воспоминаниями", "фотокнига на заказ",
        "один из самых тёплых подарков — особенно для родителей, бабушек и дедушек."),
    "backpack_school": ("Школьный рюкзак с ортопедической спинкой", "школьный рюкзак ортопедический",
        "актуально к 1 сентября и выпускному — выбирайте по возрасту ученика."),
    "watch_classic": ("Классические наручные часы", "наручные часы подарочные",
        "статусный подарок, который редко выходит из моды."),
    "makeup_mirror": ("Зеркало с подсветкой для макияжа", "зеркало с подсветкой косметическое",
        "практичный и приятный подарок для повседневной красоты."),
    "cocktail_set": ("Набор для приготовления коктейлей", "набор бармена для коктейлей",
        "весёлый подарок для тех, кто любит принимать гостей."),
    "fondue_set": ("Набор для фондю или раклета", "набор для фондю",
        "интересный формат для семейных вечеров и посиделок с друзьями."),
    "camera_instant": ("Фотоаппарат мгновенной печати", "фотоаппарат моментальной печати",
        "популярный подарок для подростков и молодёжи — фото сразу можно подержать в руках."),
    "gaming_accessory": ("Игровой аксессуар (коврик для мыши, наушники, контроллер)", "игровые аксессуары подарок",
        "беспроигрышный вариант для геймеров любого возраста."),
    "scented_bath_set": ("Набор для ванны (соли, бомбочки, масла)", "подарочный набор для ванны",
        "приятный вариант, чтобы порадовать близкого человека маленьким SPA дома."),
    "wall_art": ("Постер или картина в стильной раме", "постер в раме для интерьера",
        "хороший способ обновить интерьер и сделать подарок персональным по сюжету."),
    "handbag_woman": ("Стильная женская сумка через плечо", "женская сумка через плечо",
        "практичный и приятный подарок — если не уверены в цвете, берите чёрный или бежевый."),
    "belt_cufflinks": ("Кожаный ремень или запонки", "кожаный ремень мужской подарочный",
        "классический аксессуар, который легко подобрать даже без примерки."),
    "kids_book_set": ("Набор детских книг с иллюстрациями", "детские книги набор подарочный",
        "хороший подарок для малышей — развивает речь и любовь к чтению с раннего возраста."),
    "business_pen_set": ("Подарочный набор: ручка и визитница", "подарочный набор ручка визитница",
        "сдержанный деловой подарок, уместный даже для формальных отношений."),
    "flower_box": ("Стабилизированные цветы в коробке (стоят до года)", "стабилизированные цветы в коробке",
        "красивая альтернатива обычному букету — не завянет через несколько дней."),
    "newborn_set": ("Подарочный набор для новорождённого (боди, полотенце, конверт)", "набор для новорожденного подарочный",
        "практичный набор, который точно пригодится в первые месяцы жизни малыша."),
    "maternity_set": ("Уходовый набор для будущей мамы (крем от растяжек, косметика)", "набор для беременных уходовый",
        "заботливый подарок, который помогает будущей маме чувствовать себя комфортнее."),
    "wine_glasses_set": ("Набор бокалов для вина или графин", "набор бокалов для вина подарочный",
        "красивый и универсальный подарок для тех, кто любит принимать гостей."),
}


def item_md(key):
    name, q, note = IDEAS[key]
    return (f"### {name}\n\n"
            f"{note}\n\n"
            f'<a class="cta-link" href="{oz(q)}">Посмотреть на Ozon</a> '
            f'<a class="cta-link" href="{wb(q)}">Посмотреть на Wildberries</a>\n')


def build_article(slug, title, description, category, intro, keys, outro, date=None, source="queue"):
    body_items = "\n".join(item_md(k) for k in keys)
    fm_date = f"date: {date}\n" if date else ""
    content = (
        "---\n"
        f'title: "{title}"\n'
        f"slug: {slug}\n"
        f'description: "{description}"\n'
        f"category: {category}\n"
        f"{fm_date}"
        "---\n\n"
        f"{intro}\n\n"
        f"{body_items}\n"
        f"{outro}\n"
    )
    out_dir = PUB_DIR if source == "published" else QUEUE_DIR
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"{slug}.md"), "w", encoding="utf-8") as f:
        f.write(content)


OUTRO_DEFAULT = (
    "\n## Как выбрать точнее\n\n"
    "Если сомневаетесь между несколькими вариантами — ориентируйтесь на образ жизни "
    "человека (домосед, путешественник, спортсмен, творческая профессия) и на то, "
    "чем он увлекается в свободное время. Практичные подарки редко разочаровывают, "
    "а вот с юмористическими и очень личными лучше быть осторожнее, если не уверены "
    "в чувстве юмора получателя.\n"
)

ARTICLES = [
    # ---------- PUBLISHED (8) ----------
    dict(slug="podarki-muzhchine-na-den-rozhdeniya", source="published", date="2026-08-24",
         title="20 идей подарков мужчине на день рождения до 5000 рублей",
         description="Подборка практичных и интересных идей подарков мужчине на день рождения в пределах 5000 рублей.",
         category="Мужчине",
         intro="Выбрать подарок мужчине бывает непросто — вкусы у всех разные. Мы собрали подборку идей, "
               "которые подходят для большинства мужчин: от практичных гаджетов до подарков для отдыха и хобби.",
         keys=["wireless_headphones","power_bank","smart_watch","portable_speaker","leather_wallet",
               "thermo_mug","backpack","tool_set","car_accessories","grill_bbq","gaming_accessory",
               "watch_classic","board_game","massager","perfume","cocktail_set"]),

    dict(slug="podarki-zhenshchine-na-den-rozhdeniya", source="published", date="2026-08-24",
         title="20 идей подарков женщине на день рождения до 5000 рублей",
         description="Подборка подарков женщине на день рождения: от косметики и украшений до подарков-впечатлений.",
         category="Женщине",
         intro="Собрали универсальные идеи подарков для женщины на день рождения — подойдут, если вы точно "
               "не знаете размер одежды или конкретный бренд косметики, но хотите подарить что-то приятное.",
         keys=["cosmetics_set","blanket","aroma_diffuser","makeup_mirror","perfume","photo_book",
               "candle_set","scented_bath_set","tea_coffee_set","thermo_mug","wall_art",
               "smart_watch","book","gift_certificate","yoga_mat","wireless_headphones"]),

    dict(slug="chto-podarit-rebenku-na-novyj-god", source="published", date="2026-08-24",
         title="Что подарить ребёнку на Новый год: 18 идей по возрастам",
         description="Идеи новогодних подарков для детей разного возраста — от малышей до школьников.",
         category="Ребёнку",
         intro="Новогодние подарки для детей — это всегда особое волшебство. Подобрали идеи, которые "
               "подойдут для разных возрастов: уточните возрастную маркировку на упаковке при выборе.",
         keys=["kids_constructor","kids_creativity_set","kids_scooter","board_game_kids","night_light",
               "puzzle_3d","camera_instant","backpack_school","book","board_game",
               "photo_frame_digital","gaming_accessory","houseplant_kit","led_lamp"]),

    dict(slug="podarki-kollege", source="published", date="2026-08-25",
         title="Подарки коллеге: 15 универсалььных идей, которые точно понравятся",
         description="Нейтральные и универсальные идеи подарков коллеге по работе на любой праздник.",
         category="Коллеге",
         intro="Подарок коллеге должен быть приятным, но не слишком личным. Собрали нейтральные варианты, "
               "которые подойдут почти любому человеку в офисе.",
         keys=["thermo_mug","planner","office_organizer","tea_coffee_set","candle_set",
               "phone_case","gift_certificate","sports_bottle","wallet_card_holder","board_puzzle",
               "aroma_diffuser","power_bank","led_lamp","book"]),

    dict(slug="chto-podarit-na-23-fevralya", source="published", date="2026-08-25",
         title="Что подарить на 23 февраля: 16 идей для мужчин",
         description="Подборка подарков на 23 февраля: для коллег, друзей, папы, мужа или брата.",
         category="Праздники",
         intro="23 февраля — повод порадовать не только военных, но и всех мужчин вокруг: коллег, друзей,"
               "родственников. Вот идеи на любой бюджет.",
         keys=["thermo_mug","power_bank","tool_set","car_accessories","leather_wallet","grill_bbq",
               "gaming_accessory","portable_speaker","watch_classic","wireless_headphones",
               "sports_bottle","cocktail_set","backpack","massager"]),

    dict(slug="chto-podarit-na-8-marta", source="published", date="2026-08-25",
         title="Что подарить на 8 марта: 16 идей для женщин",
         description="Подборка подарков на 8 марта для мамы, коллег, подруг и любимой девушки.",
         category="Праздники",
         intro="На 8 марта хочется порадовать всех женщин вокруг — маму, коллег, подруг. Собрали идеи "
               "на разный бюджет и уровень близости отношений.",
         keys=["cosmetics_set","candle_set","aroma_diffuser","tea_coffee_set","makeup_mirror",
               "scented_bath_set","photo_book","blanket","wall_art","gift_certificate",
               "perfume","houseplant_kit","book","yoga_mat"]),

    dict(slug="podarki-do-1000-rublej", source="published", date="2026-08-26",
         title="Подарки до 1000 рублей: 20 недорогих, но приятных идей",
         description="Что подарить, если бюджет ограничен 1000 рублями — подборка недорогих, но приятных идей.",
         category="Бюджет",
         intro="Небольшой бюджет — не повод дарить что попало. Собрали идеи до 1000 рублей, которые всё равно "
               "выглядят продуманно и приятно.",
         keys=["candle_set","phone_case","sports_bottle","wallet_card_holder","tea_coffee_set",
               "night_light","board_puzzle","office_organizer","houseplant_kit","planner",
               "kids_creativity_set","car_accessories"]),

    dict(slug="chto-podarit-podrostku", source="published", date="2026-08-26",
         title="Что подарить подростку: 18 актуальных идей на 2026 год",
         description="Идеи подарков подростку на день рождения, Новый год или выпускной из 9 класса.",
         category="Подростку",
         intro="Угодить подростку непросто — вкусы меняются быстро. Собрали идеи, которые остаются "
               "актуальными: от гаджетов до подарков для творчества и хобби.",
         keys=["wireless_headphones","camera_instant","gaming_accessory","power_bank","portable_speaker",
               "backpack","kids_scooter","phone_case","board_game","puzzle_3d",
               "gift_certificate","led_lamp","book","smart_watch"]),

    # ---------- QUEUE (16) ----------
    dict(slug="podarki-mame-na-den-rozhdeniya", source="queue",
         title="Подарки маме на день рождения: 15 идей",
         description="Что подарить маме на день рождения — идеи для любого бюджета и возраста.",
         category="Маме",
         intro="Подарок для мамы хочется выбрать особенно тщательно. Вот идеи, которые подойдут почти "
               "любой маме — от практичных до по-настоящему трогательных.",
         keys=["photo_book","blanket","aroma_diffuser","cosmetics_set","tea_coffee_set","candle_set",
               "houseplant_kit","makeup_mirror","massager","photo_frame_digital","scented_bath_set","book"]),

    dict(slug="podarki-pape", source="queue",
         title="Подарки папе: 15 идей для любого возраста",
         description="Что подарить папе на день рождения или праздник — практичные и душевные идеи.",
         category="Папе",
         intro="Папам часто сложнее всего выбирать подарки — кажется, что у них уже всё есть. Собрали "
               "идеи, которые пригодятся в быту, на даче или для отдыха.",
         keys=["tool_set","grill_bbq","thermo_mug","car_accessories","leather_wallet","massager",
               "portable_speaker","watch_classic","power_bank","photo_book","board_game"]),

    dict(slug="chto-podarit-luchshemu-drugu", source="queue",
         title="Что подарить лучшему другу: 15 идей",
         description="Идеи подарков для лучшего друга или подруги на день рождения.",
         category="Другу",
         intro="Для близкого друга хочется подарить что-то со смыслом, но не слишком серьёзное. Вот "
               "идеи, которые подойдут для тёплой дружеской компании.",
         keys=["board_game","puzzle_3d","portable_speaker","camera_instant","cocktail_set","fondue_set",
               "gaming_accessory","gift_certificate","backpack","thermo_mug","led_lamp"]),

    dict(slug="podarki-na-novyj-god-kollegam", source="queue",
         title="Подарки на Новый год для коллег и корпоратива: 15 идей до 1500 рублей",
         description="Недорогие новогодние подарки коллегам на корпоратив или тайного Санту.",
         category="Праздники",
         intro="Для корпоративного обмена подарками важно уложиться в бюджет и не промахнуться с идеей. "
               "Собрали нейтральные варианты до 1500 рублей.",
         keys=["tea_coffee_set","candle_set","thermo_mug","office_organizer","planner","phone_case",
               "sports_bottle","board_puzzle","night_light","car_accessories","houseplant_kit"]),

    dict(slug="chto-podarit-devushke-na-den-vlyublennykh", source="queue",
         title="Что подарить девушке на День влюблённых: 15 романтичных идей",
         description="Романтичные подарки девушке на 14 февраля на любой бюджет.",
         category="Праздники",
         intro="День влюблённых — повод сделать что-то приятное и немного романтичное. Вот идеи, "
               "которые подойдут для разных этапов отношений.",
         keys=["perfume","cosmetics_set","photo_book","candle_set","scented_bath_set","wall_art",
               "blanket","makeup_mirror","gift_certificate","aroma_diffuser","book"]),

    dict(slug="chto-podarit-parnyu-na-den-vlyublennykh", source="queue",
         title="Что подарить парню на День влюблённых: 15 идей",
         description="Идеи подарков парню на 14 февраля — от практичных гаджетов до подарков-впечатлений.",
         category="Праздники",
         intro="Подарок парню на 14 февраля необязательно должен быть романтичным в классическом "
               "понимании — часто лучше заходят практичные и интересные вещи.",
         keys=["wireless_headphones","power_bank","portable_speaker","leather_wallet","gaming_accessory",
               "watch_classic","cocktail_set","thermo_mug","backpack","gift_certificate"]),

    dict(slug="podarki-babushke", source="queue",
         title="Подарки бабушке: 15 душевных идей",
         description="Что подарить бабушке на день рождения или праздник — тёплые и практичные идеи.",
         category="Бабушке",
         intro="Для бабушки особенно ценны знаки внимания и заботы. Собрали идеи, которые совмещают "
               "практичность и душевность.",
         keys=["photo_book","photo_frame_digital","blanket","aroma_diffuser","tea_coffee_set",
               "houseplant_kit","massager","candle_set","scented_bath_set"]),

    dict(slug="podarki-dedushke", source="queue",
         title="Подарки дедушке: 15 идей",
         description="Что подарить дедушке на день рождения или 23 февраля — практичные и тёплые идеи.",
         category="Дедушке",
         intro="Дедушкам обычно приятны практичные подарки для дома, дачи или отдыха, а также всё, "
               "что связано с семьёй и воспоминаниями.",
         keys=["photo_book","tool_set","grill_bbq","thermo_mug","massager","board_game",
               "car_accessories","photo_frame_digital","houseplant_kit"]),

    dict(slug="chto-podarit-na-novoselye", source="queue",
         title="Что подарить на новоселье: 18 полезных идей",
         description="Идеи подарков на новоселье — от практичных мелочей до атмосферных вещей для дома.",
         category="Праздники",
         intro="На новоселье принято дарить что-то полезное для нового дома. Собрали идеи, которые "
               "пригодятся почти в любой квартире.",
         keys=["kitchen_gadget","aroma_diffuser","led_lamp","houseplant_kit","tool_set","wall_art",
               "blanket","candle_set","fondue_set","cocktail_set","tea_coffee_set","office_organizer"]),

    dict(slug="podarki-na-svadbu", source="queue",
         title="Подарки на свадьбу: 15 идей, которые не будут пылиться на полке",
         description="Что подарить на свадьбу молодожёнам — практичные и запоминающиеся идеи.",
         category="Праздники",
         intro="Свадебный подарок хочется выбрать так, чтобы он действительно пригодился молодой семье. "
               "Вот идеи, которые обычно оказываются кстати.",
         keys=["kitchen_gadget","cocktail_set","fondue_set","photo_book","blanket","wall_art",
               "houseplant_kit","gift_certificate","led_lamp","tea_coffee_set"]),

    dict(slug="podarki-do-3000-rublej", source="queue",
         title="Подарки до 3000 рублей: 20 идей на все случаи",
         description="Что подарить в пределах 3000 рублей — универсальные идеи для любого получателя.",
         category="Бюджет",
         intro="3000 рублей — комфортный бюджет для подарка, который не выглядит скромно. Собрали "
               "универсальные идеи, которые подойдут почти любому человеку.",
         keys=["thermo_mug","power_bank","cosmetics_set","board_game","backpack","aroma_diffuser",
               "wireless_headphones","perfume","photo_book","kitchen_gadget","sports_bottle","planner"]),

    dict(slug="podarki-do-500-rublej", source="queue",
         title="Подарки до 500 рублей: 18 бюджетных, но приятных вариантов",
         description="Небольшие подарки до 500 рублей, которые всё равно выглядят продуманно.",
         category="Бюджет",
         intro="Даже с бюджетом до 500 рублей можно подобрать приятный подарок, если правильно "
               "расставить приоритеты. Вот подборка недорогих, но удачных идей.",
         keys=["candle_set","phone_case","sports_bottle","wallet_card_holder","night_light",
               "board_puzzle","office_organizer","houseplant_kit"]),

    dict(slug="dorogie-podarki", source="queue",
         title="Дорогие подарки: 15 идей для особого случая",
         description="Идеи дорогих и статусных подарков для юбилея, свадьбы или большого праздника.",
         category="Бюджет",
         intro="Для особого повода — юбилея, годовщины или крупного праздника — хочется подарить что-то "
               "по-настоящему запоминающееся. Вот идеи для более высокого бюджета.",
         keys=["watch_classic","smart_watch","camera_instant","portable_speaker","leather_wallet",
               "grill_bbq","gaming_accessory","photo_book","cocktail_set"]),

    dict(slug="podarki-dlya-doma-i-uyuta", source="queue",
         title="Подарки для дома и уюта: 18 идей",
         description="Идеи подарков для дома — уютные и практичные вещи для интерьера и быта.",
         category="Для дома",
         intro="Подарки для дома почти всегда универсальны и уместны. Собрали идеи, которые сделают "
               "пространство уютнее.",
         keys=["blanket","aroma_diffuser","led_lamp","candle_set","houseplant_kit","wall_art",
               "kitchen_gadget","fondue_set","tea_coffee_set","office_organizer"]),

    dict(slug="gadzhety-v-podarok", source="queue",
         title="Гаджеты в подарок: 18 идей для любителей техники",
         description="Подборка подарков-гаджетов для тех, кто любит технику и новинки.",
         category="Гаджеты",
         intro="Для любителей техники сложно ошибиться с подарком-гаджетом. Собрали актуальные идеи "
               "на разный бюджет.",
         keys=["wireless_headphones","power_bank","smart_watch","portable_speaker","camera_instant",
               "gaming_accessory","photo_frame_digital","led_lamp","phone_case"]),

    dict(slug="podarki-na-vypusknoj", source="queue",
         title="Подарки на выпускной: 15 идей для школьников и студентов",
         description="Что подарить на выпускной — идеи для школьников 9, 11 класса и студентов.",
         category="Праздники",
         intro="Выпускной — важный рубеж, и подарок хочется подобрать со смыслом. Вот идеи для "
               "школьников и студентов на старте новой главы жизни.",
         keys=["backpack_school","backpack","power_bank","planner","wireless_headphones",
               "camera_instant","gift_certificate","watch_classic","book"]),
    # ---------- QUEUE: расширение банка (масштабирование, 01.09.2026) ----------
    dict(slug="podarki-muzhu-na-godovschinu-svadby", source="queue",
         title="Подарки мужу на годовщину свадьбы: 15 идей",
         description="Что подарить мужу на годовщину свадьбы — идеи для любого срока брака и бюджета.",
         category="Мужчине",
         intro="Годовщина свадьбы — хороший повод сделать мужу приятный и немного личный подарок. "
               "Собрали идеи, которые подойдут и для первой годовщины, и для более солидной даты.",
         keys=["watch_classic","leather_wallet","belt_cufflinks","wireless_headphones","photo_book",
               "cocktail_set","portable_speaker","grill_bbq","gift_certificate"]),

    dict(slug="podarki-zhene-na-godovschinu-svadby", source="queue",
         title="Подарки жене на годовщину свадьбы: 15 идей",
         description="Что подарить жене на годовщину свадьбы — романтичные и практичные идеи.",
         category="Женщине",
         intro="На годовщину свадьбы хочется напомнить жене, как много она значит. Вот идеи — от "
               "романтичных мелочей до более серьёзных подарков.",
         keys=["flower_box","perfume","handbag_woman","photo_book","cosmetics_set","wall_art",
               "scented_bath_set","gift_certificate","makeup_mirror"]),

    dict(slug="chto-podarit-na-yubiley-zhenschine-30-let", source="queue",
         title="Что подарить женщине на юбилей 30 лет: 15 идей",
         description="Идеи подарков женщине на юбилей 30 лет — стильные и запоминающиеся варианты.",
         category="Женщине",
         intro="30 лет — красивая дата, которую хочется отметить особенным подарком. Собрали идеи, "
               "которые подойдут для этого юбилея.",
         keys=["handbag_woman","perfume","smart_watch","photo_book","cosmetics_set","flower_box",
               "wall_art","gift_certificate","wine_glasses_set"]),

    dict(slug="chto-podarit-na-yubiley-zhenschine-40-let", source="queue",
         title="Что подарить женщине на юбилей 40 лет: 15 идей",
         description="Идеи подарков женщине на юбилей 40 лет — от статусных вещей до подарков-впечатлений.",
         category="Женщине",
         intro="40-летний юбилей — повод для по-настоящему тёплого и статусного подарка. Вот варианты "
               "на разный бюджет.",
         keys=["watch_classic","perfume","handbag_woman","photo_book","massager","flower_box",
               "gift_certificate","wine_glasses_set","cosmetics_set"]),

    dict(slug="chto-podarit-na-yubiley-muzhchine-40-let", source="queue",
         title="Что подарить мужчине на юбилей 40 лет: 15 идей",
         description="Идеи подарков мужчине на юбилей 40 лет — статусные и практичные варианты.",
         category="Мужчине",
         intro="40 лет — солидная дата для мужчины, и подарок хочется подобрать соответствующий. "
               "Собрали идеи от классики до техники.",
         keys=["watch_classic","leather_wallet","belt_cufflinks","grill_bbq","portable_speaker",
               "smart_watch","cocktail_set","gift_certificate","tool_set"]),

    dict(slug="chto-podarit-na-yubiley-muzhchine-50-let", source="queue",
         title="Что подарить мужчине на юбилей 50 лет: 15 идей",
         description="Идеи подарков мужчине на юбилей 50 лет — солидные и практичные варианты.",
         category="Мужчине",
         intro="Юбилей 50 лет — повод для подарка с характером. Вот идеи, которые подчеркнут статус "
               "и учтут интересы именинника.",
         keys=["watch_classic","leather_wallet","grill_bbq","massager","portable_speaker",
               "photo_book","wine_glasses_set","gift_certificate","tool_set"]),

    dict(slug="podarki-nachalniku", source="queue",
         title="Подарки начальнику: 15 нейтральных и уместных идей",
         description="Что подарить начальнику на день рождения или праздник — сдержанные деловые идеи.",
         category="Коллеге",
         intro="Подарок начальнику требует особого такта — важно остаться в рамках делового этикета. "
               "Собрали нейтральные, но приятные варианты.",
         keys=["business_pen_set","tea_coffee_set","wine_glasses_set","planner","gift_certificate",
               "thermo_mug","wallet_card_holder","belt_cufflinks"]),

    dict(slug="podarki-nachalnitse", source="queue",
         title="Подарки начальнице: 15 идей в деловом стиле",
         description="Что подарить начальнице на 8 марта или день рождения — сдержанные и приятные идеи.",
         category="Коллеге",
         intro="Для начальницы хочется найти подарок одновременно приятный и уместный. Вот идеи, "
               "которые не выходят за рамки делового этикета.",
         keys=["flower_box","business_pen_set","cosmetics_set","tea_coffee_set","gift_certificate",
               "candle_set","makeup_mirror","planner"]),

    dict(slug="podarki-uchitelyu-na-den-uchitelya", source="queue",
         title="Подарки учителю на День учителя: 15 идей",
         description="Что подарить учителю на 5 октября — уместные и не банальные идеи.",
         category="Праздники",
         intro="Учителю хочется подарить что-то не банальное, но при этом уместное. Собрали идеи, "
               "которые подойдут и для класса в складчину, и для личного подарка.",
         keys=["flower_box","business_pen_set","tea_coffee_set","planner","candle_set",
               "gift_certificate","photo_book","wine_glasses_set"]),

    dict(slug="chto-podarit-devochke-na-den-rozhdeniya-5-let", source="queue",
         title="Что подарить девочке на день рождения 5 лет: 15 идей",
         description="Идеи подарков девочке на 5 лет — развивающие игрушки и творческие наборы.",
         category="Ребёнку",
         intro="В 5 лет дети особенно любят яркие игрушки и творчество. Собрали идеи, которые понравятся "
               "именно девочкам этого возраста.",
         keys=["kids_creativity_set","kids_book_set","board_game_kids","night_light","puzzle_3d",
               "kids_constructor","photo_frame_digital"]),

    dict(slug="chto-podarit-malchiku-na-den-rozhdeniya-10-let", source="queue",
         title="Что подарить мальчику на день рождения 10 лет: 15 идей",
         description="Идеи подарков мальчику на 10 лет — гаджеты, конструкторы и активные игры.",
         category="Ребёнку",
         intro="В 10 лет дети уже тянутся к технике и активным играм, но конструкторы и настолки всё "
               "ещё в почёте. Вот подборка идей.",
         keys=["kids_scooter","gaming_accessory","kids_constructor","board_game_kids","camera_instant",
               "puzzle_3d","backpack_school","kids_book_set"]),

    dict(slug="podarki-teshche", source="queue",
         title="Подарки тёще: 15 идей, чтобы точно угодить",
         description="Что подарить тёще на день рождения или праздник — беспроигрышные идеи.",
         category="Женщине",
         intro="Подарок тёще — задача с особой ответственностью. Собрали идеи, которые обычно "
               "воспринимаются тепло и без лишних вопросов.",
         keys=["flower_box","tea_coffee_set","cosmetics_set","photo_book","houseplant_kit",
               "scented_bath_set","candle_set"]),

    dict(slug="podarki-svekrovi", source="queue",
         title="Подарки свекрови: 15 душевных идей",
         description="Что подарить свекрови на день рождения или 8 марта — тёплые и уместные идеи.",
         category="Женщине",
         intro="Для свекрови хочется подобрать подарок, который покажет уважение и внимание. Вот "
               "идеи, которые редко разочаровывают.",
         keys=["flower_box","tea_coffee_set","photo_book","houseplant_kit","aroma_diffuser",
               "candle_set","scented_bath_set"]),

    dict(slug="chto-podarit-na-den-materi", source="queue",
         title="Что подарить на День матери: 15 трогательных идей",
         description="Идеи подарков на День матери — для мамы, бабушки или жены-мамы.",
         category="Праздники",
         intro="День матери — хороший повод сказать спасибо словами и подарком. Собрали идеи, которые "
               "подходят для мам любого возраста.",
         keys=["photo_book","flower_box","blanket","tea_coffee_set","houseplant_kit","massager",
               "scented_bath_set","photo_frame_digital"]),

    dict(slug="podarki-do-2000-rublej", source="queue",
         title="Подарки до 2000 рублей: 18 идей на разные случаи",
         description="Что подарить в пределах 2000 рублей — удачные идеи для любого получателя.",
         category="Бюджет",
         intro="2000 рублей — бюджет, в котором уже есть простор для выбора. Собрали идеи, которые "
               "выглядят продуманно и подойдут почти любому человеку.",
         keys=["thermo_mug","candle_set","phone_case","sports_bottle","tea_coffee_set","planner",
               "board_puzzle","wallet_card_holder","office_organizer","houseplant_kit"]),

    dict(slug="podarki-do-5000-rublej", source="queue",
         title="Подарки до 5000 рублей: 20 идей на все случаи",
         description="Что подарить в пределах 5000 рублей — универсальные идеи для любого получателя.",
         category="Бюджет",
         intro="5000 рублей — комфортный бюджет для по-настоящему приятного подарка. Собрали идеи, "
               "которые подойдут и для дня рождения, и для праздника.",
         keys=["wireless_headphones","smart_watch","cosmetics_set","backpack","perfume","photo_book",
               "portable_speaker","leather_wallet","kitchen_gadget","wine_glasses_set"]),

    dict(slug="podarki-do-10000-rublej", source="queue",
         title="Подарки до 10000 рублей: 15 идей для особого случая",
         description="Что подарить в пределах 10000 рублей — идеи для юбилея, свадьбы или крупного праздника.",
         category="Бюджет",
         intro="10000 рублей — бюджет для по-настоящему запоминающегося подарка. Собрали идеи для "
               "юбилеев, свадеб и других важных поводов.",
         keys=["smart_watch","watch_classic","handbag_woman","portable_speaker","camera_instant",
               "gaming_accessory","leather_wallet","wine_glasses_set"]),

    dict(slug="podarki-na-rozhdenie-rebenka", source="queue",
         title="Подарки на рождение ребёнка: 15 полезных идей",
         description="Что подарить родителям новорождённого — практичные и трогательные идеи.",
         category="Для дома",
         intro="На рождение ребёнка принято дарить что-то практичное для малыша или приятное для "
               "уставших родителей. Вот подборка идей.",
         keys=["newborn_set","photo_book","kids_book_set","blanket","night_light","houseplant_kit",
               "tea_coffee_set"]),

    dict(slug="podarki-beremennoj", source="queue",
         title="Подарки беременной: 15 заботливых идей",
         description="Что подарить будущей маме — уходовые и практичные идеи для беременных.",
         category="Женщине",
         intro="Для будущей мамы хочется подобрать что-то заботливое и полезное. Собрали идеи, "
               "которые пригодятся и до, и после родов.",
         keys=["maternity_set","blanket","aroma_diffuser","photo_book","tea_coffee_set","massager",
               "newborn_set"]),

    dict(slug="podarki-luchshey-podruge", source="queue",
         title="Подарки лучшей подруге: 15 идей", 
         description="Что подарить лучшей подруге на день рождения — тёплые и весёлые идеи.",
         category="Другу",
         intro="Для лучшей подруги хочется найти подарок с настроением — что-то личное, но не слишком "
               "серьёзное. Вот идеи, которые обычно заходят на ура.",
         keys=["cosmetics_set","candle_set","photo_book","handbag_woman","scented_bath_set",
               "wall_art","gift_certificate","perfume"]),

    dict(slug="podarki-synu", source="queue",
         title="Подарки сыну: 15 идей на день рождения", 
         description="Что подарить сыну на день рождения — идеи для разного возраста.",         category="Ребёнку",
         intro="Подарок сыну хочется выбрать так, чтобы он действительно порадовал, а не пылился на "
               "полке. Собрали идеи для разных возрастов и увлечений.",
         keys=["kids_constructor","gaming_accessory","kids_scooter","board_game_kids","backpack_school",
               "puzzle_3d","kids_book_set","camera_instant"]),

    dict(slug="podarki-docheri", source="queue",
         title="Подарки дочери: 15 идей на день рождения",
         description="Что подарить дочери на день рождения — идеи для разного возраста.",
         category="Ребёнку",
         intro="Для дочери хочется подобрать подарок, который совпадёт с её увлечениями. Вот идеи "
               "для разных возрастов — от малышек до подростков.",
         keys=["kids_creativity_set","kids_book_set","night_light","board_game_kids","backpack_school",
               "camera_instant","photo_frame_digital","handbag_woman"]),

    dict(slug="podarki-na-den-rozhdeniya-muzhu", source="queue",
         title="Подарки мужу на день рождения: 15 идей",
         description="Что подарить мужу на день рождения — практичные и приятные идеи.",
         category="Мужчине",
         intro="Для мужа хочется подобрать подарок, который будет по-настоящему в тему — не просто "
               "формальность. Вот идеи на день рождения.",
         keys=["wireless_headphones","leather_wallet","grill_bbq","portable_speaker","watch_classic",
               "gaming_accessory","tool_set","cocktail_set"]),

    dict(slug="podarki-na-den-rozhdeniya-zhene", source="queue",
         title="Подарки жене на день рождения: 15 идей",
         description="Что подарить жене на день рождения — романтичные и практичные идеи.",
         category="Женщине",
         intro="День рождения жены — повод сделать по-настоящему приятный подарок. Собрали идеи "
               "от романтичных до практичных.",
         keys=["flower_box","perfume","handbag_woman","cosmetics_set","photo_book","scented_bath_set",
               "makeup_mirror","wall_art"]),
]

def main():
    for art in ARTICLES:
        build_article(
            slug=art["slug"], title=art["title"], description=art["description"],
            category=art["category"], intro=art["intro"], keys=art["keys"],
            outro=OUTRO_DEFAULT, date=art.get("date"), source=art["source"],
        )
    print(f"Сгенерировано статей: {len(ARTICLES)}")

if __name__ == "__main__":
    main()
