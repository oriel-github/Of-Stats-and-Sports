# Of Stats and Sports

## Objective
We wish to conduct analysis on sports statistics to understand potential factors on team performance.   
As that is an incredibly general inquiry, with many avenues of investigation, we focus our questions to: 

**Are sport teams' performance correlated with the population of the area it's based in?**  
**Is the performance distribution across the population for one sport the same across all sports?**  
**If so, by what confidence do we know? And if not all the same, for which sports does that apply to?**  

### Approach
As smaller regions may be limited in hosting the full range of sporting teams, we focus on the Big 4: 
- NFL (2018 data in [nfl.csv](assets/nfl.csv))
- MLB (2018 data in [mlb.csv](assets/mlb.csv))
- NBA (2018 data in [nba.csv](assets/nba.csv)) 
- NHL (2018 data in [nhl.csv](assets/nhl.csv))  

However we may then have the inverse problem: Larger regions may have many teams of the same sport.  
If so, we will take the average across the teams of a single sport to represent that sport for the region.

We will define 'performance' as Win/Loss ratio = $\frac{number \ of \ wins}{number \ of \ wins \  + \ number \ of \ losses}$  

'Correlation' will be defined by `pearsonr` (as calculated by Scipy's [Pearson R class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html))  

'The area it's based in' will be defined by the data source, so may be mapped to metro area rather than just the city.  
If so, then 'the population' we want to find correlation with is defined as the population of the metro area, not just city.  

Since metropolitan regions vary in names (e.g. 'New York Metropolitan', 'Greater New York', 'NYC Metro Area', etc),  
for this project we will use the data source (Wikipedia) names as the 'official' region name of a given sports team.  
Thus, Oakland Raiders will be mapped to the given region, 'San Francisco Bay Area' and not 'Oakland Metro'.  

'Is the performance distribution ... **the same** across all sports' will be defined by t-tests at 95% Confidence.  
Meaning to say if the mean performance data of a sport has a less than 5% chance of being what it is,  
assuming that it shares 'the same' performance distribution of another sport as defined by their performance data,    
then we reject the idea that the 2 sports have 'the same' performance behavior across the population.  

t-Tests and their p-values will be defined by `ttest_rel` (as calculated by Scipy's [ttest_rel class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mstats.ttest_rel.html#scipy.stats.mstats.ttest_rel.html)).  


'... the same across **all** sports' means we will be examining all possible pairwise permutations of the Big 4.  
Technically that means 16, but 4 are trivial because team performance will always be pefectly correlated with itself.  
And also, order doesn't matter (e.g. NFL with NBA as opposed to NBA with NFL), so really we are looking 6 combinations.
However, class methods will also be built to allow the 16 pairwise correlation matrix output for easier visual comprehension.  
Moreover, the classification matrix will be set as the default class output, giving just the binary results of the p-values.  

Similarly for the population correlation class, where correlation and classification is shown in tabular form for the big 4.

## Dataset

We will constrain the performance dataset to just 1 year, as statistical relationships can vary over time as teams change.  
  
Data is sourced from wikipedia on major sports teams according to their metropolitan regions (see [wikipedia article source]('https://en.wikipedia.org/wiki/List_of_American_and_Canadian_cities_by_number_of_major_professional_sports_franchises')).  
Both the population `url` and the 2018 sport performance `csv` data files, are data raw, unprocessed.    
The `csv` files are attributed to the University of Michigan, found in their [Coursera Machine Learning Module](https://www.coursera.org/learn/python-machine-learning). 
