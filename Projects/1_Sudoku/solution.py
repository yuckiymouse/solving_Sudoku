from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
# left
diagonal_lr = [rows[i] + cols[i] for i in range(len(rows))]

# right .....reverse index ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
# 最後から数えて、変量は１
rcols = cols[::-1]

# loopはindex 8から-1までで、変量は-1 
# (ex. for x in range(0, 10, 2): print x **result** 0, 2, 3, 6, 8で、10は含まない。10まで、ということ。）
diagonal_rl = [rows[i] + rcols[i] for i in range(len(rows) -1, -1, -1)]
unitlist.append(diagonal_lr)
unitlist.append(diagonal_rl)

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # iterate through each unit list:
    for unit in unitlist:
        # check if any value for a square in the list is equal to any other value
        # make a list of values in the squares
        val_list = [values[square] for square in unit]
       
        # find all duplicate values in that list that could be naked twins
        # criteria are 1) the number appears exactly twice in val_list and
        # 2) the number is 2 digits long
        nt_dupes_index = [i for i in range(0, len(val_list)) if
                    val_list.count(val_list[i]) == 2  and len(val_list[i]) == 2]

        # if there is at least one pair of naked twins
        if len(nt_dupes_index) == 2:
            # create a variable for the nt value
            nt_value = val_list[nt_dupes_index[0]]
            # turn the two values into a list
            nt_list_values = list(val_list[nt_dupes_index[0]])
            # iterate through the val_list to find common digits
            idx = 0
            for v in val_list:
                if len(v) > 1 and v != nt_value:
                    v_list = list(v)
                    found_nt_vals = [j for j in v_list if j in nt_list_values]
                    # if nt numbers found in value, replace it in the values dict
                    if len(found_nt_vals) > 0:
                        for k in found_nt_vals:
                            values[unit[idx]] = values[unit[idx]].replace(k, "")
                idx += 1


        # no naked twin pairs found
        else:
            continue
    return (values)
    
    
    
    
    
    raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digits = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digits, '')
    return values
    raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    
    raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        #check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        #use eliminate strategy
        values = eliminate(values)
        
        #use only choice strategy
        values = only_choice(values)
        
        #check how many boxes have a determined value
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # if no new values were added, stop the loop
        stalled = solved_values_before == solved_values_after
        
        #sanity check, return False if there is a box with zero available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    
    raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    if values is False:
        return False ## failed earlier
    
    if all(len(values[s]) == 1 for s in boxes):
        return values ## solved
    
    # choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return naked_twins(attempt)
   
      


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
