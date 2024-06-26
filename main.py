import pandas as pd
from analysis import SportCorrelations as Corrs

## Loads all wiki tables from URL page into list, so formatting assumes current wiki table column layout
## Specifically Metro name at col 0, population at 3, Big 4 at 5-8
def get_population_data(population_data_filename, pop_data_table_no = 1):
    return pd.read_html(population_data_filename)[pop_data_table_no - 1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

## Extracts sport names as used by population data to set as instance variables for many methods to call df columns
def get_sport_list(formatted_population_data):
    return list(formatted_population_data.columns[1:])


## For seeing results of pairwise sports performance across the population, whether they behave the same or not
class SportsPerformanceRelationship(Corrs):

    ## sports file order in sport_data_filename_list needs to correspond to sport order in Wiki population data table
    ## If population data isn't the first table e.g. If 3rd table that appears on the page, specify pop_data_table_no = 3
    def __init__(self, sport_data_filename_list, population_data_filename, pop_data_table_no = 1):
        population_data = get_population_data(population_data_filename, pop_data_table_no)
        super().__init__(population_data, get_sport_list(population_data), sport_data_filename_list)
        self.get_pair_corrs()
        self.get_pair_corr_tests()
        self.get_pair_corr_pvals()

    ## Default results displayed as pairwise matrix table 
    def __str__(self):
        results = self.get_pval_matrix().map(lambda x: self.classify_pval(x))
        return f'Pairwise Sport Performance t-Test Results:\n {results}'
    
    def classify_pval(self, p_val): ## Classifying ttest results at 95% Confidence 
        if p_val < 0.05: return 'Not Same'
        else: return 'Same'


## For seeing results of population to sports performance
class PopulationPerformanceRelationship(Corrs):

    ## sports file order in sport_data_filename_list needs to correspond to sport order in Wiki population data table
    ## If population data isn't the first table e.g. If 3rd table that appears on the page, specify pop_data_table_no = 3
    def __init__(self, sport_data_filename_list, population_data_filename, pop_data_table_no = 1):
        self.population_data = get_population_data(population_data_filename, pop_data_table_no)
        sports = get_sport_list(self.population_data)
        super().__init__(self.population_data, sports, sport_data_filename_list)

    ## Default results display in tabular form the correlation coefficients and classifications for each sport
    def __str__(self):
        results = {team:corr.coeff for team, corr in self.metro_corrs.items()}
        df = pd.DataFrame.from_dict(results, orient='index', columns=['Pearson R Coefficient'])
        df['Class'] = df['Pearson R Coefficient'].apply(self.classify_corr)
        return f"Population-Performance Correlation Results:\n {df}"
    
    def classify_corr(self, corr):
        if float('%.2f' % corr) == 0.00: return 'No Correlation'  ## Corr at most ±0.499%, basically insignificant corr to report
        elif corr > 0.7: return 'Strong, Positive Correlation'
        elif corr < -0.7: return 'Strong, Negative Correlation'
        elif corr < 0: return 'Weak, Negative Correlation'
        else: return 'Weak, Positive Correlation'


if __name__ == "__main__":
    sport_data_paths = ["assets/nfl.csv", "assets/mlb.csv", "assets/nba.csv", "assets/nhl.csv"]
    pop_data_filelink = 'https://en.wikipedia.org/wiki/List_of_American_and_Canadian_cities_by_number_of_major_professional_sports_franchises'

    population_correlation = PopulationPerformanceRelationship(sport_data_paths, pop_data_filelink)
    print(population_correlation.metro_corrs['NHL'].data)