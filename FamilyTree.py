import sys

class Person:
    #Constructor
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents
        self.children = []
        self.spouses = []

    #Compares two person objects and determines whether they are equal
    def __eq__(self, other):
        return self.name == other.name

    
    def __hash__(self):
        return hash(self.name)

    #Returns string (name) of the person object
    def __str__(self):
        return self.name


# Dictionary to store family tree
family_tree = dict()


def add_person(person):
    if person.name not in family_tree:
        family_tree[person.name] = person
    return family_tree[person.name]


def get_person(name):
    if name in family_tree:
        return family_tree[name]


def get_all_people():
    return list(family_tree.keys())


def get_parents(name):
    person = get_person(name)
    if person:
        return person.parents
    else:
        return []


def get_children(name):
    person = get_person(name)
    if person:
        return person.children
    else:
        return []


def get_spouses(name):
    person = get_person(name)
    if person:
        return person.spouses
    else:
        return []


def get_siblings(name):
    person = get_person(name)
    siblings = []

    if person and person.parents:
        parent1 = get_person(person.parents[0])
        parent_1_children = []
        if parent1:
            parent_1_children = parent1.children

        parent2 = get_person(person.parents[1])
        parent_2_children = []
        if parent2:
            parent_2_children = parent2.children

        siblings = set(parent_1_children).intersection(parent_2_children)

    return siblings


def get_ancestors_internal(name, ancestor_list):
    parents = get_parents(name)

    # Adam & Eve generation
    if not parents:
        ancestor_list.append(name)
    else:
        ancestor_list.extend(parents)
        for parent in parents:
            get_ancestors_internal(parent, ancestor_list)


def get_ancestors(name):
    ancestor_list = []
    get_ancestors_internal(name, ancestor_list)
    return list(set(ancestor_list))

"""
Descendants methods
"""
def get_descendants_internal(name, descendant_list):
    children = get_children(name)
    if not children:
        descendant_list.append(name)
    else:
        descendant_list.extend(children)
        for child in children:
            get_descendants_internal(child, descendant_list)


def get_descendants(name):
    descendant_list = []
    get_descendants_internal(name, descendant_list)
    return list(set(descendant_list))


def get_relatives(name):
    relatives = []
    ancestors = get_ancestors(name)
    relatives.extend(ancestors)
    for ancestor in ancestors:
        relatives.extend(get_descendants(ancestor))

    return list(set(relatives))


def descendant_tree_internal(name, level, desc_list):
    if level == 0:
        desc_list.append(name)
    else:
        children = get_children(name)
        #desc_list.extend(children)
        if children:
            for child in children:
                descendant_tree_internal(child, level - 1, desc_list)


def descendant_tree(name, level):
    descendant_list = []
    descendant_tree_internal(name, level, descendant_list)
    return list(set(descendant_list))


def ancestor_tree(name, level):
    ancestor_list = []
    ancestor_tree_internal(name, level, ancestor_list)
    return list(set(ancestor_list))


def ancestor_tree_internal(name, level, ancestor_list):
    if level == 0:
        ancestor_list.append(name)
    else:
        parents = get_parents(name)
        #ancestor_list.extend(parents)
        if parents:
            for parent in parents:
                ancestor_tree_internal(parent, level - 1, ancestor_list)


def get_cousins(name, degree, removal):
    cousins = []

    # A first degree cousin is 2 levels up the ancestor tree and 2 levels
    # down the descendant tree (plus 1 for each level of removal)
    up = degree + 1
    down = up + removal
    ancestors = ancestor_tree(name, up)
    for person in ancestors:
        cousins.extend(descendant_tree(person, down))
    return list(set(cousins) - set(get_children(name)))


def get_unrelated(name):
    unrelated = get_all_people()
    unrelated = list(set(unrelated) - set(get_relatives(name)))
    unrelated = list(set(unrelated) - set(get_descendants(name)))
    unrelated = list(set(unrelated) - set(get_siblings(name)))
    unrelated = list(set(unrelated) - set(get_spouses(name)))
    if name in unrelated:
        unrelated.remove(name)
    return unrelated


