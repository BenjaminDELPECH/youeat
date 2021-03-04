import re


cdef str SEPARATOR_PATTERN = "[^a-zA-Z]"

cdef str WORD_SEPARATOR = ";"

cdef int GROUP_SIZE = 3

cpdef float dice_coefficient_cpdef(str string_searched, str str_b):
    return dice_coefficient_cdef(string_searched, str_b)

cdef float dice_coefficient_cdef(str string_searched, str str_b):
    """dice coefficient 2nt/(na + nb)."""

    # cdef int group_size, cpt_same_grp
    # cdef double group_size, cpt_same_grp, nominator, denominator, coefficient
    # cdef char *list_char_a, *list_char_b
    # cdef char ** list_str_grp_a, ** list_str_grp_b

    string_searched = string_searched.lower()

    str_b = str_b.lower()

    # cdef str separator_pattern
    separator_pattern = re.compile(SEPARATOR_PATTERN)

    group_size = GROUP_SIZE if (len(string_searched) > 2) else len(string_searched)

    list_char_a = generate_list_of_char_list(string_searched, separator_pattern, group_size)
    list_str_grp_a = generate_list_of_str_grp(list_char_a, group_size)

    list_char_b = generate_list_of_char_list(str_b, separator_pattern, group_size)
    list_str_grp_b = generate_list_of_str_grp(list_char_b, group_size)

    cpt_same_grp = 0

    cdef str elem

    for elem in list_str_grp_a:
        if elem in list_str_grp_b:
            cpt_same_grp += 1

    nominator = 2 * cpt_same_grp
    denominator = len(string_searched) + len(str_b)
    coefficient = nominator / denominator
    return coefficient

cdef generate_list_of_str_grp(list_of_str_grp, group_size):
    list_of_str = []
    cdef int i
    cdef char* list_of_chat
    for list_of_char in list_of_str_grp:
        for i in range(0, len(list_of_char), group_size):
            if i + group_size <= len(list_of_char):
                upper_limit = i + group_size
                char_list_by_group = list_of_char[i:upper_limit]
                str = ''.join(char_list_by_group)
                list_of_str.append(str)

    return list_of_str

cdef generate_list_of_char_list(my_string, separator_pattern, group_size):
    grp_char_list = []
    my_string = re.split(separator_pattern, my_string)
    for splitted_group in my_string:
        if len(splitted_group) >= group_size:
            grp_char_list.append(list(splitted_group))

    return grp_char_list
