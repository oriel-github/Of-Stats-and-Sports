import pandas as pd
import scipy.stats as stats
from preprocessing import PreProcessData as Data
from cartesian_product import get_combinations_of, combos_in_cartesian
from string_of_teams_extraction import match_teams

## Helper class for the primary SportCorrelations class, feeding it Correlation by Metro data for a single sport
class MetroCorrelations(Data):

    ## Inherits methods/attributes to access processed data while separating out correlation analysis methods/attributes
    def __init__(self, formatted_metro_data, sport, sport_file):
        Data.__init__(self, formatted_metro_data, sport, sport_file)
        self.process_performance_data()
        self.process_pop_data()
        self.df = None
        self.coeff = None
    
    def match_metro(self, team): 
        ## Calls function from string_of_teams_extraction.py to see which metro team the sport data team matches to
        team_matches = self.metro_data[self.sport].apply(lambda metro_teams: match_teams(metro_teams, team)).dropna()
        if team_matches.empty: return 'Unknown Metro'  # Later merging will drop any performance data with 'Unknown Metro' 
        else: return team_matches.index[0]  # Returns the Metro associated with the Metro team name

    ## Calls a helper method to associate teams to their metros in order to aggregate performance by metro
    def get_team_metros(self):
        self.data['Metropolitan area'] = self.data['team'].apply(self.match_metro)

    def get_performances(self):  # Performances by team
        self.data['W/L ratio'] = self.data['W'].apply(int) / (self.data['W'].apply(int) + self.data['L'].apply(int))

    def get_performances_by_metro(self):
        return self.data[['W/L ratio', 'Metropolitan area']].groupby('Metropolitan area').mean()

    ## Merges sport & metro dataframes to align performance & population data, via Metro, allowing their correlation calculation
    def get_metro_performance_corr(self): 
        self.df = self.metro_data.merge(self.get_performances_by_metro(), on='Metropolitan area')
        self.coeff = stats.pearsonr(self.df[self.pop_column_name()].apply(float), self.df['W/L ratio'])[0]


## The base class that the main.py classes inherit statistical analysis methods/attributes from and package for output uses
class SportCorrelations():

    ## Instantiates MetroCorrelation class for each sport, for use both for Population & Pairwise Correlation Analyses
    def __init__(self, formatted_metro_data, sports, sport_files):
        self.sports, self.pair_corrs, self.pair_corr_tests, self.pair_corr_pvals = sports, None, None, None
        self.metro_corrs = {s:self.get_metro_corr(formatted_metro_data, s, f) for s,f in zip(sports, sport_files)}

    def get_metro_corr(self, formatted_metro_data, sport, sport_file):
        metro_corr = MetroCorrelations(formatted_metro_data, sport, sport_file)
        metro_corr.get_team_metros()
        metro_corr.get_performances()
        metro_corr.get_metro_performance_corr()
        return metro_corr
    
    ## Helper method to extract a sport pair's corresponding performance data 
    def get_corr_df_pair(self, sport_pair):
        return self.metro_corrs[sport_pair[0]].df.iloc[:,[0,2]], self.metro_corrs[sport_pair[1]].df.iloc[:,[0,2]]
    
    ## Culls only the performance data of shared metros to properly calculate correlation 
    def get_pair_corr(self, corr_df_sport_pair):
        pop_col = self.metro_corrs[self.sports[0]].pop_column_name()
        return (corr_df_sport_pair[0].merge(corr_df_sport_pair[1], on='Metropolitan area')
                                     .drop(columns=[f'{pop_col}_y', f'{pop_col}_x'])) 
    
    ## Calls pairwise generator function from cartesian_product.py to apply get_pair_corr() for all sport pairs
    def get_pair_corrs(self):
        pairs = get_combinations_of(self.sports)
        self.pair_corrs = {p:self.get_pair_corr(self.get_corr_df_pair(p)) for p in pairs}
    
    ## Performs ttest on said sport pair
    def get_pair_corr_test(self, sport_corr_df):
        return stats.ttest_rel(sport_corr_df['W/L ratio_x'], sport_corr_df['W/L ratio_y'])
    
    ## Assumes get_pair_corrs() has been called to define data for all pairs to apply ttest across all pairs
    def get_pair_corr_tests(self):
        self.pair_corr_tests = {pair:self.get_pair_corr_test(corr) for pair, corr in self.pair_corrs.items()}

    ## Assumes get_pair_corr_tests() has been called to define ttests for all pairs to extract all their p-vals  
    def get_pair_corr_pvals(self):
        self.pair_corr_pvals = {pair:test.pvalue for pair, test in self.pair_corr_tests.items()}

    ## Assumes get_pair_corr_pvals() has been called to define p-vals for all pairs to produce p-val matrix
    ## Calls function from cartesian_product.py to translate pair correlations all pairwise options in matrix 
    def get_pval_matrix(self):
        return combos_in_cartesian(self.pair_corr_pvals)

    


if __name__ == "__main__":
    sport_data_paths = ["assets/nhl.csv", "assets/nba.csv", "assets/nfl.csv", "assets/mlb.csv"]
    sport_names = 'NHL', 'NBA', 'NFL', 'MLB'
    metro_data = pd.read_html("https://en.wikipedia.org/wiki/List_of_American_and_Canadian_cities_by_number_of_major_professional_sports_franchises")[1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

    results = SportCorrelations(metro_data, sport_names, sport_data_paths)
    results.get_pair_corrs()
    results.get_pair_corr_tests()
    results.get_pair_corr_pvals()
    print(results.pair_corrs)
    print(results.pair_corr_tests)
    print(results.pair_corr_pvals)
    print(results.get_pval_matrix())
