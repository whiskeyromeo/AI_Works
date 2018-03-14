import re

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def get_diagonals(row, col):
    """
    Takes strings representing the rows and columns of the sudoku
    and cells expected along the diagonal
    Args:
        row(string): a string representing the row
        col(string): a string representing the column
    Returns:
        A list comprised of two lists, one representing the descending
        peers and another representing the ascending peers
    """
    desc = [a+b for a,b in zip(*(v+v[-1]*(max(len(row), len(col))-len(v)) for v in (row, col)))]
    asc = [a+b for a,b in zip(*(v+v[-1]*(max(len(row), len(col))-len(v)) for v in (row, col[::-1])))]
    return [desc, asc]

boxes = cross(rows, cols)

def prep_cells():
    """
    Uses the global strings row, col to create a list of all units
    Returns: 
        A list of all units which exist in the sudoku
    """
    #Find the peers in the same row
    row_units = [cross(r, cols) for r in rows]
    #Find the peers in the same 
    col_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs,cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    diagonal_units = get_diagonals(rows, cols)
    unitlist = row_units + col_units + square_units + diagonal_units
    return unitlist


def gen_units(values):
    """
    Uses a set of values to generate units of peers
    Args: 
        values(dict): a dict of the form {'box_name': '123456789', ... }
    Returns:
        A dictionary organized by keys representing cells with a list of units
        as the value

    """
    unitlist = prep_cells()
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    return units

def gen_peers(values):
    """
    Uses values to generate a dictionary of all peers of a given cell
    Args:
        values(dict): a dict of the form {'box_name': '123456789', ... }
    Returns:
        A dict organized by keys representing cells with the value a list
        of all peers
    """
    units = gen_units(values)
    return dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    newVals = values.copy()
    # Get the dictionary of all of the peers
    peers = gen_units(newVals)
    # Get the potential twins
    potential_twins = [box for box in newVals.keys() if len(newVals[box]) == 2]
    #Iterate through the twins
    for box in potential_twins:
        # Nominate a candidate
        candidate = newVals[box]
        #Get the units of the candidate
        for unit in peers[box]:
            # iterate through the units
            for peer in unit:
                if newVals[peer] == candidate and peer != box:
                    #we found a twin! Iterate through the unit again
                    for peer2 in unit:
                        # Avoid the twins and sub out the values from the twins
                        if peer2 != box and peer2 != peer:
                            newVals[peer2] = newVals[peer2].translate({ord(c): None for c in candidate})
    return newVals


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    assert len(grid) == 81
    assert re.match('[1-9.]*$', grid)
    values = dict(zip(boxes, grid))
    for k in values:
        values[k] = re.sub('[.]', '123456789', values[k])
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
            for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Eliminates digit options from a cell whose peers have been determined to 
    contain a value
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        values(dict): modified version of the dict

    """
    peers = gen_peers(values)
    solved = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    '''
        Go through all the units, and whenever there is a unit with a value that only
        fits in one box, make that the choice
        Input: A sudoku in dictionary form
        Output: Resulting sudoku in dictionary form
    '''
    unitlist = prep_cells()
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Runs through the sudoku, eliminating choices as it goes.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        Args:
        values(dict): a modified version of the dictionary
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    """
    Uses depth-first search and propagation to create a search tree and solve the sudoku
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        False if dead-ended, the modified copy of values if successful
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for val in values[s]:
        new_sod = values.copy()
        new_sod[s] = val
        attempt = search(new_sod)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)
    




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
