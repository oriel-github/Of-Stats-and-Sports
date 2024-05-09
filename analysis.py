import pandas as pd
import scipy.stats as stats
import preprocessing

class SportAnalysis():

    ## Sport Name must be same format as performance_data string format, e.g. 'NHL'
    def __init__(self, sport_name, performance_data, sport_pop_data):
        self.sport = sport_name
        self.data = performance_data
        self.pop = sport_pop_data

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

    def nhl_correlation(self): 
        def match_metro(row): return self.pop[self.sport].apply(lambda x: self.match_teams(x, row)).dropna().index[0]
        self.data['Metropolitan area'] = self.data['team'].apply(match_metro)
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))
        city_ratios = self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()
        self.pop = self.pop.merge(city_ratios, on='Metropolitan area')

        return stats.pearsonr(self.pop['Population (2016 est.)[8]'].apply(int), self.pop['W/L ratio'])[0]

    # def check_correct(self):
    #     assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    #     assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    #     assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    #     assert len(population_by_region) == 28

    #     assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    #     assert len(population_by_region) == 26

    #     assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    #     assert len(population_by_region) == 29


processor = preprocessing.PreProcessData()
processor.process_pop_data()
processor.process_performance_data()
analysis = SportAnalysis('NHL', processor.nhl, processor.nhl_pop)
print(analysis.nhl_correlation())