import pandas as pd

## Not used for any function in this module, but as a helper function for SportsCorrelations class
def get_combinations_of(set_list):  # Extracting only pairs regardless of order
    combination_list, i = [], 0  # Defining 1st pair element tracker variable
    while i < len(set_list):  
        j = i + 1  # Defining 2nd pair element tracker that always tracks on elements i hasn't been paired with earlier
        while j < len(set_list):  # Iterates over all potential pairs with that i 
            combination_list.append((set_list[i], set_list[j]))  
            j += 1
        i += 1
    return combination_list


## All permutations of each set element has its own list to make passing into DataFrame below easier
def get_permutations_of(set_list):
    get_permutation_list_of = lambda elem: [(elem, other_elem) for other_elem in set_list]
    return [get_permutation_list_of(elem) for elem in set_list]

## Helper function that returns the corresponding combination value for a single permutation
def permutation_to_combo(permutation, combo_dic): 
    if permutation[0] == permutation[1]: return 1  # By correlation, the permutation pair of itself has coeff = 1
    elif permutation in combo_dic: return combo_dic[permutation]  # when permutation order matches combination order
    else: return combo_dic[(permutation[1], permutation[0])]  # if not, switch order to match with its combination

## Expresses values of combinations in matrix form of pairwise permutations
def combos_in_cartesian(values_by_combo):
    combinations = list(values_by_combo.keys())
    cartesian_set = list(set(sum(combinations, ())))  # Flattens list of combinations to list of elements to take unique set on
    # Create a cartesian product matrix populated element-wise by all the pairwise permutations of the combination set
    df = pd.DataFrame(get_permutations_of(cartesian_set), index=cartesian_set, columns=cartesian_set)
    return df.map(lambda permutation: permutation_to_combo(permutation, values_by_combo))  # combination values for all elements


if __name__ == "__main__":
    combo_vals = {('NHL', 'NBA'):1, ('NHL', 'NFL'):2, ('NHL', 'MLB'):3, ('NBA', 'NFL'):4, ('NBA', 'MLB'):5, ('NFL', 'MLB'):6}
    print(combos_in_cartesian(combo_vals))

