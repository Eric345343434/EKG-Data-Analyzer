import pandas as pd
import plotly.express as px
from tinydb import TinyDB, Query
from tinydb.table import Table, Document

def hold_power(values, times, power_lv):
    held_time = []
    start = None
    end = None

    for value, time in zip(values, times):
        if value >= power_lv and start is None:
            start = time
        if value < power_lv and end is None and start is not None:
            end = time
            held_time.append(end - start)
            start = None
            end = None

    return max(held_time)

class person:

    @staticmethod
    def get_person_data() -> Table:
        """ A `staticmethod` that knows where the person Database is and returns a TinyDB-Table with the Persons """
        return TinyDB("Data/person_db.json").table("persons")
        

    @staticmethod
    def get_person_names(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring) -> dict:
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        person_data = person.get_person_data()
        if suchstring == "None":
            return {}

        lastname, firstname = suchstring.split(", ")
        PersonQuery = Query()
        found_list = person_data.search((PersonQuery.lastname == lastname) and (PersonQuery.firstname == firstname))
        if found_list == []:
            return None
        else:
            return found_list[0]

    
    @staticmethod
    def load_by_id(person_id) -> dict:
        ''' A `staticmethod` that loads a person by id '''
        try:
            persone = person.get_person_data().get(doc_id=person_id)
            return persone
        except:
            raise ValueError("Person with ID {} not found".format(id))
    
    @staticmethod
    def find_person_id_by_name(suchstring) -> int:
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""
        person_data = person.get_person_data()
        if suchstring == "None":
            return {}

        lastname, firstname = suchstring.split(", ")
        PersonQuery = Query()
        found_list = person_data.search((PersonQuery.lastname == lastname) and (PersonQuery.firstname == firstname))
        if found_list == []:
            return None
        else:
            return found_list[0].doc_id
        
        
    @staticmethod
    def find_person_data_by_id(person_id) -> dict:
        """ Eine Funktion der die ID übergeben wird und die die Person als Dictionary zurück gibt"""
        person_data = person.get_person_data()
        PersonQuery = Query()
        found_list = person_data.search(PersonQuery.id == person_id)
        if found_list == []:
            return None
        else:
            return found_list
    
    @staticmethod
    def add_person(firstname: str, lastname: str, year_of_birth: int, picture_path: str):
        db = TinyDB("Data/person_db.json")
        person_table = db.table("persons")
        next_id = str(len(person_table) + 1)
        person_table.insert({
            "id": next_id,
            "year_of_birth": year_of_birth,
            "firstname": firstname,
            "lastname": lastname,
            "picture_path": picture_path
        })
    
    @staticmethod
    def update_person(person_id: int, firstname: str, lastname: str, year_of_birth: int, picture_path: str):
        """Updates the data of an existing person."""
        person_table = person.get_person_data()
        person_table.update({'firstname': firstname, 'lastname': lastname, 'year_of_birth': year_of_birth, 'picture_path': picture_path}, doc_ids=[person_id])
    
    @staticmethod
    def delete_person(person_id: int):
        """Deletes a person and their related EKG tests from the database."""
        person_table = person.get_person_data()
        person_table.remove(doc_ids=[person_id])
        ekgdata.delete_ekg_tests_by_person_id(person_id)


    @staticmethod
    def calc_max_heart_rate(age):
        """Calculates the max heart rate from the age."""
        return 220 - age

    @staticmethod
    def calc_age(birthdate):
        """Calculates the age from a birthdate."""
        today = pd.Timestamp.today()
        birthdate = pd.to_datetime(birthdate)
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def __init__(self, person_id):
        person_table = person.get_person_data().get(doc_id=person_id)
        self.year_of_birth = person_table["year_of_birth"]
        self.firstname = person_table["firstname"]
        self.lastname = person_table["lastname"]
        self.picture_path = person_table["picture_path"]
        self.id = person_table.doc_id

