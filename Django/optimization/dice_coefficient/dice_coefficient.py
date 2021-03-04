import re

SEPARATOR_PATTERN = "[^a-zA-Z]"

WORD_SEPARATOR = ";"

GROUP_SIZE = 4


def dice_coefficient(string_searched, str_b):
    """dice coefficient 2nt/(na + nb)."""

    string_searched = string_searched.lower()

    str_b = str_b.lower()

    separator_pattern = re.compile(SEPARATOR_PATTERN)

    group_size = GROUP_SIZE if (len(string_searched) >= GROUP_SIZE) else len(string_searched)

    list_char_a = filter_list_char(string_searched, separator_pattern, group_size)
    list_str_grp_a = generate_list_of_char_group(list_char_a, group_size)

    list_char_b = filter_list_char(str_b, separator_pattern, group_size)
    list_str_grp_b = generate_list_of_char_group(list_char_b, group_size)

    cpt_same_grp = 0

    for elem in list_str_grp_a:
        if elem in list_str_grp_b:
            cpt_same_grp += 1

    nominator = 2 * cpt_same_grp
    denominator = len(string_searched + str_b)
    coefficient = nominator / denominator
    return coefficient


def generate_list_of_char_group(list_of_str_grp, group_size):
    list_of_str = []
    for list_of_char in list_of_str_grp:
        for i in range(0, len(list_of_char), group_size):
            if i + group_size <= len(list_of_char):
                upper_limit = i + group_size
                char_list_by_group = list_of_char[i:upper_limit]
                str = ''.join(char_list_by_group)
                list_of_str.append(str)

    return list_of_str


def filter_list_char(my_string, separator_pattern, group_size):
    new_char_list = []
    my_string = re.split(separator_pattern, my_string)
    for splitted_group in my_string:
        if len(splitted_group) >= group_size:
            new_char_list.append(list(splitted_group))

    return new_char_list
