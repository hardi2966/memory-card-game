import ipywidgets as widgets
from IPython.display import display, clear_output
import random
import time
import json
import os

LEADERBOARD_FILE = "leaderboard.json"
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

class MemoryGame:
    def __init__(self, player_mode, players, theme, difficulty, welcome_box):
        self.player_mode = player_mode
        self.players = players
        self.current_player = 0
        self.scores = [0 for _ in players]
        self.theme = theme
        self.difficulty = difficulty
        self.welcome_box = welcome_box

        if difficulty == "Easy":
            self.btn_layout = widgets.Layout(width='80px', height='80px')
            self.rows, self.cols = 3, 4
        elif difficulty == "Medium":
            self.btn_layout = widgets.Layout(width='60px', height='60px')
            self.rows, self.cols = 4, 4
        else:
            self.btn_layout = widgets.Layout(width='40px', height='40px')
            self.rows, self.cols = 6, 6

        self.symbol_themes = {
            "Fruits": ["🍎", "🍌", "🍒", "🍇", "🍉", "🍓", "🍑", "🥝", "🍍", "🥥"],
            "Shapes": ["▲", "●", "■", "◆", "★", "☀", "☁", "☂", "☯", "✿"],
            "Animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"],
            "Sports": ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🥎", "🏏", "🏑", "🏓"],
            "Vehicles": ["🚗", "🚕", "🚙", "🚌", "🚎", "🏎", "🚓", "🚑", "🚒", "🚜"],
            "Food": ["🍔", "🍟", "🌭", "🍕", "🥪", "🌮", "🍣", "🥗", "🍩", "🍪"],
            "Technology": ["💻", "🖥", "⌨️", "🖱", "📱", "📷", "🎧", "🎮", "📺", "🔋"],
            "Nature": ["🌲", "🌳", "🌴", "🌵", "🌸", "🌼", "🌻", "🍂", "🍄", "🌙"],
            "Weather": ["☀️", "🌤", "⛅", "🌧", "⛈", "🌩", "❄️", "🌪", "🌈", "💨"]
        }

        symbols = self.symbol_themes[self.theme] * 10
        needed_pairs = (self.rows * self.cols) // 2
        symbols = symbols[:needed_pairs]
        self.cards = symbols * 2
        random.shuffle(self.cards)
        self.flipped = []
        self.buttons = []
        self.matched_indices = set()
        self.start_time = time.time()

        self.game_box = widgets.VBox()
        self.create_ui()
    def create_ui(self):
        self.score_label = widgets.Label(value=self.get_score_text())
        self.board_grid = widgets.GridBox(layout=widgets.Layout(grid_template_columns="repeat(" + str(self.cols) + ", auto)"))
        self.buttons = []
        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                btn = widgets.Button(
                    description="❓",
                    layout=self.btn_layout
                )
                btn.on_click(lambda b, i=idx: self.flip_card(i))
                self.buttons.append(btn)
                self.board_grid.children = self.buttons
                idx += 1
        self.game_box.children = [self.score_label, self.board_grid]
        clear_output(wait=True)
        display(self.game_box)
    def get_score_text(self):
        if self.player_mode == "Single":
            return f"Player: {self.players[0]} | Score: {self.scores[0]}"
        else:
            return " | ".join([f"{self.players[i]}: {self.scores[i]}" for i in range(len(self.players))]) + f" | Turn: {self.players[self.current_player]}"
    def flip_card(self, index):
        if len(self.flipped) == 2 or index in self.matched_indices:
            return
        btn = self.buttons[index]
        btn.description = self.cards[index]
        self.flipped.append((index, self.cards[index]))
        if len(self.flipped) == 2:
            time.sleep(1)
            self.check_match()
    def check_match(self):
        (index1, sym1), (index2, sym2) = self.flipped
        btn1, btn2 = self.buttons[index1], self.buttons[index2]
        if sym1 == sym2:
            self.scores[self.current_player] += 1
            self.matched_indices.add(index1)
            self.matched_indices.add(index2)
            btn1.disabled = True
            btn2.disabled = True
        else:
            btn1.description = "❓"
            btn2.description = "❓"
            if self.player_mode == "Double":
                self.current_player = 1 - self.current_player
        self.flipped = []
        self.score_label.value = self.get_score_text()
        if len(self.matched_indices) == self.rows * self.cols:
            self.end_game()
    def end_game(self):
        elapsed = int(time.time() - self.start_time)
        if self.player_mode == "Single":
            message = f"🎉 {self.players[0]} scored {self.scores[0]} in {elapsed} sec"
            winner = self.players[0]
        else:
            if self.scores[0] > self.scores[1]:
                winner = self.players[0]
                message = f"🎉 {winner} wins with {self.scores[0]} points!"
            elif self.scores[1] > self.scores[0]:
                winner = self.players[1]
                message = f"🎉 {winner} wins with {self.scores[1]} points!"
            else:
                winner = "Tie"
                message = "🤝 It's a tie!"

        lb = load_leaderboard()
        if winner != "Tie":
            lb.append({"player": winner, "score": max(self.scores), "time": elapsed})
            save_leaderboard(lb)
        print(message)
        restart_button = widgets.Button(description="Restart?")
        restart_button.on_click(lambda b: self.restart_game())
        self.game_box.children = list(self.game_box.children) + [restart_button]
    def restart_game(self):
        clear_output(wait=True)
        launch_welcome()

def launch_welcome():
    welcome_box = widgets.VBox()
    title_label = widgets.Label(value="🃏 Memory Card Game")

    mode_label = widgets.Label(value="Select Mode:")
    mode_radio = widgets.RadioButtons(options=["Single", "Double"], value="Single")

    player1_input = widgets.Text(description="Player 1 Name:", placeholder="Enter your name")
    player2_input = widgets.Text(description="Player 2 Name (if 2 players):", placeholder="Enter your name")

    theme_label = widgets.Label(value="Theme:")
    theme_dropdown = widgets.Dropdown(options=["Fruits", "Shapes", "Animals", "Sports", "Vehicles", "Food", "Technology", "Nature", "Weather"], value="Fruits")

    diff_label = widgets.Label(value="Difficulty:")
    diff_dropdown = widgets.Dropdown(options=["Easy", "Medium", "Hard"], value="Easy")
    start_button = widgets.Button(description="Start Game")
    exit_button = widgets.Button(description="Exit")
    def start_game_handler(b):
        mode = mode_radio.value
        p1 = player1_input.value or "Player 1"
        p2 = player2_input.value or "Player 2"
        players = [p1] if mode == "Single" else [p1, p2]
        theme = theme_dropdown.value
        difficulty = diff_dropdown.value
        MemoryGame(mode, players, theme, difficulty, welcome_box)
    def exit_handler(b):
        clear_output(wait=True)
        print("Exiting game.")
    start_button.on_click(start_game_handler)
    exit_button.on_click(exit_handler)
    welcome_box.children = [title_label, mode_label, mode_radio, player1_input, player2_input, theme_label, theme_dropdown, diff_label, diff_dropdown, start_button, exit_button]
    display(welcome_box)
if __name__ == "__main__":
    launch_welcome()