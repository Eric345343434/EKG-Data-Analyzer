import json

# Opening JSON file
def load_person_data():
    """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data
# %%

def get_person_list(person_data):
    """A Function that takes the Persons-Dictionary and returns a List auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names



# %% Test
#get_person_list(load_person_data())
