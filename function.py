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

class Person:

    @staticmethod
    def get_person_data() -> Table:
        """ A `staticmethod` that knows where the person Database is and returns a TinyDB-Table with the Persons """
        
        return TinyDB("data/person_db.json").table("persons")
        

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
        person_data = Person.get_person_data()
        if suchstring == "None":
            return {}

        lastname, firstname = suchstring.split(", ")
        PersonQuery = Query()
        found_list = person_data.search((PersonQuery.lastname == lastname) and (PersonQuery.firstname == firstname))
        if found_list == []:
            return None
        else:
            return found_list

    
    @staticmethod
    def load_by_id(person_id) -> dict:
        ''' A `staticmethod` that loads a person by id '''
        try:
            person = Person.get_person_data().get(doc_id=person_id)
            return person
        except:
            raise ValueError("Person with ID {} not found".format(id))

    @staticmethod
    def get_person_id(person_data):
        """Returns a list of all person IDs."""
        return [entry['id'] for entry in person_data]

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

    def __init__(self, person_dict):
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]

class EkgData:
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
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
        '''Function that knows where the person Database is and returns a TinyDB-Table with EKGs '''
        return TinyDB("data/person_db.json").table("ekg_tests")

    @staticmethod
    def load_by_person_id(ekg_id):
        """Loads an EKG test by ID."""
        EKGQuery = Query()
        EKGdata = EkgData.load_ekg_table()
        found_list = EKGdata.search(EKGQuery.person_id == ekg_id)
        if found_list == []:
            return None
        else:
            return found_list

    @staticmethod
    def get_ids(person_data):
        return [test["id"] for person in person_data for test in person["ekg_tests"]]

if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.get_person_data()
    person_names = Person.get_person_names(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))
    print("hallo")
    print(Person.load_by_id(3))
    print(Person.calc_max_heart_rate(20))
    print(Person.calc_age("2000-01-01"))
    print(EkgData.load_ekg_table())
    print(EkgData.load_by_person_id(1))
    ekg_dict = persons[0]["ekg_tests"][0]
    #ekg_instance = EkgData(ekg_dict)
    #print(ekg_instance.calc_duration())






