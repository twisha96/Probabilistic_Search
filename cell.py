class Cell:

	def __init__(cell, terrain_type):
		"""
		type = 0 => cell is flat
 		type = 1 => cell is hilly
		type = 2 => cell is forested
		type = 3 => cell is a maze of caves
		"""
		cell.type = terrain_type
		cell.p_target = 0
		cell.visited = False
		false_negative = {
			0: 0.1,
			1: 0.3,
			2: 0.7,
			3: 0.9
		}
		cell.false_negative = false_negative[cell.type]