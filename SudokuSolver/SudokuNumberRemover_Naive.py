import random
import copy
import Read_Sample_File_From_Downloads

def printing(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j], end=" ")
        print()

#checks if number doesnt exist already within row/col
def isSafe(grid, row, col, num):
    # Check if 'num' is not in the current row
    for x in range(len(grid[0])):
        if grid[row][x] == num:
            return False

    # Check if 'num' is not in the current column
    for x in range(len(grid)):
        if grid[x][col] == num:
            return False
        
    return True

def solveSudoku(grid, row, col, numSolution):
    
    #if currently on last cell, board is a valid solution
    if row == len(grid) - 1 and col == len(grid[0]):
        numSolution += 1
        return numSolution

    #if at end of row, enter next row
    if col == len(grid[0]):
        row += 1
        col = 0

    #if number already exists in current cell, go to the next cell
    if grid[row][col] > 0:
        return solveSudoku(grid, row, col + 1, numSolution)

    #iterates through possible numbers to the cell
    for num in range(1, max(len(grid), len(grid[0])) + 1, 1):
        #if number can be placed, set cell to current number 
        if isSafe(grid, row, col, num):
            grid[row][col] = num

            #continue to next cell 
            numSolution = solveSudoku(grid, row, col + 1, numSolution)

            #if a board has more than 1 solution, return
            if numSolution > 1:
                return numSolution

            #if placed num is an invalid solution, remove num and go to next possible number
            grid[row][col] = 0

    return numSolution

grid = Read_Sample_File_From_Downloads.read_sudoku_from_file("2x4Board100.txt")
count = 0
print("Initial Grid:")
printing(grid)

while(count < 2):
    rRow = random.randint(0, len(grid[0])-1)
    rCol = random.randint(0, len(grid)-1)
    if grid[rRow][rCol] != 0:
        oldGrid = copy.deepcopy(grid)
        grid[rRow][rCol] = 0
        print("New Grid w/ Removed Num")
        printing(grid)
        count = solveSudoku(grid, 0, 0, 0)
        if (count==2):
            grid = oldGrid
print("Uniquely Solveable Grid:")
printing(grid)


