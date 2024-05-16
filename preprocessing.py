import pandas as pd

## Cleaning both population and sport data 
class PreProcessData():

    def __init__(self, formatted_metro_data, sport, sport_file):
        self.metro = formatted_metro_data
        self.sport = sport
        self.metro_data = None
        self.data = pd.read_csv(sport_file)

    ## Defined here to be used in parent and throughout all child classes
    def pop_column_name(self):  
        for col in self.metro.columns: 
            if 'Population' in col: return col  # Can't hard code column name because Wiki includes year in the name
        raise Exception('No Population Data Column in Population file')  # Catches when no population data

    ## Cleans population dataframe
    def process_pop_data(self):
        pop_col = self.pop_column_name()
        self.metro[pop_col] = self.metro[pop_col].replace("\[.*\]","", regex=True).replace(",","", regex=True)
        self.metro[self.sport] = self.metro[self.sport].replace("—", "").str.replace("\[.*\]","",regex=True)
        self.metro_data = self.metro[self.metro[self.sport].str.contains('\w+')][[pop_col,self.sport]]

    ## Cleans sport dataframe
    def process_performance_data(self):
        self.data = self.data.drop(self.data.index[self.data['year'] != 2018])  # The latest year from sport data csv's
        self.data = self.data.drop(self.data.index[self.data['team'].str.contains('FC')])
        self.data = self.data.drop(self.data.index[self.data['team'].str.contains('Division')])
        self.data['team'] = self.data['team'].replace('*','').replace('[*+]','', regex=True).replace("\(.*\)","", regex=True)




if __name__ == "__main__":
    sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
    sport_name = 'NHL', 'NBA', 'NFL', 'MLB'
    metro_data = pd.read_html("assets/wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

    for n in [0, 1, 2, 3]:
        processor = PreProcessData(metro_data, sport_name[n], sport_data_paths[n])
        processor.process_pop_data()
        print(processor.metro_data)