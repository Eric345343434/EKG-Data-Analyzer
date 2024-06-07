import json
import pandas as pd
def hold_power(values, times, power_lv):
    held_time = []
    start = None
    end = None

    for value, time in zip(values, times):

        if value >= power_lv and start is None:
            start = time

        if value < power_lv and end is None and start is not None:
            end = time
            held_time.append(end-start)
            start = None
            end = None

    return max(held_time)



class person:


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
        
        person_data = person.get_person_data()
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
        
    def load_by_id(person_id):
        """A Function that loads a person by ID"""
        person_data = person.get_person_data()
        for eintrag in person_data:
            if eintrag["id"] == person_id:
                return eintrag
        else:
            return {}
    def get_person_id(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person id"""
        list_of_id = []
        for eintrag in person_data:
            list_of_id.append(eintrag["id"])
        return list_of_id
    def calc_max_heart_rate(age):
        """A Function that calculates the max heart rate from the age"""
        return 220 - age



    def calc_age(birthdate):
        """A Function that calculates the age from a birthdate"""
        today = pd.Timestamp.today()
        birthdate = pd.to_datetime(birthdate)
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age


    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]

if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = person.get_person_data()
    person_names = person.get_person_names(persons)
    print(person_names)
    print(person.find_person_data_by_name("Huber, Julian"))





# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class ekgdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        self.peaks = self.find_peaks()
    
    def find_peaks(self, threshold=340, respacing_factor=5):
        series = self.df["EKG in mV"]
        # Respace the series
        series = series.iloc[::respacing_factor]
        
        # Filter the series
        series = series[series>threshold]

        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index-respacing_factor)
        return peaks

    def estimate_hr(peaks):
        if len(peaks) < 2:
             return 0  # No valid heart rate can be calculated with less than 2 peaks

        total_time = 0
        for i in range(len(peaks) - 1):
            total_time += peaks[i + 1] - peaks[i]

        heart_rate = len(peaks) / (total_time / 1000)  # Convert milliseconds to seconds
        return heart_rate

    def load_by_id(ekg_id):
        """A Function that loads a person by ID"""
        person_data = person.get_person_data()
        for eintrag in person_data:
            for test in eintrag["ekg_tests"]:
                if test["id"]== ekg_id:
                    return test
        else:
            return {}
        



    def get_ids(person_data):
        ekg_ids=[]
        for eintrag in person_data:
            ekg_ids.append(eintrag["id"])
        return ekg_ids
    



if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = ekgdata(ekg_dict)
    print(ekg.df.head())
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = ekgdata(ekg_dict)


