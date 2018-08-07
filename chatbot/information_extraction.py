from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE

nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')


def get_data_from_file(file_path='./assignment_01.data'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]

    return cleaned_lines

sents = get_data_from_file()
cl = ClausIE.get_instance()
triples = cl.extract_triples(sents)

class Person(object):
    def __init__(self, name, likes=None, has=None, trips=None):
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.trips = [] if trips is None else trips
        self.heats = []

    def __repr__(self):
        return self.name

    def setlike(self, people):
        self.likes.append(people)

    def setpet(self, pet):
        self.has.append(pet)

    def settrip(self, trip):
        self.trips.append(trip)

    def setheat(self, people):
        self.heats.append(people)


class Pet(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.likes = []  # if likes is None else likes

    def __repr__(self):
        return self.name

    def setlike(self, pet):
        self.likes.append(pet)


class Trip(object):
    def __init__(self, depart_to, time):
        self.place = depart_to
        self.time = time

    def __repr__(self):
        return "to" + self.place


class Persons(object):
    def __init__(self):
        self.dict = {}

    def addperson(self, person):
        self.dict[person.name] = person


class Pets(object):
    def __init__(self):
        self.dict = {}

    def addpet(self, pet):
        self.dict[pet.name] = pet


class Trips(object):
    def __init__(self):
        self.dict = {}

    def addtrip(self, trip):
        self.dict[trip.place] = trip


persons = Persons()
pets = Pets()
trips = Trips()



def process_relation_triplet(triplet):

    global root
    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object
    doc = nlp(unicode(sentence))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
    # person and person are friend
    if root.lemma_ == 'be' and triplet.object == "friends":
        if len([e.text for e in doc.ents if e.label_ == 'PERSON']) == 2:
            name1 = str([e.text for e in doc.ents if e.label_ == 'PERSON'][0])
            name2 = str([e.text for e in doc.ents if e.label_ == 'PERSON'][1])
            if name1 not in persons.dict.keys() and name2 not in persons.dict.keys():
                a = Person(name1)
                b = Person(name2)
                a.setlike(b)
                b.setlike(a)
            elif name1 not in persons.dict.keys() and name2 in persons.dict.keys():
                a = Person(name1)
                persons.dict[name2].setlike(a)
                a.setlike(persons.dict[name2])
                persons.addperson(a)
            elif name1 in persons.dict.keys() and name2 not in persons.dict.keys():
                b = Person(name2)
                persons.dict[name1].setlike(b)
                b.setlike(persons.dict[name1])
                persons.addperson(b)
            else:
                persons.dict[name1].setlike(persons.dict[name2])
                persons.dict[name2].setlike(persons.dict[name1])

    # person likes person
    if root.lemma_ == 'like' and "n't" not in [token.text for token in doc]:
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON' or 'ORG'] and triplet.object in [e.text
                                                                                                                 for e
                                                                                                                 in
                                                                                                                 doc.ents
                                                                                                                 if
                                                                                                                 e.label_ == 'PERSON']:
            if triplet.subject not in persons.dict.keys() and triplet.object not in persons.dict.keys():
                a = Person(triplet.subject)
                b = Person(triplet.object)
                a.setlike(b)
                persons.addperson(a)
                persons.addperson(b)
            elif triplet.subject in persons.dict.keys() and triplet.object not in persons.dict.keys():
                b = Person(triplet.object)
                persons.dict[triplet.subject].setlike(b)
            elif triplet.subject not in persons.dict.keys() and triplet.object in persons.dict.keys():
                a = Person(triplet.subject)
                a.setlike(persons.dict[triplet.object])
                persons.addperson(a)
            else:
                persons.dict[triplet.subject].setlike(persons.dict[triplet.object])
    if root.lemma_ == 'like' and "n't" in [token.text for token in doc]:
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON' or 'ORG'] and triplet.object in [e.text
                                                                                                                 for e
                                                                                                                 in
                                                                                                                 doc.ents
                                                                                                                 if
                                                                                                                 e.label_ == 'PERSON']:
            persons.dict[triplet.subject].setheat(triplet.object)
    # person is friend with person
    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        if len([e for e in fw_doc.ents if e.label_ == 'PERSON']) == 1:
            fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON'][0].text
            if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in
                                                                                                    doc.ents
                                                                                                    if
                                                                                                    e.label_ == 'PERSON']:
                if triplet.subject not in persons.dict.keys() and fw_who not in persons.dict.keys():
                    a = Person(triplet.subject)
                    b = Person(fw_who)
                    a.setlike(b)
                    b.setlike(a)
                    persons.addperson(a)
                    persons.addperson(b)
                elif triplet.subject in persons.dict.keys() and fw_who not in persons.dict.keys():
                    b = Person(fw_who)
                    persons.addperson(b)
                    persons.dict[triplet.subject].setlike(b)
                    b.setlike(persons.dict[triplet.subject])
                elif triplet.subject not in persons.dict.keys() and fw_who in persons.dict.keys():
                    a = Person(triplet.subject)
                    a.setlike(persons.dict[fw_who])
                    persons.addperson(a)
                    persons.dict[fw_who].setlike(a)
                else:
                    if persons.dict[fw_who] not in persons.dict[triplet.subject].likes and persons.dict[
                        triplet.subject] not in persons.dict[fw_who].likes:
                        persons.dict[triplet.subject].setlike(persons.dict[fw_who])
                        persons.dict[fw_who].setlike(persons.dict[triplet.subject])
                    else:
                        persons.dict[fw_who].setlike(persons.dict[triplet.subject])
        else:
            fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON']
            fw_all = [re_spaces.split(str(e)) for e in fw_who]
            for i in fw_all:
                for name in i:
                    if name in persons.dict.keys() and triplet.subject in persons.dict.keys():
                        persons.dict[name].setlike(persons.dict[triplet.subject])
                        persons.dict[triplet.subject].setlike(persons.dict[name])
                    elif name not in persons.dict.keys() and triplet.subject in persons.dict.keys():
                        a = Person(name)
                        a.setlike(persons.dict[triplet.subject])
                        persons.addperson(a)
                        persons.dict[triplet.subject].setlike(a)
                    elif name in persons.dict.keys() and triplet.subject not in persons.dict.keys():
                        a = Person(triplet.subject)
                        a.setlike(persons.dict[name])
                        persons.dict[name].setlike(a)
                        persons.addperson(a)
                    else:
                        a = Person(name)
                        b = Person(triplet.subject)
                        a.setlike(b)
                        b.setlike(a)
                        persons.addperson(a)
                        persons.addperson(b)
    # people has a pet names xx
    if root.lemma_ == "have" and ("named" in triplet.object):
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))
        # chunks = list(doc.noun_chunks)
        span_text = obj_span.text
        span_list = span_text.split("named")
        pet_name = str(span_list[-1]).strip()
        s_people = str([token.text for token in doc if token.ent_type_ == 'PERSON'][0])
        type = 'dog' if 'dog' in triplet.object else 'cat'
        if s_people not in persons.dict.keys():
            a = Person(s_people)
            b = Pet(pet_name, type)
            a.setpet(b)
            persons.addperson(a)
            pets.addpet(b)
        else:
            b = Pet(pet_name, type)
            persons.dict[s_people].setpet(b)
            pets.addpet(b)
    # Process (people's PET'NAME is xx)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))
        if obj_span[0].pos_ == 'PROPN':  # len(obj_span) == 1 and
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))
            s_people = str([token.text for token in subj_doc if token.ent_type_ == 'PERSON'][0])
            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'
            if s_people in persons.dict.keys():
                a = Pet(name, s_pet_type)
                persons.dict[s_people].setpet(a)
                pets.addpet(a)
            else:
                a = Pet(name, s_pet_type)
                b = Person(s_people)
                b.setpet(a)
                persons.addperson(b)
                pets.addpet(a)
    if ('GPE' in [e.label_ for e in doc.ents] or 'ORG' in [e.label_ for e in doc.ents])  and  'DATE' in [e.label_ for e in doc.ents]:
        sub_span = doc.char_span(sentence.find(triplet.subject), len(triplet.subject))
        time = [str(e.text) for e in doc.ents if e.label_ == 'DATE'][0]
        place = [str(e.text) for e in doc.ents if e.label_ == 'GPE'][0]
        if len(sub_span) == 1 and sub_span[0].pos_ == 'PROPN':
            name = str(triplet.subject)
            if name not in persons.dict.keys():
                b = Person(name)
                a = Trip(place, time)
                b.settrip(a)
                trips.addtrip(a)
                persons.addperson(b)
            else:
                a = Trip(place, time)
                trips.addtrip(a)
                persons.dict[name].settrip(a)
        else:
            people = [str(e.text) for e in doc.ents if e.label_ == 'PERSON']
            count = len([str(e.text) for e in doc.ents if e.label_ == 'PERSON'])
            for i in range(count):
                if people[i] not in persons.dict.keys():
                    a = Trip(place, time)
                    trips.addtrip(a)
                    b = Person(people[i])
                    b.settrip(a)
                else:
                    a = Trip(place, time)
                    trips.addtrip(a)
                    persons.dict[people[i]].settrip(a)
    if root.lemma_ == "like" and (triplet.object in pets.dict.keys()):  ##and triplet.subject in pets.dict.keys()):
        pets.dict[triplet.subject].setlike(pets.dict[triplet.object])
    if triplet.object.startswith('friends with') and triplet.subject in pets.dict.keys():
        fw_doc = nlp(unicode(triplet.object))
        if 'ORG' in [e.label_ for e in fw_doc.ents]:
            fw_who = str([e for e in fw_doc.ents if e.label_ == 'ORG'][0].text)
            pets.dict[triplet.subject].setlike(pets.dict[fw_who])
            pets.dict[fw_who].setlike(pets.dict[triplet.subject])





