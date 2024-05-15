
## Wiki team naming convention excludes city/state name, so function assumes no location name
def get_teams_from_string(string): ## Splits all the individual team names from the single Metro sport team string
    words = string.split(' ')
    if len(words) > 1:
        teams = []
        while words != []:
            if words[0][-1] == 's':  
                ## Assumes single words ending in s must be team name, and first word of multi-word name never end in s
                teams.append(words.pop(0))
            elif 'team' in set(words): ## When team has no name, Wiki name convention calls it '[city/state] NHL team'
                team_idx = words.index('team')
                words.pop(team_idx)  ## Exclude words that will for sure mess up function, i.e. 'NHL team'
                words.pop(team_idx-1)  ## leaving [city/state] bc ensure if 1 or 2 words, 
            else: 
                if len(words) == 1: teams.append(words.pop(0))
                else: teams.append(' '.join([words.pop(0), words.pop(0)])) ## assumes multi-word names are only 2 words long
        return teams
    else: return words

def match_teams(metro_team_string, name_from_sport_data):
    for metro_team in get_teams_from_string(metro_team_string): 
        if metro_team in name_from_sport_data: return metro_team


if __name__ == "__main__":
    print(get_teams_from_string('Rangers Islanders Devils'))