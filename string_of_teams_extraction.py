## REGEX MODULE FOR SEPARATING SPORT TEAM NAMES FROM A SINGLE STRING OF WORDS WITH UNCERTAIN NUMBER OF SPORT TEAM NAMES
## These functions were moved into separate file to declutter application classes from their primary methods

## Helper function to return the passed string list with the presumed words of the unnamed team removed
def remove_unnamed_team_words(words_sublist, no_words_to_remove):
    for _ in range(no_words_to_remove): words_sublist.pop()  # passed list is such that the unnamed team is at the end 
    return words_sublist

## Helper function checking if the uncertain word is the location of the unnamed team or another team
def handle_potential_team_name(words_sublist):
    if words_sublist[-4][-1] in ['Los', 'Las']: return remove_unnamed_team_words(words_sublist, 4)
    else: return remove_unnamed_team_words(words_sublist, 3)  # More likely 1-word [place] than 2-words where 1st word ends on 's'

## Helper function with conditional logic to handle how to remove unnamed team without dropping named team words
def drop_unnamed_team(words_sublist):
    # Since Wiki name convention calls unnamed teams '[place][name] NHL team', we can safely drop up to 3 words
    if len(words_sublist) < 4: return remove_unnamed_team_words(words_sublist, len(words_sublist))
    # Helper function to handle presence of 4th word that ends with 's'
    elif words_sublist[-4][-1] == 's': return handle_potential_team_name(words_sublist) 
    else: return remove_unnamed_team_words(words_sublist, 4) # More likely a 2-worded [place][name] than a team not ending on 's'


## Splits a single string of teams into list of teams
def get_teams_from_string(string):  
    words = string.split(' ')
    if len(words) > 1:  # Case where we need to identify team names 
        teams = []
        while words != []:  # Iterating through by removal
            if 'team' in set(words):  # Unnamed teams have 'team' in their Wiki name 
                team_idx = words.index('team')  # Assumes a metro doesn't have 2 unnamed teams 
                words_sublist_before = drop_unnamed_team(words[:team_idx+1])  # Its presence messes extraction logic below
                words_sublist_after = words[team_idx+1:]  # Not splitting words before & after unnamed team also messes below
                return (get_teams_from_string(' '.join(words_sublist_before)) +  # Recursively extract from each sublist
                        get_teams_from_string(' '.join(words_sublist_after)))  # Returns as we don't need to be in the while loop
            elif words[0][-1] == 's': teams.append(words.pop(0))  # Most teams end on 's', most 1st word of multi-word teams don't
            else: # Have to determine with next word to see if team name includes next word too (we assume no 3-word names)
                if len(words) == 1: teams.append(words.pop(0))  # Lack of next word is trivial
                # 2-worded team name ending in 's' more likely than a name not ending in 's', so we combine given probabilities
                elif words[1][-1] == 's': teams.append(' '.join([words.pop(0), words.pop(0)]))  
                else: teams.append(words.pop(0))  # A 1 word name not ending in 's' more likely than 2 words
        return teams
    else: return words


## Calls a helper function to help check which metro team name the sport data team matches with if any
def match_teams(metro_team_string, name_from_sport_data):
    metro_teams = get_teams_from_string(metro_team_string)  
    metro_teams = list(filter(None, metro_teams))  # Clears [""], ["", ""] extraction outputs from get_teams_from_string
    for metro_team in metro_teams: 
        if metro_team in name_from_sport_data: return metro_team  # Metro team names don't have city/state so used as substring


if __name__ == "__main__":
    print(get_teams_from_string('Rangers Islanders Devils'))