def find_attacking_queens(string):
	'''
		Should take a string representing the positions of queens on a board
		and return the number of attacking pairs
	'''
	attacking_queen_count = 0
	for idx, num in enumerate(string):
		for jdx, num2 in enumerate(string):
			if idx != jdx:
				if num == num2:
					attacking_queen_count+=1
				if int(num) == (int(num2) - abs(idx - jdx)):
					attacking_queen_count+=1
				if int(num) == (int(num2) + abs(idx - jdx)):
					attacking_queen_count+=1
	return str(attacking_queen_count/2)


board1 = '24748552'
board2 = '32752411'
board3 = '24415124'
board4 = '32543213'

print( board1 + ' : ' + find_attacking_queens(board1))
print( board2 + ' : ' + find_attacking_queens(board2))
print( board3 + ' : ' + find_attacking_queens(board3))
print( board4 + ' : ' + find_attacking_queens(board4))