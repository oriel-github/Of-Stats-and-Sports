import pandas as pd
import scipy.stats as stats
from preprocessing import PreProcessData as Data
from cartesian_product import get_combinations_of, combos_in_cartesian

class MetroCorrelations(Data):

    ## Sport Name must be same format as performance_data string format, e.g. 'NHL'
    def __init__(self, formatted_metro_data, sport, sport_file):
        Data.__init__(self, formatted_metro_data, sport, sport_file)
        self.process_performance_data()
        self.process_pop_data()
        self.df = None
        self.coeff = None

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

    def get_team_metros(self):
        def match_metro(row): return self.metro_data[self.sport].apply(lambda x: self.match_teams(x, row)).dropna().index[0]
        self.data['Metropolitan area'] = self.data['team'].apply(match_metro)

    def get_performances(self):
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))

    def get_performances_by_metro(self):
        return self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()

    def get_metro_performance_corr(self): 
        self.df = self.metro_data.merge(self.get_performances_by_metro(), on='Metropolitan area')
        self.coeff = stats.pearsonr(self.df[self.pop_index()].apply(int), self.df['W/L ratio'])[0]


class SportCorrelations():

    ## Sport names and Data filenames need to match in length and sport order
    def __init__(self, formatted_metro_data, sports, sport_files):
        self.sports, self.pair_corrs, self.pair_corr_tests = sports, None, None
        self.metro_corrs = {s:self.get_metro_corr(formatted_metro_data, s, f) for s,f in zip(sports, sport_files)}

    def get_metro_corr(self, formatted_metro_data, sport, sport_file):
        metro_corr = MetroCorrelations(formatted_metro_data, sport, sport_file)
        metro_corr.get_team_metros()
        metro_corr.get_performances()
        metro_corr.get_metro_performance_corr()
        return metro_corr
    
    def get_corr_df_pair(self, sport_pair):
        return self.metro_corrs[sport_pair[0]].df.iloc[:,[0,2]], self.metro_corrs[sport_pair[1]].df.iloc[:,[0,2]]
    
    def get_pair_corr(self, corr_df_sport_pair):
        return (corr_df_sport_pair[0].merge(corr_df_sport_pair[1], on='Metropolitan area')
                                     .drop(columns=['Population (2016 est.)[8]_y', 'Population (2016 est.)[8]_x'])) 
    
    def get_pair_name(self, sport_pair_string_list):
        return sport_pair_string_list[0] + '_' + sport_pair_string_list[1]
    
    def get_pair_corrs(self):
        pairs = get_combinations_of(self.sports)
        self.pair_corrs = {p:self.get_pair_corr(self.get_corr_df_pair(p)) for p in pairs}
    
    def get_pair_corr_test(self, sport_corr_df):
        return stats.ttest_rel(sport_corr_df['W/L ratio_x'], sport_corr_df['W/L ratio_y'])
    
    def get_pair_corr_tests(self):
        self.pair_corr_tests = {pair:self.get_pair_corr_test(corr) for pair, corr in self.pair_corrs.items()}

    def get_pair_corr_pvals(self):
        self.pair_corr_pvals = {pair:test.pvalue for pair, test in self.pair_corr_tests.items()}

    def get_pval_matrix(self):
        return combos_in_cartesian(self.pair_corr_pvals)


if __name__ == "__main__":
    sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
    sport_name = 'NHL', 'NBA', 'NFL', 'MLB'
    metro_data = pd.read_html("assets/wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

    results = SportCorrelations(metro_data, sport_name, sport_data_paths)
    results.get_pair_corrs()
    results.get_pair_corr_tests()
    results.get_pair_corr_pvals()
    print(results.get_pval_matrix())