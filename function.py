def hold_power(values, times, power_lv):
    held_time = []
    start= 0
    for value,time in zip(values,times):
        if value <  power_lv:
            start = time
        if value > power_lv:
            end = time
            held_time.append(end-start)
    return max(held_time) 

value =[1,2,3,4,5,6,7,8]
time = [1,2,3,4,5,6,7,8]
power_lv = 2

print(hold_power(value,time,power_lv))
#%%

import json

def get_person_data():
    """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_names(person_data):
    """A Function that takes the persons-dictionary and returns a list auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names

def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""
    
    person_data = get_person_data()
    #print(suchstring)
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print()

            return eintrag
    else:
        return {}

if __name__ == "__main__":
 person_names_list = get_person_names()
 print(person_names_list)
 suchstring = "Huber, Julian"
 print(find_person_data_by_name(suchstring))