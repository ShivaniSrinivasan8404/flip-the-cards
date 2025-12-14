import tkinter as tk
from tkinter import messagebox
import random
import time

# -------------------------------------------------
# SETTINGS
# -------------------------------------------------
EMOJIS = ["🐶","🐱","🐼","🐵","🦊","🐸","🐯","🐷","🐙","🐰"]
FONT = ("Segoe UI Emoji", 48)
BACKGROUND = "#0ecbe8"
CARD_COLOR = "#4A19EB"
FLIP_COLOR = "#b65bb0"
MATCH_COLOR = "#78e76e"

HIGH_SCORE = None  # Stores best time this session

# -------------------------------------------------
# GAME CLASS
# -------------------------------------------------
class EmojiFlipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Emoji Flip Memory Game")
        self.root.configure(bg=BACKGROUND)

        self.matched = 0
        self.start_time = None

        self.make_menu()
        self.create_game_board()
        self.create_timer_label()

        self.update_timer()  # Start timer loop

    # ---------------- TIMER ----------------
    def create_timer_label(self):
        self.timer_label = tk.Label(
            self.root,
            text="Time: 0.0 s",
            font=("Arial", 20, "bold"),
            bg=BACKGROUND,
            fg="white"
        )
        self.timer_label.pack()

        self.start_time = time.time()

    def update_timer(self):
        if self.matched < 16:  # Continue updating only during game
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.1f} s")

        self.root.after(100, self.update_timer)

    # ---------------- MENU BAR ----------------
    def make_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)

        game_menu.add_command(label="Restart", command=self.restart)
        game_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

    # ---------------- BOARD SETUP ----------------
    def create_game_board(self):
        emojis = random.sample(EMOJIS, 8)
        self.cards = emojis * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.first = None

        self.frame = tk.Frame(self.root, bg=BACKGROUND)
        self.frame.pack(pady=20)

        index = 0
        for r in range(4):
            row = []
            for c in range(4):
                btn = tk.Button(
                    self.frame,
                    text="❔",
                    font=("Segoe UI Emoji", 35),
                    width=3,
                    height=1,
                    bg=CARD_COLOR,
                    fg="white",
                    relief="raised",
                    command=lambda idx=index: self.flip_card(idx)
                )
                btn.grid(row=r, column=c, padx=10, pady=10)
                row.append(btn)
                index += 1
            self.buttons.append(row)

    # ---------------- FLIP ANIMATION ----------------
    def animate_flip(self, btn, emoji):
        for size in range(35, 5, -3):  
            btn.config(font=("Segoe UI Emoji", size))
            btn.update()

        btn.config(text=emoji, bg=FLIP_COLOR)

        for size in range(5, 35, 3):  
            btn.config(font=("Segoe UI Emoji", size))
            btn.update()

    # ---------------- GAME LOGIC ----------------
    def flip_card(self, index):
        r, c = divmod(index, 4)
        btn = self.buttons[r][c]

        if btn["text"] != "❔":
            return

        emoji = self.cards[index]
        self.animate_flip(btn, emoji)

        if self.first is None:
            self.first = (index, btn, emoji)

        else:
            idx1, btn1, emoji1 = self.first

            if emoji1 == emoji:
                btn.config(bg=MATCH_COLOR)
                btn1.config(bg=MATCH_COLOR)

                self.matched += 2

                if self.matched == 16:
                    self.show_scoreboard()

            else:
                self.root.after(700, lambda: self.hide_cards(btn, btn1))

            self.first = None

    def hide_cards(self, b1, b2):
        b1.config(text="❔", bg=CARD_COLOR, font=("Segoe UI Emoji", 35))
        b2.config(text="❔", bg=CARD_COLOR, font=("Segoe UI Emoji", 35))

    # ---------------- SCOREBOARD POPUP ----------------
    def show_scoreboard(self):
        global HIGH_SCORE

        total_time = time.time() - self.start_time

        # Update high score
        if HIGH_SCORE is None or total_time < HIGH_SCORE:
            HIGH_SCORE = total_time
            new_score_text = "🏆 NEW HIGH SCORE!"
        else:
            new_score_text = ""

        win = tk.Toplevel(self.root)
        win.title("🎉 Game Complete!")
        win.geometry("380x330")
        win.configure(bg="#222831")

        tk.Label(win, 
                 text="🎉 YOU WON! 🎉", 
                 font=("Arial", 26, "bold"),
                 bg="#222831", fg="#00E0FF").pack(pady=10)

        tk.Label(win, 
                 text=f"⏳ Time Taken: {total_time:.2f} seconds",
                 font=("Arial", 18),
                 bg="#222831", fg="white").pack(pady=10)

        tk.Label(win,
                 text=f"🏅 High Score: {HIGH_SCORE:.2f} s",
                 font=("Arial", 18, "bold"),
                 bg="#222831", fg="#FFD369").pack(pady=5)

        tk.Label(win,
                 text=new_score_text,
                 font=("Arial", 20, "bold"),
                 bg="#222831", fg="#00FF88").pack()

        tk.Button(win, text="🔄 Play Again",
                  font=("Arial", 16, "bold"),
                  bg="#00ADB5", fg="white",
                  width=15,
                  command=lambda: [win.destroy(), self.restart()]).pack(pady=15)

        tk.Button(win, text="🚪 Exit",
                  font=("Arial", 16, "bold"),
                  bg="#d72323", fg="white",
                  width=15,
                  command=self.root.quit).pack()

    # ---------------- RESTART ----------------
    def restart(self):
        self.frame.destroy()
        self.matched = 0
        self.first = None
        self.start_time = time.time()
        self.create_game_board()


# -------------------------------------------------
# RUN GAME
# -------------------------------------------------
root = tk.Tk()
root.geometry("650x650")
EmojiFlipGame(root)
root.mainloop()