class ekgdata:
    def __init__(self, ekg_dict:int):
        ekg_table = ekgdata.load_ekg_table()
        self.id = ekg_table.get(doc_id=ekg_dict).doc_id
        self.date = ekg_table.get(doc_id=ekg_dict)["date"]
        self.data = ekg_table.get(doc_id=ekg_dict)["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.peaks = self.find_peaks()
        self.peaks_index = self.find_peaks_index()

    def find_peaks(self, threshold=340, respacing_factor=1):
        series = self.df["EKG in mV"]
        series = series.iloc[::respacing_factor]
        series = series[series > threshold]

        peaks = []
        last = current = next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current >= next and current > threshold:
                peaks.append(self.df["Time in ms"][index])

        return peaks

    def find_peaks_index(self, threshold=340, respacing_factor=1):
        series = self.df["EKG in mV"]
        series = series.iloc[::respacing_factor]
        series = series[series > threshold]

        peaks_index = []
        last = current = next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current >= next and current > threshold:
                peaks_index.append(index)

        return peaks_index

    def calc_duration(self):
        """Calculates the duration of the EKG-Test."""
        return (self.df["Time in ms"].iloc[-1] - self.df["Time in ms"].iloc[0]) / 1000

    @staticmethod
    def estimate_hr(peaks):
        if len(peaks) < 2:
            return None

        time_differences = [peaks[i] - peaks[i - 1] for i in range(1, len(peaks)) if peaks[i] - peaks[i - 1] > 200]
        avg_time_diff = sum(time_differences) / len(time_differences)
        avg_time_diff_s = avg_time_diff / 1000
        heart_rate = 60 / avg_time_diff_s

        return heart_rate

    def plot_ekg_with_peaks(self, start, end):
        df = self.df.copy()[start:end]
        df['Peaks'] = 0
        valid_peaks = [p for p in self.peaks_index if p in df.index]
        df.loc[valid_peaks, 'Peaks'] = 1

        fig = px.line(df, x='Time in ms', y='EKG in mV', title='EKG Data with Peaks')
        fig.add_scatter(x=df.loc[valid_peaks, 'Time in ms'], y=df.loc[valid_peaks, 'EKG in mV'], mode='markers', name='Peaks', marker=dict(color='red'))
        return fig
    
    @staticmethod
    def load_ekg_table() -> Table:
        '''Function that knows where the person Database is and returns a TinyDB-Table with EKGs
         -gives Table with all ekg´s '''
        return TinyDB("Data/person_db.json").table("ekg_tests")

    @staticmethod
    def load_by_ekg_id(ekg_id:int):
        """Loads an EKG test by ID."""
        EKGQuery = Query()
        EKGdata = ekgdata.load_ekg_table()
        found_list = EKGdata.search(EKGQuery.person_id == ekg_id)
        if found_list == []:
            return None
        else:
            return found_list
        
    @staticmethod
    def get_ekg_ids_by_person_id(person_id:int):
        '''gives all ekg_ids which belong to the given person_id
        -   list of the coresponding ekgs '''
        ekg_ids_1 = []
        for document in ekgdata.load_ekg_table():
            if document["person_id"] == person_id:
                ekg_ids_1.append(document.doc_id)
        ekg_ids=[]
        for i in range(0, len(ekg_ids_1)):
            ekg_ids.append(ekg_ids_1[i])            
        return ekg_ids

    @staticmethod
    def get_ids():
        '''Function that returns all IDs of the EKGs'''
        ids = []
        for person in ekgdata.load_ekg_table():
            ids.append(person.doc_id)
        return ids
    
    @staticmethod
    def add_ekg_test(person_id: int, date: str, result_link: str):
        """Adds a new EKG test to the database."""
        ekg_table = ekgdata.load_ekg_table()
        new_ekg_id = len(ekg_table) + 1
        new_ekg_test = {
            "person_id": person_id,
            "date": date,
            "result_link": result_link
        }
        ekg_table.insert(Document(new_ekg_test, doc_id=new_ekg_id))

    @staticmethod
    def delete_ekg_tests_by_person_id(person_id: int):
        """Deletes all EKG tests associated with a given person_id."""
        ekg_table = ekgdata.load_ekg_table()
        EKGQuery = Query()
        ekg_table.remove(EKGQuery.person_id == person_id)
    

    def df0(self):
        time = self.df["Time in ms"]
        time_difference = time[1]-time[0]
        Time_0=[]
        for i in range(len(time)):
            Time_0.append(i)
            i += time_difference
        return Time_0
    def time_dif(self):
        time = self.df["Time in ms"]
        time_difference = time[1]-time[0]
        return time_difference

        
if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = person.get_person_data()
    person_names = person.get_person_names(persons)
    print(person_names)
    print(person.find_person_data_by_name("Huber, Julian"))
    print("hallo -----------------")
    print(person.find_person_id_by_name("Huber, Julian"))
    print(person.find_person_id_by_name("Schmirander, Yunus"))
    print(person.find_person_id_by_name("Heyer, Yannic"))
    print(person.load_by_id(1))
    print(person.load_by_id(2))
    print(person.calc_max_heart_rate(20))
    print(person.calc_age("2000-01-01"))
    print(ekgdata.load_ekg_table())
    print(ekgdata.get_ekg_ids_by_person_id(1))
    print('create EKGdata object')
    ekg = ekgdata(2)
    #print(ekg.__dict__)
    print(ekg.peaks[:15])
    print(ekg.estimate_hr(ekg.peaks))
    print(ekg.get_ids())
    print(ekg.time_dif())
    






