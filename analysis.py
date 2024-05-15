import pandas as pd
import scipy.stats as stats
from preprocessing import PreProcessData as Data
from cartesian_product import get_combinations_of, combos_in_cartesian
from string_of_teams_extraction import match_teams

class MetroCorrelations(Data):

    def __init__(self, formatted_metro_data, sport, sport_file):
        Data.__init__(self, formatted_metro_data, sport, sport_file)
        self.process_performance_data()
        self.process_pop_data()
        self.df = None
        self.coeff = None

    def get_team_metros(self):
        def match_metro(row): 
            matches = self.metro_data[self.sport].apply(lambda x: match_teams(x, row)).dropna()
            if matches.empty: return 'No matching metro team'
            else: return matches.index[0]
        self.data['Metropolitan area'] = self.data['team'].apply(match_metro)

    def get_performances(self):
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))

    def get_performances_by_metro(self):
        self.data = self.data.drop(self.data.index[self.data['Metropolitan area'] == 'No matching metro team'])
        return self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()

    def get_metro_performance_corr(self): 
        self.df = self.metro_data.merge(self.get_performances_by_metro(), on='Metropolitan area')
        self.coeff = stats.pearsonr(self.df[self.pop_index()].apply(float), self.df['W/L ratio'])[0]


class SportCorrelations():

    def __init__(self, formatted_metro_data, sports, sport_files):
        self.sports, self.pair_corrs, self.pair_corr_tests, self.pair_corr_pvals = sports, None, None, None
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
        pop_col = self.metro_corrs[self.sports[0]].pop_index()
        return (corr_df_sport_pair[0].merge(corr_df_sport_pair[1], on='Metropolitan area')
                                     .drop(columns=[f'{pop_col}_y', f'{pop_col}_x'])) 
    
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
    print(results.pair_corrs)
    print(results.pair_corr_tests)
    print(results.pair_corr_pvals)
    print(results.get_pval_matrix())
