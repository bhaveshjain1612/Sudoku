import streamlit as st
import numpy as np
import time
from ortools.sat.python import cp_model

# ---------------- CP-SAT Solver ---------------- #
def solve_sudoku_cp(puzzle):
    model = cp_model.CpModel()
    cells = {}

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                cells[i, j] = model.NewIntVar(1, 9, f"x_{i}_{j}")
            else:
                cells[i, j] = model.NewIntVar(puzzle[i][j], puzzle[i][j], f"x_{i}_{j}")

    for i in range(9):
        model.AddAllDifferent([cells[i, j] for j in range(9)])
    for j in range(9):
        model.AddAllDifferent([cells[i, j] for i in range(9)])
    for bi in range(3):
        for bj in range(3):
            box = [cells[i, j] for i in range(bi*3, bi*3+3) for j in range(bj*3, bj*3+3)]
            model.AddAllDifferent(box)

    model.Add(sum(cells[i, j] for i in range(9) for j in range(9)) == 405)

    solver = cp_model.CpSolver()
    start = time.time()
    status = solver.Solve(model)
    end = time.time()

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        solved = np.array([[solver.Value(cells[i, j]) for j in range(9)] for i in range(9)])
        return solved, end - start
    return None, end - start

# ---------------- Smart Backtracking Solver ---------------- #
def get_candidates(board, row, col):
    if board[row][col] != 0:
        return []
    used = set(board[row]) | {board[i][col] for i in range(9)}
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            used.add(board[box_r + i][box_c + j])
    return [n for n in range(1, 10) if n not in used]

def find_empty_with_fewest_options(board):
    best = (None, None, list(range(1, 10)))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                opts = get_candidates(board, i, j)
                if len(opts) < len(best[2]):
                    best = (i, j, opts)
    return best if best[0] is not None else None

def solve_smart(board):
    cell = find_empty_with_fewest_options(board)
    if not cell:
        return True
    row, col, candidates = cell
    for num in candidates:
        board[row][col] = num
        if solve_smart(board):
            return True
        board[row][col] = 0
    return False

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Sudoku Solver", layout="centered")
st.title("Sudoku Solver")
st.markdown("Enter your Sudoku puzzle below (use 0 for empty cells):")

# Buttons
col1, col2 = st.columns([1, 1])
solve_clicked = col1.button("✅ Solve Sudoku")
reset_clicked = col2.button("🔁 Reset Grid")

# Handle reset
if reset_clicked:
    for i in range(9):
        for j in range(9):
            st.session_state[f"cell_{i}_{j}"] = "0"
    st.rerun()

# Create input grid
input_grid = []
for i in range(9):
    cols = st.columns(11)  # 9 inputs + 2 for vertical dividers
    row = []
    col_idx = 0  # actual Streamlit column index

    for j in range(9):
        key = f"cell_{i}_{j}"
        if key not in st.session_state:
            st.session_state[key] = "0"

        # Input field
        val = cols[col_idx].text_input(
            key,
            value=st.session_state[key],
            max_chars=1,
            label_visibility="collapsed"
        )

        # Convert to int
        try:
            num = int(val)
            row.append(num if 0 <= num <= 9 else 0)
        except:
            row.append(0)

        col_idx += 1

        # Add vertical divider after 3rd and 6th column
        if (j + 1) % 3 == 0 and j != 8:
            with cols[col_idx]:
                st.markdown("<div style='font-size:24px; text-align:center;'>|</div>", unsafe_allow_html=True)
            col_idx += 1

    input_grid.append(row)

    # Add horizontal divider after 3rd and 6th row
    if (i + 1) % 3 == 0 and i != 8:
        st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)


# Handle solve
if solve_clicked:
    st.write("🧮 Solving using OR-Tools Optimizer...")
    cp_solution, cp_time = solve_sudoku_cp(input_grid)

    if cp_solution is not None:
        st.success(f"✅ Optimized solution found in {cp_time:.4f} seconds.")

        # Fill values back into session state
        for i in range(9):
            for j in range(9):
                st.session_state[f"cell_{i}_{j}"] = str(cp_solution[i][j])

        st.rerun()

    else:
        st.error("❌ Optimizer couldn't find a valid solution.")
        st.info(f"⏱️ Time taken: {cp_time:.4f} seconds.")