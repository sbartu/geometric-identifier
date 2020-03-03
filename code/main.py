import fileinput
import os
import sys
from collections import OrderedDict
from math import sqrt
from shapes import *
from plot import *

input = {}
adj_list = {}
objects = []
all_loops = []
current_path = []
named_loops = {}
pruned_loops = []
line_count = 0

def main():

    args = sys.argv

    in_f = os.path.abspath(sys.argv[1])
    out_f = os.path.abspath(sys.argv[2])

    with open(in_f) as fp:
        lines = fp.readlines()
    
    for line in lines:
        parse_line(line)

    input_name = os.path.basename(sys.argv[1]).split('.')[0]

    loops = find_closed_loops()
    # test_print()
    interp_col = find_subsets()
    
    suffix = 'a'
    for interp in interp_col:
    
        identify_shapes(interp)
        fill_attributes()
        # print_objects()
        
        file_write(out_f + '/' + input_name + suffix + '.txt')
        
        setup_plot(objects, out_f + '/' + input_name + suffix + '.png')
        
        objects.clear()
        Shape.reset_n()
        suffix = chr(ord(suffix) + 1)


def file_write(filename):

    f = open(filename, 'w')
    
    for shape in objects:
        if shape.unions != '':
            f.write(shape.get_p_line() + '\n')
        if not shape.only_loop:
            f.write(shape.get_shape_line() + '\n')
        f.write(shape.get_pos_lines() + '\n')
        
    for shape in objects:
        for line in shape.hrel:
            f.write(line + '\n')
            
        for line in shape.vrel:
            f.write(line + '\n')
            
        for line in shape.crel:
            f.write(line + '\n')

    f.close()


def test_print():
    """Print For Debugging"""
    print('\nInput:')
    print_dict(input)

    print('\nAdjacency List:')
    print_dict(adj_list)
    print('\n')
    
    for loop in all_loops:
        print(loop)


def print_dict(dictionary):
    """Prints Input Dictionary Line by Line"""
    for k, v in dictionary.items():
        to_print =  str(k) + ' : ' + str(v)
        print(to_print)


def parse_line(line):
    global line_count
    """Parses Given Line Into The Adjacency List"""
    words = line.split()
    name = words[0]
    kind = words[2].split('(')[0]
    vertices = ((words[2].split('('))[1].split(')')[0]).split(',')

    key = (name, kind)

    input[key] = []

    u = (vertices[0], vertices[1])

    if kind == 'line':
        line_count += 1
        v = (vertices[2], vertices[3])

        if u not in adj_list:
            adj_list[u] = set()
        if v not in adj_list:
            adj_list[v] = set()
        adj_list[u].add(v)
        adj_list[v].add(u)

        input[key].append(u)
        input[key].append(v)

    elif len(vertices) == 3:
    
        objects.append(Shape(u, 'circle', u, key[0], float(vertices[2])))
        
    else:
        objects.append(Shape(tuple(u), 'dot', u, key[0], 0.2))


def find_closed_loops():
    """DFS the Adjacency List to Find Closed Loops"""

    loops = set()

    for key in adj_list:
        current_path.clear()
        dfs2(adj_list, key)
        


    valid = True

    while(valid):
        valid = clean_same_loops(all_loops)


def clean_same_loops(loops):
    """Clears Loops That Share at Least an Edge"""
    for loop_x in loops:
        for loop_y in loops:
            if loop_x == loop_y:
                continue
            if set(loop_x) == set(loop_y):
                loops.remove(loop_y)
                return True

    return False


def dfs2(graph, node, visited = None):
    
    added = False
    if not visited:
        visited = []
    
    if node not in visited:
        added = True
        visited.append(node)
        
        for next in graph[node]:
            dfs2(graph, next, visited)

    if visited[0] == node and len(visited) > 2:
        
        saved_path = visited.copy()
        saved_path.append(node)
        all_loops.append(saved_path)
    
    elif visited and added:

        del visited[-1]

    return visited


def dfs_sub(graph, node, visited = None, number = 0):
    
    added = False
    if not visited:
        visited = []
    
    if node not in visited and (all(nodes in graph[node] for nodes in visited) and visited is not None):
        added = True
        number += len(node) - 1
        visited.append(node)
        
        for next in graph[node]:
            dfs_sub(graph, next, visited, number)

    if number == line_count:

        saved_path = visited.copy()
        pruned_loops.append(saved_path)
    
    elif visited and added:

        number -= len(node) - 1
        del visited[-1]

    return visited    


def find_subsets():

    seen = []
    tuples = [tuple(i) for i in all_loops]
    subset_dict = dict()

    for loop_i in tuples:
        for loop_j in tuples:
            if loop_i not in subset_dict:
                subset_dict[loop_i] = []

            if loop_i == loop_j:
                continue

            if not share_line(loop_i, loop_j):
                subset_dict[loop_i].append(loop_j)

    for key in subset_dict:

        pruned_loops.clear()
        dfs_sub(subset_dict, key)
        interpret = pruned_loops.copy()

        for i in interpret:
            if set(i) not in seen:
                seen.append(set(i))

    return seen


def share_line(loop1, loop2):
    """Return True if Given 2 Loops Have a Common Line"""
    for i in range(1, len(loop1)):
        for j in range(1, len(loop2)):
            
            if set([loop1[i], loop1[i - 1]]) == set([loop2[j], loop2[j - 1]]):
                return True
    
    return False
    

