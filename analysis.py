import pandas as pd
import scipy.stats as stats
from preprocessing import PreProcessData as Data

class MetroPerformanceCorrelationBySport(Data):

    ## Sport Name must be same format as performance_data string format, e.g. 'NHL'
    def __init__(self, formatted_metro_data, metro_sport_name, sport_data_filename):
        Data.__init__(self, formatted_metro_data, metro_sport_name, sport_data_filename)
        self.process_performance_data()
        self.process_pop_data()
        self.corr = None

    def get_teams_from_string(self, string):
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

    def match_teams(self, metro_team_string, name_from_sport_data):
        for metro_team in self.get_teams_from_string(metro_team_string): 
            if metro_team in name_from_sport_data: return metro_team

    def match_team_to_metro(self):
        def match_metro(row): return self.metro_data[self.sport].apply(lambda x: self.match_teams(x, row)).dropna().index[0]
        self.data['Metropolitan area'] = self.data['team'].apply(match_metro)

    def get_team_performances(self):
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))

    def get_team_performances_by_metro(self):
        return self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()

    def get_metro_to_performance_correlation(self): 
        self.metro_data = self.metro_data.merge(self.get_team_performances_by_metro(), on='Metropolitan area')
        self.corr = stats.pearsonr(self.metro_data[self.pop_index()].apply(int), self.metro_data['W/L ratio'])[0]


class MetroPerformanceCorrelationAllSports():

    ## Sport names and Data filenames need to match in length and sport order
    def __init__(self, formatted_metro_data, metro_sport_names, sport_data_filenames):
        self.sport_list = metro_sport_names
        self.corr_pairs = []

        self.metro_perform_corr_by_sport = {}
        for sport, data in zip(metro_sport_names, sport_data_filenames):
            metro_perform_corr = MetroPerformanceCorrelationBySport(formatted_metro_data, sport, data)
            metro_perform_corr.match_team_to_metro()
            metro_perform_corr.get_team_performances()
            metro_perform_corr.get_metro_to_performance_correlation()
            self.metro_perform_corr_by_sport[sport] = metro_perform_corr

    def get_pairs_of(self, unpaired_list):
        pair_list, i = [], 0
        while i < len(unpaired_list):
            j = i + 1
            while j < len(unpaired_list):
                pair_list.append([unpaired_list[i], unpaired_list[j]])
                j += 1
            i += 1
        return pair_list
    
    def get_metro_perform_data_by_sport_pairs(self):
        sport_pairs = self.get_pairs_of(self.sport_list)
        metro_perform_data_by_sport_pairs = {}
        for pair in sport_pairs:
            first_sport_metro_data = self.metro_perform_corr_by_sport[pair[0]].metro_data
            second_sport_metro_data = self.metro_perform_corr_by_sport[pair[1]].metro_data
            pair_metro_data = first_sport_metro_data.merge(second_sport_metro_data, on='Metropolitan area')
            metro_perform_data_by_sport_pairs[pair[0] + '_' + pair[1]] = pair_metro_data
        return metro_perform_data_by_sport_pairs

    def get_metro_perform_corr_by_sport_pairs(self):
        




sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
sport_name = 'NHL', 'NBA', 'NFL', 'MLB'
metro_data = pd.read_html("assets/wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

# for n in [0, 1, 2, 3]:
#     analysis = MetroCorrelation(metro_data, sport_name[n], sport_data_paths[n])
#     analysis.get_correlation()
#     print(analysis.corr)

results = MetroPerformanceCorrelationAllSports(metro_data, sport_name, sport_data_paths)
print(results.get_metro_perform_data_by_sport_pairs())