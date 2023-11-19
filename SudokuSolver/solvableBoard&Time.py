import os
import random
import re
import random
import time
import copy

def read_sudoku_from_file(file_path):
    # Get the user's home directory
    #home_directory = os.path.expanduser("~")

    # Create the full path to the Downloads directory
    #downloads_directory = os.path.join(home_directory, "Downloads")

    # Create the full path to the file
    #file_path = os.path.join(downloads_directory, filename)

    # Check if the file exists before attempting to read
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
            # Split the contents into rows
            rows = file_contents.strip().split('\n')

            # Convert the string representation to a 2D list (grid)
            grid = [[int(num) if num != '0' else 0 for num in row.split()] for row in rows]

            return grid
    else:
        print(f"The file {filename} does not exist in the Downloads directory.")

def printing(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j], end=" ")
        print()

def isSafe(grid, row, col, num, subgrid_rows, subgrid_cols):
    # Check if 'num' is not in the current row
    for x in range(len(grid[0])):
        if grid[row][x] == num:
            return False

    # Check if 'num' is not in the current column
    for x in range(len(grid)):
        if grid[x][col] == num:
            return False
        
    # Check if 'num' is not in the current sub-grid
    startRow, startCol = subgrid_rows * (row // subgrid_rows), subgrid_cols * (col // subgrid_cols)
    for i in range(subgrid_rows):
        for j in range(subgrid_cols):
            if grid[startRow + i][startCol + j] == num:
                return False
            
    return True

def solveSudoku(grid, row, col, subgrid_rows, subgrid_cols, numSolution):
    
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
        return solveSudoku(grid, row, col + 1, subgrid_rows, subgrid_cols, numSolution)

    #iterates through possible numbers to the cell
    for num in range(1, max(len(grid), len(grid[0])) + 1, 1):
        #if number can be placed, set cell to current number 
        if isSafe(grid, row, col, num, subgrid_rows, subgrid_cols):
            grid[row][col] = num

            #continue to next cell 
            numSolution = solveSudoku(grid, row, col + 1, subgrid_rows, subgrid_cols, numSolution)

            #if a board has more than 1 solution, return
            if numSolution > 1:
                return numSolution

            #if placed num is an invalid solution, remove num and go to next possible number
            grid[row][col] = 0

    return numSolution

def read_sudoku_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    grid = [list(map(int, line.split())) for line in lines]
    return grid

input_folder_path = "C:\\Users\\Yimmy\\Downloads\\Ver1.2Boards\\"


# Loop through subfolders in the input folder
for subfolder in os.listdir(input_folder_path):
    print("Subfolder:", subfolder)
    subfolder_path = os.path.join(input_folder_path, subfolder)
    print(subfolder_path)

    # Check if it's a directory
    if os.path.isdir(subfolder_path):
        # Loop through files in the subfolder
        for filename in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, filename)

            # Check if it's a file
            if os.path.isfile(file_path):
                # Check if the file has a ".txt" extension
                print(f"FileName: {filename}")

                if filename.__contains__("Board"):
                    # Extract dimensions and iteration_number from the filename
                    intermediate = os.path.splitext(filename)[0].split("x")

                    print(f"intermediate: {intermediate}")

                    if len(intermediate) > 1:
                        matches = re.findall(r'\d+', intermediate[1])

                    # Extract the first and second values
                    subgrid_col_dim = intermediate[0]
                    subgrid_row_dim = int(matches[0]) if matches else None
                    iteration = int(matches[1]) if len(matches) > 1 else None

                    # Print the result
                    print("Subgrid col dim: ", subgrid_col_dim)
                    print("Subgrid row dim:", subgrid_row_dim)
                    #print("Iteration:", iteration)
                    
#######################READ IN BASE FILE AND MAKE SOLVABLE############################################################################
                    
                    grid = read_sudoku_from_file(file_path)
                    count = 0
                    print("Initial Grid:")
                    printing(grid)

                    start_time = time.time()
                    while(count < 2):
                        if time.time()-start_time > 130:
                            break
                        rRow = random.randint(0, len(grid[0])-1)
                        rCol = random.randint(0, len(grid)-1)
                        if grid[rRow][rCol] != 0:
                            oldGrid = copy.deepcopy(grid)
                            grid[rRow][rCol] = 0
                            print("New Grid w/ Removed Num")
                            printing(grid)
                            count = solveSudoku(grid, 0, 0, int(subgrid_row_dim), int(subgrid_col_dim), 0)
                            if (count==2):
                                grid = oldGrid

                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time
                    OUT_FILE = "C:\\Users\\Yimmy\\Downloads\\solvableBoard&Time.txt"
                    with open(OUT_FILE, 'a') as file:
                        file.write(f"-----------------------------------------------------------------------------------\n")
                        file.write(f"FileName: {filename}\n")
                        for i in range(len(grid)):
                            for j in range(len(grid[i])):
                                file.write(f"{grid[i][j]} ")
                            file.write("\n")
                        file.write(f"Time to remove values: {elapsed_time}\n\n")
                        file.close()

                    

                    #print("Uniquely Solveable Grid:")
                    #printing(grid)

