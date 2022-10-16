from copy import deepcopy

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def print_puzzle(puzzle):
    for line in puzzle:
        print(line)
    print('\n')

def get_position(puzzle, element):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == element:
                return (i, j)

def distance_heuristics(state, final_state):
    result = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            [i2, j2] = get_position(final_state, state[i][j])
            result += manhattan_distance(j, i, j2, i2)
    return result

def get_possible_movements(puzzle):
    [blank_space_i, blank_space_j] = get_position(puzzle, 0)
    movements = []

    # up
    if (blank_space_i - 1 >= 0):
        new_state = deepcopy(puzzle)
        aux = new_state[blank_space_i - 1][blank_space_j]
        new_state[blank_space_i - 1][blank_space_j] = 0
        new_state[blank_space_i][blank_space_j] = aux
        movements.append(new_state)

    # down
    if (blank_space_i + 1 < 3):
        new_state = deepcopy(puzzle)
        aux = new_state[blank_space_i + 1][blank_space_j]
        new_state[blank_space_i + 1][blank_space_j] = 0
        new_state[blank_space_i][blank_space_j] = aux
        movements.append(new_state)

    # left
    if (blank_space_j - 1 >= 0):
        new_state = deepcopy(puzzle)
        aux = new_state[blank_space_i][blank_space_j - 1]
        new_state[blank_space_i][blank_space_j - 1] = 0
        new_state[blank_space_i][blank_space_j] = aux
        movements.append(new_state)

    # right
    if (blank_space_j + 1 < 3):
        new_state = deepcopy(puzzle)
        aux = new_state[blank_space_i][blank_space_j + 1]
        new_state[blank_space_i][blank_space_j + 1] = 0
        new_state[blank_space_i][blank_space_j] = aux
        movements.append(new_state)
    
    return movements

def get_most_promissor_node(nodes):
    most_promissor_node = nodes[0]
    for node in nodes:
        most_promissor_node_heuristics = most_promissor_node["distance"] + most_promissor_node["level"]
        node_heuristics = node["distance"] + node["level"]
        if node_heuristics < most_promissor_node_heuristics:
            most_promissor_node = node
    return most_promissor_node

def get_node_path(states_by_level, node):
    level = node["level"]

    aux = node["puzzle_state"]
    path = [(aux, level)]
    possible_movements = get_possible_movements(aux)
    for i in reversed(range(level)):
        found = False
        for state in states_by_level[i]:
            if state in possible_movements:
                found = True
                path.append((state, i))
                aux = state
                possible_movements = get_possible_movements(aux)
        if not found:
            raise Exception("did not found father for", aux)
    return path

def print_node_path(node_path):
    for step in reversed(node_path):
        print("\npasso", step[1])
        print_puzzle(step[0])

def search_a_star(initial, final):
    visited = []
    node = {
        "puzzle_state": initial,
        "level": 0,
        "distance": distance_heuristics(initial, final)
    }
    to_visit = [node]
    states_by_level = [[]] * 10000
    states_by_level[0] = [initial]
    generated_nodes = 1

    while(len(to_visit) > 0):
        if len(to_visit) == 0:
            raise Exception("problema sem solucao")

        node = get_most_promissor_node(to_visit)
        to_visit.remove(node)
        visited.append(node["puzzle_state"])

        if node["puzzle_state"] == final:
            print_node_path(get_node_path(states_by_level, node))
            print("generated nodes: ", generated_nodes)
            return node
        
        possible_movements = get_possible_movements(node["puzzle_state"])
        level = node["level"] + 1
        states_at_this_level = []
        for movement in possible_movements:
            if movement not in visited:
                movement_node = {
                    "puzzle_state": movement,
                    "level": level,
                    "distance": distance_heuristics(movement, final)
                }
                generated_nodes += 1
                to_visit.append(movement_node)
                states_at_this_level.append(movement)

        states_by_level[level] = states_by_level[level] + states_at_this_level



def main():
    # initial_state = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
    initial_state = [[3, 6, 1], [4, 8, 0], [5, 7, 2]]
    final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print("final node", search_a_star(initial_state, final_state))

main()