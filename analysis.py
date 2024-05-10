import pandas as pd
import scipy.stats as stats
from preprocessing import PreProcessData as Data

class SportAnalysis(Data):

    ## Sport Name must be same format as performance_data string format, e.g. 'NHL'
    ## Assumes population and performance df are preprocessed
    def __init__(self, formatted_population_data, population_sport_name, sport_data_filename):
        Data.__init__(self, formatted_population_data, population_sport_name, sport_data_filename)
        self.process_performance_data()
        self.process_pop_data()
        self.corr = None

    def split_team_names(self, string):
        split = string.split(' ')
        if len(split) > 1:
            new_split = []
            while split != []:
                if split[0][-1] == 's': 
                    new_split.append(split.pop(0))
                    if split == []: break
                if split[0][-1] != 's': 
                    if len(split) == 1: new_split.append(split.pop(0))
                    else: new_split.append(' '.join([split.pop(0), split.pop(0)]))
            return new_split
        else: return split

    def match_teams(self, region_team_string, team_to_match):
        for region_team in self.split_team_names(region_team_string): 
            if region_team in team_to_match: return region_team

    def get_correlation(self): 
        def match_metro(row): return self.pop_data[self.sport].apply(lambda x: self.match_teams(x, row)).dropna().index[0]
        self.data['Metropolitan area'] = self.data['team'].apply(match_metro)
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))
        city_ratios = self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()
        self.pop_data = self.pop_data.merge(city_ratios, on='Metropolitan area')
        self.corr = stats.pearsonr(self.pop_data[self.pop_index()].apply(int), self.pop_data['W/L ratio'])[0]


sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
sport_name = 'NHL', 'NBA', 'NFL', 'MLB'
population_data = pd.read_html("assets/wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

for n in [0, 1, 2, 3]:
    analysis = SportAnalysis(population_data, sport_name[n], sport_data_paths[n])
    analysis.get_correlation()
    print(analysis.corr)
