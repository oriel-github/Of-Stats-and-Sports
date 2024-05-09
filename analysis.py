import pandas as pd
import numpy as np
import scipy.stats as stats

class Analysis():

    def __init__(self) -> None:
        pass

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
        def match_metro(row): return nhl_pop['NHL'].apply(lambda x: match_teams(x, row)).dropna().index[0]
        nhl['Metropolitan area'] = nhl['team'].apply(match_metro)
        city_ratios = nhl[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()
        nhl_pop = nhl_pop.merge(city_ratios, on='Metropolitan area')

        population_by_region = nhl_pop['Population (2016 est.)[8]'].apply(int) # pass in metropolitan area population from cities
        win_loss_by_region = nhl_pop['W/L ratio'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
        
        assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
        assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

        assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
        assert len(population_by_region) == 28

        assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
        assert len(population_by_region) == 26

        assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
        assert len(population_by_region) == 29
        
        return stats.pearsonr(population_by_region, win_loss_by_region)[0]
