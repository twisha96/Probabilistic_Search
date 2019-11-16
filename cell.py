class Cell:

   def __init__(cell):
      """
      type = 0 => cell is flat
      type = 1 => cell is hilly
      type = 2 => cell is forested
      type = 3 => cell is a maze of caves
      """
      cell.type = -1

      # boolean which says if target is at the cell
      cell.is_target = False

      # belief of a cell containing the target
      cell.belief = -1

      # the probability of a cell containing the target without any prior knowledge
      cell.initial_probability = -1

      # the rate of false positive for the given cell
      cell.false_negative = 0

      # cost of a cell given a current cell
      cell.cost = -1

      # the utility of the entire map given this cell as the current cell
      cell.utility_helper = -1

      # the summation of the cost of cell and the entire board
      cell.utility = -1

      # cost of cell computed by using it's distance from the explored node and cost of the subsequent traversal upon failure
      cell.new_cost = -1
