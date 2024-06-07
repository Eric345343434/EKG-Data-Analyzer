from function import ekgdata,person
import pandas as pd

ekg_dict = ekgdata.load_by_id(1) 
print(ekg_dict)
ekgdata1= ekgdata(ekg_dict)

ekgdata1.find_peaks()
print(ekgdata1.find_peaks())