def processE(input):
    parent1_name = input[1]
    parent2_name = input[2]

    parent1 = add_person(Person(parent1_name, []))
    parent2 = add_person(Person(parent2_name, []))

    if parent2.name not in parent1.spouses:
        parent1.spouses.append(parent2.name)
    if parent1.name not in parent2.spouses:
        parent2.spouses.append(parent1.name)

    # Check if this event includes a child
    if len(input) > 3:
        child_name = input[3]
        add_person(Person(child_name, [parent1.name, parent2.name]))
        parent1.children.append(child_name)
        parent2.children.append(child_name)


def print_sorted(unsorted_list):
    if unsorted_list:
        for x in sorted(unsorted_list):
            print(x)


def processR(input_array):
    person1_name = input_array[1]
    person2_name = input_array[2]

    if not person1_name or not person2_name:
        print("unrelated")

    if person2_name in get_spouses(person1_name):
        print("spouse")
    elif person1_name in get_parents(person2_name) or person2_name in get_parents(person1_name):
        print("parent")
    elif person2_name in get_siblings(person1_name):
        print("sibling")
    elif person1_name in get_ancestors(person2_name) or person2_name in get_ancestors(person1_name):
        print("ancestor")
    elif list(set(get_ancestors(person1_name)) & set(get_ancestors(person2_name))):
        print("relative")
    else:
        print("unrelated")

"""
Returns yes or no depending on whether the input statement is factually correct
"""
def processX(input_array):
    person1_name = input_array[1]
    person2_name = input_array[3]
    relation = input_array[2]

    if relation == "sibling":
        if person1_name in get_siblings(person2_name):
            print("Yes")
        else:
            print("No")
    elif relation == "relative":
        if list(set(get_ancestors(person1_name)) & set(get_ancestors(person2_name))):
            print("Yes")
        else:
            print("No")
    elif relation == "spouse":
        if person2_name in get_spouses(person1_name):
            print("Yes")
        else:
            print("No")
    elif relation == "parent":
        if person1_name in get_parents(person2_name):
            print("Yes")
        else:
            print("No")
    elif relation == "cousin":
        person2_name = input_array[5]
        degree = int(input_array[3])
        removal = int(input_array[4])
        if person1_name in get_cousins(person2_name, degree, removal):
            print("Yes")
        else:
            print("No")
    elif relation == "ancestor":
        if person1_name in get_ancestors(person2_name):
            print("Yes")
        else:
            print("No")
    elif relation == "unrelated":
        if person1_name in get_unrelated(person2_name):
            print("Yes")
        else:
            print("No")

"""
Method prints out list of relatives given relation to a Person
"""
def processW(input_array):
    relation = input_array[1]
    name = input_array[2]

    if relation == "sibling":
        print_sorted(get_siblings(name))
    elif relation == "relative":
        print_sorted(get_relatives(name))
    elif relation == "spouse":
        print_sorted(get_spouses(name))
    elif relation == "parent":
        print_sorted(get_parents(name))
    elif relation == "ancestor":
        print_sorted(get_ancestors(name))
    elif relation == "unrelated":
        print_sorted(get_unrelated(name))
    elif relation == "cousin":
        name = input_array[4]
        degree = int(input_array[2])
        removal = int(input_array[3])
        print_sorted(get_cousins(name, degree, removal))

"""
Handles user interface
"""
def handle_line(raw_line):
    if raw_line:
        input_array = raw_line.split()
        if input_array[0] == 'E':
            processE(input_array)
        elif input_array[0] == 'R':
            print(raw_line, end='')
            processR(input_array)
            print()
        elif input_array[0] == 'X':
            print(raw_line, end='')
            processX(input_array)
            print()
        elif input_array[0] == 'W':
            print(raw_line, end='')
            processW(input_array)
            print()


for line in sys.stdin:
    handle_line(line)

# Reset family tree hashtable
family_tree = dict()
