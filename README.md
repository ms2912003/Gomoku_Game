# Gomoku AI with Minimax and Alpha-Beta Pruning

A Python implementation of the classic Gomoku (Five in a Row) game featuring two AI players using different algorithms: Minimax and Alpha-Beta Pruning.

## Features
- 🎮 Two game modes:
  - Human vs AI
  - AI vs AI (Minimax vs Alpha-Beta)
- ⚡ Optimized AI algorithms with evaluation functions
- 🎨 Clean graphical interface with Pygame
- 🔊 Sound effects for moves and game outcomes
- ⏯️ Pause functionality
- 🖱️ Interactive menu system

## Technologies Used
- Python 3.x
- Pygame
- Minimax algorithm
- Alpha-Beta pruning optimization

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ms2912003/Gomoku_Game.git
   cd gomoku-ai
    Install the required dependencies:
    bash

pip install pygame

Run the game:
bash

    python gomoku.py

Game Modes
Human vs AI

    Play against the computer which uses both Minimax and Alpha-Beta algorithms

    The AI will:

        First check for immediate winning moves

        Then block your winning moves

        Finally use strategic algorithms to determine the best move

AI vs AI

    Watch two AI players compete:

        Minimax AI (Red) - Uses basic Minimax algorithm

        Alpha-Beta AI (Blue) - Uses optimized Alpha-Beta pruning version

Controls

    Mouse: Click on the board to place your stone

    Buttons:

        Pause: Temporarily stops the game

        Back to Menu: Returns to the main menu

    Keyboard:

        P: Pause the game

        ESC: Return to menu (when paused)

File Structure

gomoku-ai/
│── gomoku.py            # Main game file
│── Images/              # Contains background images
│   ├── wood_texture.jpeg
│   └── menu.jpg
│── Sounds/              # Contains sound effects
│   ├── Mouse_Click.mp3
│   ├── Win_Sound.wav
│   └── Lose_Sound.wav
└── README.md            # This file

Future Improvements

    Adjustable difficulty levels

    Move history and undo functionality

    Tournament mode with score tracking

    Improved evaluation function for smarter AI

    Mobile/Web version
    
Enjoy the game! 🎮
