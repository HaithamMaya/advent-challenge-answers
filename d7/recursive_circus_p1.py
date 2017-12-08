file = open('input.txt', 'r')

parents = []
children = []


def split_row(row):
    return row.split(' -> ')


def strip_parent_garbage(parent):
    return parent.split(' (')[0]


def add_parent(p, c, parent):
    if parent not in c:
        p.append(parent)
    return p, c


def add_children(p, c, child_text):
    children_to_add = [child.rstrip() for child in child_text.split(', ')]
    c.extend(children_to_add)
    return p, c


def analyze_row(p, c, row):
    to_add = split_row(row)
    parent_to_add = strip_parent_garbage(to_add[0])
    p, c = add_parent(p, c, parent_to_add)
    if len(to_add) > 1:
        add_children(p, c, to_add[1])


for row in file:
    analyze_row(parents, children, row)

for child in children:
    parents = list(filter(child.__ne__, parents))

print("parents:")
print(parents)
print("children:")
print(children)
