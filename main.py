import sqlite3
import pymorphy2
import string

morph = pymorphy2.MorphAnalyzer(lang='uk')

text = "Бандера один з головних ідеологів боротьби за незалежність України першої половини ХХ століття, символ національно-визвольного руху. У червні 1941 року керівництво крила ОУН, що було під орудою Бандери, проголосило у Львові Українську державу. Але оскільки нацистська Німеччина вже окупувала ці землі, Бандера був заарештований і провів три роки в німецьких тюрмах і таборах. З наближенням радянських військ у 1944-му Бандера знову очолив ОУН і залишався її керівником до останніх днів. Він був убитий у Мюнхені радянськими спецслужбами. Імя Степана Бандери і досі наводить жах на ворогів України. Саме тому радянська, а згодом і російська історіографія свідомо фальсифікує факти з його життя і діяльності."
words = [word.strip(string.punctuation) for word in text.split()]
# print(words)
# print(len(words))
# p = morph.parse(str(words[4]))[0]
# print(morph.parse(str(words[4]))[0].normal_form)
# print(p.tag.POS)
# print(p.tag.case)
conn = sqlite3.connect(':memory:')


c = conn.cursor()

# create table 'words'
c.execute("""CREATE TABLE words (
            word_id INTEGER PRIMARY KEY,
            meaning TEXT,
            pos_type TEXT,
            examples TEXT,
            spelling TEXT
            )""")

# create table 'pos'
c.execute("""CREATE TABLE pos (
            pos_type TEXT PRIMARY KEY
            )""")

# create table 'inflection_types'
c.execute("""CREATE TABLE inflection_types (
            inflection_type TEXT PRIMARY KEY
            )""")

# create table 'inflections'
c.execute("""CREATE TABLE inflections (
            word_id INTEGER PRIMARY KEY, 
            inflected_form TEXT,
            inflected_type TEXT
            )""")


def get_normal_form_of_the_word(word):
    normal_form = morph.parse(word)[0].normal_form
    return normal_form

def get_all_pos_from_text():
    pos_list = []
    for i in range(len(words)):
        word = words[i]
        part_of_speech = morph.parse(str(words[i]))[0]
        pos_list.append(part_of_speech.tag.POS)
    return set(pos_list)

def get_all_inflection_types_from_text():
    it_list = []
    for i in range(len(words)):
        word = words[i]
        it_list.append(morph.parse(word)[0].tag.case)
    return set(it_list)


def insert_pos():
    pos_set = get_all_pos_from_text()
    for pos in pos_set:
        conn.execute("INSERT INTO pos VALUES (:pos_type)", {'pos_type': pos})

def insert_words_and_inflections():
    for i in range(len(words)):
        word = words[i]
        normal_form = get_normal_form_of_the_word(word)
        pos = morph.parse(str(words[i]))[0]
        conn.execute("INSERT INTO words VALUES (NULL, :meaning, :pos_type, :examples, :spelling)", {'meaning': '-', 'pos_type': pos.tag.POS, 'examples': '-', 'spelling': normal_form})
        if (normal_form != word):
            case = morph.parse(word)[0].tag.case
            conn.execute("INSERT INTO inflections VALUES (NULL, :inflected_form, :inflected_type)", {'inflected_form': word, 'inflected_type': case})


def insert_inflection_types():
    it_set = get_all_inflection_types_from_text()
    for it in it_set:
        conn.execute("INSERT INTO inflection_types VALUES (:inflected_type)", {'inflected_type': it})


def get_pos():
    c.execute("SELECT * FROM pos")
    return c.fetchall()

def get_words():
    c.execute("SELECT * FROM words")
    return c.fetchall()

def get_inflections():
    c.execute("SELECT * FROM inflections")
    return c.fetchall()


def get_inflection_types():
    c.execute("SELECT * FROM inflection_types")
    return c.fetchall()



insert_pos()
insert_inflection_types()
insert_words_and_inflections();
print("Parts of speech:")
print(get_pos())

print("Inflection types:")
print(get_inflection_types())

print("Inflections:")
print(get_inflections())

print("Words:")
print(get_words())