'''for t in triples:
    process_relation_triplet(t)'''
1+1

def process_data_from_input_file():

    for t in triples:
        process_relation_triplet(t)


def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


def answer_question(question_string):
    q_doc = nlp((unicode(preprocess_question(preprocess_question(question_string)))))
    try:
        q_trip = cl.extract_triples([preprocess_question(question_string)])[0]
        # Who has a <pet_type>?
        if q_trip.subject.lower() == 'who' and q_trip.predicate == "has":
            if q_trip.object in ["dog", 'cat']:

                answer = '{} has a {} named {}.'
                for person in persons.dict.values():
                    for pet in person.has:
                        if pet.type == q_trip.object:
                            print(answer.format(person, q_trip.object, pet))
            else:
                 print("I don't know.")
        # Who is [going to|flying to|traveling to] <place>?
        if q_trip.subject.lower() == 'who' and ("GPE" in [e.label_ for e in q_doc.ents]):
            # answer = '{} {} {}'
            q_place = str([e.text for e in q_doc.ents if e.label_ == "GPE"][0])
            count = 0
            name = []
            for person in persons.dict.values():
                for trip in person.trips:
                    if trip.place == q_place:
                        name.append(person.name)
                        count += 1
            if count == 0:
                print("I don't know.")
            else:
                for i in name:

                    print(i, q_trip.predicate, "to", q_place,".")
        # Does <person> like <person>? (e.g. Does Bob like Sally?)
        if q_trip.subject.lower().startswith('does') and q_trip.predicate == 'like':
            name1 = str([e.text for e in q_doc.ents if e.label_ == "PERSON"][0])
            name2 = str(q_trip.object)

            if name1 not in persons.dict.keys():
                print("I don't know.")
            else:
                likes = []
                for people in persons.dict[name1].likes:
                    likes.append(people.name)
                heats = []
                for people in persons.dict[name1].heats:
                    heats.append(people)
                if name2 not in likes and name2 not in heats:
                    print("I don't know.")
                elif name2 in likes:
                    print(name1, "likes", name2,".")
                elif name2 in heats:
                    print(name1, "doesn't","like", name2,".")
        # who likes xx
        if q_trip.subject.lower() == 'who' and q_trip.predicate == 'likes':
            name = str(q_trip.object)
            count = 0
            if name not in persons.dict.keys():
                print("I don't know.")
            else:
                for person in persons.dict.values():
                    for liker in person.likes:
                        if name == liker.name:
                            print(person.name, "likes", name)
                            count += 1
                if count == 0:
                    print("I don't know.")
        # who does xx like
        if q_trip.object.lower() == 'who' and q_trip.predicate.lower().startswith('does'):
            name = str(q_trip.subject)
            try:
                likes = persons.dict[name].likes
                for people in likes:
                    print(name, "likes", people,".")
            except KeyError:
                print("I don't know")
        # when is mary going wo japan?
        if "when" in re_spaces.split(str(q_trip.object).lower()) and ("GPE" in [e.label_ for e in q_doc.ents]):
            name = str(q_trip.subject)
            way = q_trip.predicate
            q_place = str([e.text for e in q_doc.ents if e.label_ == "GPE"][0])
            if name not in persons.dict.keys():
                print("I don't know.")
            else:
                if persons.dict[name].trips == []:
                    print("I don't know.")
                else:
                    try:
                        persons.dict[name].trips[0]
                        count = 0
                        for i in range(len(persons.dict[name].trips)):
                            trip = persons.dict[name].trips[i]
                            if q_place == trip.place:
                                count += 1
                                print(name, way, "to", trip.place, "in", trip.time,".")
                        if count == 0:
                            print("I don't know.")
                    except IndexError:
                        print("I don't know.")
    except ValueError:
        if 'PERSON' in [e.label_ for e in q_doc.ents]:
            name = [str(e.text) for e in q_doc.ents if e.label_ == 'PERSON'][0]
            if name in persons.dict.keys():

                chunks = list(q_doc.noun_chunks)
                target = cl.extract_triples([preprocess_question(chunks[-1].text)])[0]
                answer = "{}'s {} name is {}"
                count = 0
                for pet in persons.dict[name].has:
                    if pet.type == target.object:
                        print(answer.format(name, target.object,pet.name))
                        count += 1
                if count == 0:
                    print("I don't know.")
            else:
                print("I don't know.")







def main():
    global sents
    process_data_from_input_file()


    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")

        if question[-1] != '?':
            print('This is not a question... please try again')
    answer_question(question)


if __name__ == '__main__':
    main()
