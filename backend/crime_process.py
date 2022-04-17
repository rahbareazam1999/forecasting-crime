import pandas as pd
import numpy as np

URL = "/home/student/cs-12200-project/Data/mini_db/"
df = pd.read_csv(URL + 'raw_csv/crime.csv', encoding = "ISO-8859-1")

def crime_csv_create(df):
    '''This function takes the dataframe of the crime csv and 
        returns a clean, indexed CSV.
    '''

    # converting the numbers from object to ints
    df.iloc[:,5:18] = df.iloc[:,5:18].apply(pd.to_numeric, errors = 'coerce')

    # adding the Total column
    df["total"] = df['January'] + df['February'] + df['March'] + df['April'] + df['May'] + df['June'] + df['July'] + df['August'] + df['September'] + df['October'] + df['November'] + df['December']

    #Drop monthly observation
    df.drop(df.columns[6:18], axis=1, inplace=True)

    #Generate sums for type of crimes: violent, non_violent and violent 
    df["violent"] = df["total"][(df["Type of crime"] == "DOLOSOS") | (df["Type of crime"] == "DOLOSAS") | (df["Type of crime"] == "SECUESTRO") | (df["Type of crime"] == "EXTORSION") | (df["Type of crime"] == "DOLOSOS") | (df["Type of crime"] == "CON VIOLENCIA") | (df["Type of crime"] == "VIOLACION")]
    df["homicides"] = df["total"][(df["Type of crime"] == "DOLOSOS") & (df["Crime type"] == "HOMICIDIOS")]

    # Obtain 10 different tipe of crimes
    list_crimes = df["Crime type"].unique()
    for i in list_crimes:
        df[i] = df["total"][df["Crime type"] == i]

    df["violent"] = df["total"][(df["Type of crime"] == "DOLOSOS") | (df["Type of crime"] == "DOLOSAS") | (df["Type of crime"] == "SECUESTRO") | (df["Type of crime"] == "EXTORSION") | (df["Type of crime"] == "DOLOSOS") | (df["Type of crime"] == "CON VIOLENCIA") | (df["Type of crime"] == "VIOLACION")]

    #Group for state and year
    df = df.groupby(["year","state_key","state_name"])
    df = df.aggregate(np.sum)

    #Create non-violent crimes with aggregations
    df["no_violent"] = df["total"] - df["violent"]
    del df["Sub type of crime"]

    df.to_csv(URL + "process_csv/crime.csv", sep='\t')


crime_csv_create(df)
