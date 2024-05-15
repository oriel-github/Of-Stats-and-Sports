import pandas as pd
from analysis import SportCorrelations as Corr

## Loads all wiki tables from URL page into list, so formatting assumes current wiki table column layout
## Specifically Metro name at col 0, population at 3, Big 4 at 5-8
## If population data isn't the first table e.g. If 3rd table that appears on the page, specify pop_data_table_no = 3
def get_population_data(population_data_filename, pop_data_table_no = 1):
    return pd.read_html(population_data_filename)[pop_data_table_no - 1].iloc[:-1,[0,3,5,6,7,8]].set_index('Metropolitan area')

def get_sport_list(formatted_population_data):
    return list(formatted_population_data.columns[1:])


class PopulationPerformanceRelationship(Corr):

    ## Sport name in sports_list must be same format as it appears in population_data_filename data
    ## e.g. if population data has 'N.H.L.' as column name, then its sport_name needs to be 'N.H.L.' 
    ## sports_list and sport_data_filename_list need to correspond, e.g. ['NHL', 'NBA'] requires ['nhl.csv', 'nba.csv'] order
    def __init__(self, sport_data_filename_list, population_data_filename, pop_data_table_no = 1):
        self.population_data = get_population_data(population_data_filename, pop_data_table_no)
        sports = get_sport_list(self.population_data)
        super().__init__(self.population_data, sports, sport_data_filename_list)
        self.get_pair_corrs()
        self.get_pair_corr_tests()
        self.get_pair_corr_pvals()

    def __str__(self):
        results = self.get_pval_matrix().map(lambda x: self.classify_pval(x))
        return f'Pairwise Sport Performance Results:\n {results}'
    
    def classify_pval(self, p_val_matrix_element):
        if p_val_matrix_element < 0.05: return 'Different'
        else: return 'Similar'





if __name__ == "__main__":
    sport_data_paths = ["assets/nfl.csv", "assets/mlb.csv", "assets/nba.csv", "assets/nhl.csv"]
    pop_data_filelink = 'https://en.wikipedia.org/wiki/List_of_American_and_Canadian_cities_by_number_of_major_professional_sports_franchises'

    analysis = PopulationPerformanceRelationship(sport_data_paths, pop_data_filelink)
    print(analysis)