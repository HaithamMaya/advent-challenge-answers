from collections import Counter


class Program():
    name = None
    weight = None
    parent = None
    cum_weight = None

    def __init__(self, name, weight, parent):
        self.name = name
        self.weight = weight
        self.parent = parent

    def get_full_weight(self, programs):
        weight_sum = self.weight
        for program in programs:
            if program.parent == self.name:
                weight_sum += program.get_full_weight(programs)
        return weight_sum

    def self_with_cum_weight(self, programs):
        self.cum_weight = self.get_full_weight(programs)
        return self

    def get_children(self, programs):
        return [child for child in programs if child.parent == self.name]


def split_row(row):
    return row.split(' -> ')


def strip_parent_info(parent):
    parent_name, parent_weight = parent.split(' (')
    parent_weight = int(parent_weight.split(')')[0])
    return parent_name, parent_weight


parent_programs = []
children_programs = []
file = open('input.txt', 'r')

for row in file:
    to_add = split_row(row)
    parent_name, parent_weight = strip_parent_info(to_add[0])
    index, parent_object = next(
        ((i, item) for i, item in enumerate(children_programs) if item.name == parent_name),
        (-1, None)
    )
    if index != -1:
        parent_object.weight = parent_weight
        children_programs[index] = parent_object
    else:
        parent_programs.append(Program(parent_name, parent_weight, None))
    if len(to_add) > 1:
        for child in to_add[1].split(', '):
            child = child.rstrip()
            child_obj = next((obj for obj in parent_programs if obj.name == child), -1)
            if child_obj == -1:
                child_obj = Program(child, None, parent_name)
            else:
                child_obj.parent = parent_name
                parent_programs = [program for program in parent_programs if program.name != child]
            children_programs.append(child_obj)


children_programs = [child.self_with_cum_weight(children_programs) for child in children_programs]


def find_odd_ball(odd_ball, odd_ball_diff, prev_answer):
    if odd_ball is None:
        return (odd_ball_diff, prev_answer)
    children = odd_ball.get_children(children_programs)
    print('odd ball: %s, cum_weight: %s' % (odd_ball.name, odd_ball.cum_weight,))
    print('children count: %s' % str(len(children)))
    if len(children) == 0:
        return odd_ball
    elif len(children) == 1:
        return children[0]
    counts = Counter([child.cum_weight for child in children])
    print(counts.items())
    print([(child.weight, child.cum_weight) for child in children])
    if (len(counts.items()) <= 1) or not any(cum for cum, num in counts.items() if num > 1):
        print('prev answer is it!')
        return find_odd_ball(None, odd_ball, odd_ball_diff)
    odd_sum = next(cum for cum, num in counts.items() if num == 1)
    odd_sum_diff = next(cum for cum, num in counts.items() if num != 1) - odd_sum
    return find_odd_ball(next(child for child in children if child.cum_weight == odd_sum), odd_sum_diff, odd_ball)


odd_child, diff = find_odd_ball(parent_programs[0], None, None)
print(odd_child.name, odd_child.weight, odd_child.cum_weight, diff)
print('ANSWER = %s' % str(odd_child.weight + diff))