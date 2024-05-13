# Of Stats and Sports

## Objective
We wish to conduct analysis on sports statistics to understand potential factors on team performance.   
As that is an incredibly general inquiry, with many avenues of investigation, we focus our question to: 

**Are sport teams' performance correlated with the population of the area it's based in?**  

We will constrain the performance to the most recent year the data provides, that is 2018.  
However we will broaden the scope to include multiple sports, analyzing the impact of each.  
### Approach
As smaller regions may be limited in hosting the full range of sporting teams, we focus on the Big 4: 
- NFL (data in [nfl.csv](assets/nfl.csv))
- MLB (data in [mlb.csv](assets/mlb.csv))
- NBA (data in [nba.csv](assets/nba.csv)) 
- NHL (data in [nhl.csv](assets/nhl.csv))  

However we may then have the inverse problem: Larger regions may have many teams of the same sport.  
If so, we will take the average across the teams of a single sport to represent that sport for the region.

We will define 'performance' as Win/Loss ratio = $\frac{number \ of \ wins}{number \ of \ wins \  + \ number \ of \ losses}$  

'Correlation' will be defined by `pearsonr` (as calculated by Scipy's [Pearson R class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html))  

Since metropolitan regions vary in names (e.g. 'New York Metropolitan', 'Greater New York', 'NYC Metro Area', etc),  
for this project we will use the data source names as the 'official' region name of a given sports team.  
Thus, Oakland Raiders will be mapped to the given region, 'San Francisco Bay Area' and not 'Oakland Metro'.

## Dataset
Sourced from wikipedia on major sports teams according to their metropolitan regions (see [wikipedia_data.html](assets/wikipedia_data.html)).  
We first had to preprocessed both this `html` as well as the `csv` data before conducting analysis.  
Both `html` and `csv` files were courtesy of Coursera Machine Learning Module at University of Michigan.
