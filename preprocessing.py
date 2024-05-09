import pandas as pd

class PreProcessData():

    def __init__(self):
        self.population = pd.read_html("assets/wikipedia_data.html")[1]
        self.nhl_pop, self.nba_pop, self.nfl_pop, self.mlb_pop = None, None, None, None

        self.nhl = pd.read_csv("assets/nhl.csv")
        self.nba = pd.read_csv("assets/nba.csv")
        self.nfl = pd.read_csv("assets/nfl.csv")
        self.mlb = pd.read_csv("assets/mlb.csv")

    def process_pop_data(self):
        self.population, store = self.population.iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area'), []
        for sport in ['NHL','NBA','NFL','MLB']:
            self.population[sport] = self.population[sport].replace("—", "").str.replace("\[.*\]","",regex=True)
            store.append(self.population[self.population[sport].str.contains('\w+')][['Population (2016 est.)[8]',sport]])
        self.nhl_pop, self.nba_pop, self.nfl_pop, self.mlb_pop = store[0], store[1], store[2], store[3] 

    def process_performance_data(self):
        for df in [self.nhl, self.nba, self.nfl, self.mlb]: df.drop(df.index[df['year'] != 2018], inplace=True)

        self.nhl['team'] = self.nhl['team'].str.replace('*', '')
        self.nba['team'] = self.nba['team'].str.replace('*', '').str.replace("\(.*\)","", regex=True)
        self.nfl['team'] = self.nfl['team'].str.replace('[*+]', '', regex=True)

        self.nhl = self.nhl.drop(self.nhl.index[self.nhl['team'].str.contains('Division')])
        self.nfl = self.nfl.drop(self.nfl.index[self.nfl['team'].str.contains('FC')])

        


processor = PreProcessData()
processor.process_pop_data()
print(processor.mlb_pop)