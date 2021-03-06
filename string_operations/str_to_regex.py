# This package has the function which does the following things:
#    1. Generate a common regular expression for list of strings
#    2. generate dictionary tree from a string or list of strings
#    3. Convert dictionary tree to regular expression
# This can used to match the given the string present in the list of string


# import re


def str2dict_tree(string, dct=None):
    """
    ip : "This"
    op : {'T': {'h': {'a': {'t': {}}}}}
    """
    if dct is None:
        dct = {}
    if (len(string) > 0):
        dct[string[0]] = str2dict_tree(string[1:], dct.get(string[0]))
    return dct


def simplify_tree(dict_tree, dct={}, key_str=''):
    """
    ip: {'T': {'h': {'a': {'t': {}}, 'i': {'s': {}}}}}
    op: {'Th': {'at': {}, 'is': {}}}
    """
    # Get key in the dict_tree dictionary
    keys = list(dict_tree.keys())
    # Return the dict_tree object of there is no more child/keys present
    # in the dictionary
    if (len(keys) == 0):
        dct[key_str] = dict_tree
        return dct
    # Check if there is only one key present in te dictionary
    # If yes : create keystr using the prevuous key_str value and
    # recursively use the function to get the same result for child object
    # of the key
    elif (len(keys) == 1):
        key_str = key_str + keys[0]
        return simplify_tree(dict_tree[keys[0]], dct, key_str)
    # If the object has multiple keys / object has multiple child objects :
    #   1. Iterate throug the childs
    #   2. create list of simplify trees for child objects
    #   3. merge all the simplify trees in to one object/dictionary
    #   4. assign the final dict and return the dct
    else:
        child = {}
        for key in keys:
            child.update(simplify_tree(dict_tree[key], {}, key))
        dct[key_str] = child
        return dct


def str_list2dict_tree(str_list):
    """
    Iterate through list of string and create a dictionary tree from the list
    ip: ["That", "This"]
    op: {'T': {'h': {'a': {'t': {}}, 'i': {'s': {}}}}}
    """
    dict_tree = {}
    for element in str_list:
        dict_tree = str2dict_tree(element, dict_tree)
    return dict_tree


def dict_tree2reg_exp(dict_tree, expr=''):
    """
    convert dict_tree to regular expression
    Example1 :
        ip: {'Th': {'at': {}, 'is': {}}}
        op: '(?:Th(?:is|at))'
    Example2 :
        ip: {'T': {'h': {'a': {'t': {}}, 'i': {'s': {}}}}}
        op: '(?:T(?:h(?:i(?:s)|a(?:t))))'
    """
    keys = list(dict_tree.keys())
    if (len(keys) == 0):
        return ""
    elif (len(keys) == 1):
        return "(?:" + keys[0] + dict_tree2reg_exp(dict_tree[keys[0]]) + ')'
    else:
        expr_list = []
        for key in keys:
            expr_list.append(
                key + dict_tree2reg_exp(dict_tree[key])
            )
        return "(?:" + '|'.join(expr_list) + ")"
    return expr


if __name__ == "__main__":
    str_list = ["This", "That"]
    dict_tree = str_list2dict_tree(str_list)
    print(str_list, "  ----->  ", dict_tree)
    condensed_dict_tree = simplify_tree(dict_tree)
    print(dict_tree, "  ----->  ", condensed_dict_tree)
    print(condensed_dict_tree, "  ----->  ",
          dict_tree2reg_exp(condensed_dict_tree))
    print(dict_tree, "  ----->  ", dict_tree2reg_exp(dict_tree))
