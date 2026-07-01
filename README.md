# Memory Card Game (Python)

A simple interactive **Memory Card Matching Game** developed in **Python** using **ipywidgets** for a Jupyter Notebook environment. The game challenges players to match pairs of cards while improving memory and concentration skills.

### Features

* Single-player and two-player game modes
* Multiple themes (Fruits, Animals, Shapes, Sports, Food, Technology, Nature, Weather, and Vehicles)
* Three difficulty levels: Easy, Medium, and Hard
* Real-time score tracking and turn management
* Leaderboard system using JSON file storage
* Restart and exit options
* User-friendly graphical interface built with ipywidgets

### Technologies Used

* Python
* ipywidgets
* JSON
* Random
* Time
* OS Module

### How It Works

Players flip two hidden cards at a time to find matching pairs. If the cards match, they remain visible and the player earns a point. Otherwise, the cards are flipped back over. In two-player mode, turns alternate after an incorrect match. The game ends when all pairs have been matched, and the winner or final score is displayed and saved to the leaderboard.
