♟️ Chess AI – Python

Chess game developed in Python with Pygame and python-chess. Features an AI opponent using Minimax with Alpha-Beta pruning, heuristic evaluation, move ordering, and pawn promotion.

A simple chess game developed in Python using Pygame and python-chess, featuring a playable graphical interface and an AI opponent based on the Minimax algorithm with Alpha-Beta pruning.

Features
Interactive chessboard with mouse controls
Legal move generation using python-chess
AI opponent with:
Minimax search
Alpha-Beta pruning
Heuristic board evaluation
Move ordering optimization
Piece promotion support
Highlighting of legal moves
Basic positional evaluation (material + mobility)
Technologies
Python
Pygame
python-chess
AI Implementation

The AI evaluates positions using:

Piece values
Mobility (number of legal moves)
Alpha-Beta pruning to reduce the search tree
Capture-first move ordering for better pruning efficiency
Installation

Install dependencies:

pip install pygame python-chess
Recommended Python Version

Older Python versions are recommended for better compatibility with graphical and third-party libraries.

Tested versions:

Python 3.10
Python 3.11
Python 3.12

Python 3.13 may cause compatibility issues with some graphical dependencies on Windows.

Run the project
python main.py
Project Structure
project/
│
├── main.py
├── pieces/
│   ├── wp.png
│   ├── bp.png
│   └── ...
Future Improvements
Better evaluation heuristics
Opening book
Transposition tables
Checkmate detection optimization
Adjustable AI difficulty
Multiplayer mode
Author

University project focused on game AI and search algorithms.
