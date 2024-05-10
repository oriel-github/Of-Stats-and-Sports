import pandas as pd

class PreProcessData():

    def __init__(self, formatted_population_data, population_sport_name, sport_data_filename):
        self.population = formatted_population_data
        self.sport = population_sport_name
        self.pop_data = None
        self.data = pd.read_csv(sport_data_filename)

    def pop_index(self):
        for col in self.population.columns: 
            if 'Population' in col: return col

    def process_pop_data(self):
        self.population[self.sport] = self.population[self.sport].replace("—", "").str.replace("\[.*\]","",regex=True)
        self.pop_data = self.population[self.population[self.sport].str.contains('\w+')][[self.pop_index(),self.sport]]

    def process_performance_data(self):
        self.data = self.data.drop(self.data.index[self.data['year'] != 2018])
        self.data = self.data.drop(self.data.index[self.data['team'].str.contains('FC')])
        self.data = self.data.drop(self.data.index[self.data['team'].str.contains('Division')])
        self.data['team'] = self.data['team'].replace('*','').replace('[*+]','', regex=True).replace("\(.*\)","", regex=True)


sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
sport_name = 'NHL', 'NBA', 'NFL', 'MLB'
population_data = pd.read_html("assets/wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

# for n in [0, 1, 2, 3]:
#     processor = PreProcessData(population_data, sport_name[n], sport_data_paths[n])
#     processor.process_pop_data()
#     print(processor.pop_data)