def check_square_rect(loop):
    """Return the Shape of the Quadrilateral as Square, Rectangle or None"""
    listed = list(loop)
    i = 2
    
    dist = distance(listed[1], listed[0])
    x = listed[1][0]
    y = listed[1][1]

    while i < len(listed):

        dist_i = distance(listed[i], listed[i - 1])
        x_i = listed[i][0]
        y_i = listed[i][1]
        if x != x_i and y != y_i:
            return None
        if dist != dist_i:
            return 'rectangle'

        dist = dist_i
        x = x_i
        y = y_i
        i += 1

    return 'square'
    

def distance(p0, p1):
    """Squared Distance Between Two Vertices"""
    return ((int(p0[0]) - int(p1[0]))**2 + (int(p0[1]) - int(p1[1]))**2)


def center_of_mass(loop):
    """Center of Mass Calculation With Each Weight = 1"""
    x = 0
    y = 0
    i = 1
    
    while i < len(loop):
    
        x += int(loop[i][0])
        y += int(loop[i][1])
        i += 1
    
    total = int(len(loop)) - 1

    return (x / total, y / total)


def identify_shapes(loops):
    """Loop Through Closed Loops to Identify Their Shapes"""
    for loop in loops:
        if len(loop) == 4:
            objects.append(Shape(loop, 'triangle', center_of_mass(loop)))
        elif len(loop) == 5:
            objects.append(Shape(loop, check_square_rect(loop), center_of_mass(loop)))
        else:
            objects.append(Shape(loop, None, center_of_mass(loop)))


def fill_attributes():
    """Find Which Lines From the Initial Input Make Up This Loop and Locations"""
    for shape in objects:
        shape.find_unions(input)
        shape.find_location()
        
    for shape1 in objects:
        for shape2 in objects:

            if shape1 == shape2:
                continue

            if shape1.get_shape() != 'circle' and shape2.get_shape() != 'circle' and intersection_check(shape1, shape2):
                shape1.store_crel(shape2.get_name(), 'o')

            elif is_inside(shape1, shape2):
                shape1.store_crel(shape2.get_name(), 'i')

            check_rel_pos(shape1, shape2)


def check_rel_pos(shape1, shape2):

    center_i = shape1.get_center()
    center_j = shape2.get_center()
    center1 = (int(center_i[0]), int(center_i[1]))
    center2 = (int(center_j[0]), int(center_j[1]))
    
    if center1[0] < center2[0]:
        shape1.store_hrel(shape2.get_name(), 'l')
    elif center1[0] > center2[0]:
        shape1.store_hrel(shape2.get_name(), 'r')
        
    if center1[1] < center2[1]:
        shape1.store_vrel(shape2.get_name(), 'b')
    elif center1[1] > center2[1]:
        shape1.store_vrel(shape2.get_name(), 'a')


def intersection_check(shape1, shape2):

    for i in shape1.get_loop():
        for j in shape2.get_loop():
            if set(i) == set(j):
                return True

    return False


def raycast_intersect(point_i, edge):

    point = (int(point_i[0]), int(point_i[1]))
    huge = sys.float_info.max
    tiny = sys.float_info.min

    p1 = (int(edge[0][0]), int(edge[0][1]))
    p2 = (int(edge[1][0]), int(edge[1][1]))

    if p1[1] > p2[1]:
        (p1, p2) = (p2, p1)
    if point[1] == p1[1] or point[1] == p2[1]:
        point = (point[0], point[1] + 0.00001)
 
    intersect = False
 
    if (point[1] > p2[1] or point[1] < p1[1]) or (
        point[0] > max(p1[0], p2[0])):
        return False
 
    if point[0] < max(p1[0], p2[0]):
        intersect = True
    else:
        if abs(p1[0] - p2[0]) > tiny:
            check1 = (p2[1] - p1[1]) / float(p2[0] - p1[0])
        else:
            check1 = huge
        if abs(p1[0] - point[0]) > tiny:
            check2 = (point[1] - p1[1]) / float(point[0] - p1[0])
        else:
            check2 = huge
        intersect = check2 >= check1

    return intersect   


def is_inside(shape1, shape2):

    total = 0

    if shape2.get_shape() == 'circle':
        return is_inside_circle(shape1, shape2)

    if shape1.get_shape() == 'dot':
        loop2 = shape2.get_loop()
        point = shape1.get_loop()
        for i in range(1, len(loop2)):
            total += raycast_intersect(point, (loop2[i], loop2[i - 1]))

    else:
        loop2 = shape2.get_loop()
        for point in shape1.get_loop():
            for i in range(1, len(loop2)):
                total += raycast_intersect(point, (loop2[i], loop2[i - 1]))

    return total % 2 == 1


def is_inside_circle(shape1, shape2):
 
    if shape1.get_shape() == 'circle':
        return sqrt(float(distance(shape1.get_center(), shape2.get_center()))) + shape1.get_radius() < shape2.get_radius()

    elif shape1.get_shape() == 'dot':
        point = shape1.get_loop()
        center = shape2.get_center()
        r = shape2.get_radius()
        if not sqrt(float(distance(point, center))) < r:
            return False

    else:
        center = shape2.get_center()
        r = shape2.get_radius()
        for point in shape1.get_loop():
            if not sqrt(float(distance(point, center))) < r:
                return False
                
    return True
        
    
def print_objects():
    """Print All Produced 'Shape' Objects"""
    for shape in objects:
        shape.print_p()
        shape.print_shape()
        shape.print_pos()
        shape.print_relatives()


if __name__ == '__main__':

    main()
