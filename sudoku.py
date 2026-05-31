# A very easy board: 0 is the empty space you need to fill
board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 0] # Only one spot left!

def show_board():
    print("\n   0 1 2   3 4 5   6 7 8") # Column headers
    print("  -----------------------")
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("  ------ + ------ + ------")
        
        line = f"{r}| " # Row header
        for c in range(9):
            if c % 3 == 0 and c != 0:
                line += "| "
            char = "." if board[r][c] == 0 else str(board[r][c])
            line += char + " "
        print(line)

def play_game():
    print("Welcome to Easy Sudoku!")
    print("Goal: Fill the '.' with the correct number (1-9).")
    
    while True:
        show_board()
        
        # Get user input
        try:
            row = int(input("\nEnter Row (0-8): "))
            col = int(input("Enter Col (0-8): "))
            val = int(input("Enter Value (1-9): "))
            
            # Simple check: In this 'easy' version, we just check if it's the right answer
            # The correct answer for the last spot in this specific board is 9
            if row == 8 and col == 8 and val == 9:
                board[8][8] = 9
                show_board()
                print("\nCONGRATULATIONS! You solved it!")
                break
            else:
                print("\n[!] Not quite right. Try again!")
                
        except ValueError:
            print("\n[!] Please enter numbers only.")

if __name__ == "__main__":
    play_game()