def remove_unnamed_team_words(words_sublist, no_words_to_remove):
    for _ in range(no_words_to_remove): words_sublist.pop() ## Exclude words that will mess up function, e.g. '[place] NHL team'
    return words_sublist

def handle_potential_team_name(words_sublist):
    if words_sublist[-4][-1] not in ['Los', 'Las']: return remove_unnamed_team_words(words_sublist, 3)
    else: return remove_unnamed_team_words(words_sublist, 4) 

def handle_unnamed_team(words_sublist):
    if len(words_sublist) < 4: return remove_unnamed_team_words(words_sublist, len(words_sublist))
    elif words_sublist[-4][-1] == 's': return handle_potential_team_name(words_sublist) 
    else: return remove_unnamed_team_words(words_sublist, 4)

def get_teams_from_string(string): ## Splits all the individual team names from the single Metro sport team string
    words = string.split(' ')
    if len(words) > 1:
        teams = []
        while words != []:
            # Wiki name convention calls unnamed teams '[place] NHL team'
            if 'team' in set(words): 
                team_idx = words.index('team')  # Assumes a metro doesn't have 2 unnamed teams 
                words_sublist_with_team_dropped = handle_unnamed_team(words[:team_idx+1])
                words_sublist_after_team_idx = words[team_idx+1:]
                return (get_teams_from_string(' '.join(words_sublist_with_team_dropped)) +
                        get_teams_from_string(' '.join(words_sublist_after_team_idx)))

            ## Assumes single words ending in s must be team name, and first word of multi-word name never end in s
            elif words[0][-1] == 's': teams.append(words.pop(0))
            else: 
                if len(words) == 1: teams.append(words.pop(0))
                else: teams.append(' '.join([words.pop(0), words.pop(0)])) ## assumes multi-word names are only 2 words long
        return teams
    else: return words

def match_teams(metro_team_string, name_from_sport_data):
    metro_teams = get_teams_from_string(metro_team_string)
    metro_teams = list(filter(None, metro_teams))
    for metro_team in metro_teams: 
        if metro_team in name_from_sport_data: return metro_team  # Metro team names don't have city/state so used as substring


if __name__ == "__main__":
    print(get_teams_from_string('Rangers Islanders Devils'))