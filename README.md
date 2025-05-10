# Sudoku Solver App

This is a web-based Sudoku Solver built using Python, Streamlit, and Google OR-Tools. It provides an intuitive 9x9 grid interface where users can input Sudoku puzzles and solve them instantly using constraint programming techniques. The solver is complemented by a smart backtracking verifier and designed with a layout that visually mimics a traditional Sudoku board.

---

## Features

- Interactive 9x9 Sudoku input grid  
- Solves puzzles using Google OR-Tools CP-SAT Solver  
- Smart backtracking algorithm using the Minimum Remaining Value (MRV) heuristic  
- Timer to show the time taken to solve the puzzle  
- Clean UI with visual dividers between 3x3 subgrids  
- Reset functionality to clear and restart the grid  

## How It Works

This application solves Sudoku puzzles using a two-step architecture:

### 1. Constraint Programming with OR-Tools

The core solving logic is implemented using [Google OR-Tools](https://developers.google.com/optimization), specifically the CP-SAT (Constraint Programming - SAT) solver.

- **Variables:** Each cell is modeled as an integer variable ranging from 1 to 9.
- **Constraints:**
  - **Row Constraint:** All numbers in a row must be different (`AllDifferent`).
  - **Column Constraint:** All numbers in a column must be different.
  - **Box Constraint:** All numbers in each 3x3 subgrid must be different.
  - **Sum Constraint (Optional):** The total sum of all cells is constrained to 405 (i.e., 45 * 9), which can help stabilize and slightly optimize the model.
- **Solver Behavior:** The CP-SAT solver explores the solution space using backtracking and constraint propagation techniques to find a feasible or optimal assignment.

### 2. Smart Backtracking Verifier (Optional)

For educational or secondary verification purposes, a custom backtracking algorithm is included.

- **Heuristic:** Uses the Minimum Remaining Value (MRV) strategy to choose the next empty cell with the fewest valid options.
- **Recursion:** Applies depth-first search, trying each candidate value and backtracking when necessary.
- **Efficiency:** While slower than OR-Tools for complex puzzles, it demonstrates fundamental recursive solving techniques and serves as a cross-verification method.

### 3. Streamlit UI

The front-end is built using Streamlit:

- The input grid dynamically renders 9x9 input boxes.
- Styling logic adds visual separators (using `|` and `<hr>`) between the 3x3 blocks to replicate a classic Sudoku layout.
- After solving, the grid updates in-place with the solution.
- A timer is displayed to show the solving duration.
- The "Reset" button clears all input fields.

