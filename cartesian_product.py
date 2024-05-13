import pandas as pd

def get_combinations_of(set_list):
    combination_list, i = [], 0
    while i < len(set_list):
        j = i + 1
        while j < len(set_list):
            combination_list.append((set_list[i], set_list[j]))
            j += 1
        i += 1
    return combination_list


## Note, each combinations of each elem is contained in its own list, so len(output list) == len(input list)
def get_permutations_of(set_list):
    elem_product = lambda x: [(x, other_elem) for other_elem in set_list]
    return [elem_product(elem) for elem in set_list]


def permutation_to_combo(permutation, combo_dic): 
    if permutation[0] == permutation[1]: return 1
    elif permutation in combo_dic: return combo_dic[permutation]
    else: return combo_dic[(permutation[1], permutation[0])]


def combos_in_cartesian(values_by_combo):
    combinations = list(values_by_combo.keys())
    cartesian_set = list(set(sum(combinations, ())))
    df = pd.DataFrame(get_permutations_of(cartesian_set), index=cartesian_set, columns=cartesian_set)
    return df.map(lambda x: permutation_to_combo(x, values_by_combo))


if __name__ == "__main__":
    combo_vals = {('NHL', 'NBA'):1, ('NHL', 'NFL'):2, ('NHL', 'MLB'):3, ('NBA', 'NFL'):4, ('NBA', 'MLB'):5, ('NFL', 'MLB'):6}
    print(combos_in_cartesian(combo_vals))

