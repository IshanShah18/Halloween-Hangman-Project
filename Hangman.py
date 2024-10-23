"""
------------------------------------------------------------------------
Author: Ishan Shah
------------------------------------------------------------------------
"""
import tkinter as tk
from tkinter import messagebox
import random



# Load horror movies from the text file
def load_movies():
    with open("horror_movies.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Halloween Hangman Game")
        self.master.configure(bg='black')

        # Load horror movies
        self.movies = load_movies()
        self.chosen_movie = random.choice(self.movies).upper()
        self.guessed_letters = set()
        self.remaining_attempts = 6

        # Create canvas for hangman
        self.canvas = tk.Canvas(master, width=400, height=400, bg='black')
        self.canvas.pack()

        # Create GUI components
        self.word_label = tk.Label(master, text=self.get_display_word(), font=("Helvetica", 24), bg='black', fg='white')
        self.word_label.pack(pady=20)

        self.entry = tk.Entry(master, font=("Helvetica", 24))
        self.entry.pack(pady=10)

        self.guess_button = tk.Button(master, text="Guess", command=self.guess, bg='orange', font=("Helvetica", 14))
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_game, bg='red', font=("Helvetica", 14))
        self.reset_button.pack(pady=10)

        self.draw_hangman()

    def draw_hangman(self):
        """Draw the hangman depending on the remaining attempts."""
        self.canvas.delete("all")
        

        # Draw base stand
        self.canvas.create_line(100, 350, 300, 350, fill="white", width=5)  # base
        self.canvas.create_line(200, 350, 200, 50, fill="white", width=5)   # vertical
        self.canvas.create_line(200, 50, 300, 50, fill="white", width=5)    # top horizontal
        self.canvas.create_line(300, 50, 300, 100, fill="white", width=5)   # rope
        
    
        
            # Draw more realistic pumpkins with grooves and curved stems
        def draw_pumpkin(x1, y1, x2, y2):
            # Main pumpkin body
            self.canvas.create_oval(x1, y1, x2, y2, outline="orange", fill="orange", width=3)
    
            # Grooves (vertical lines)
            for i in range(1, 5):
                self.canvas.create_arc(x1 + i * 10, y1, x2 - i * 10, y2, start=180, extent=180, outline="darkorange", width=2)
    
            # Shading for a 3D effect
            self.canvas.create_arc(x1, y1, x2, y2, start=30, extent=120, outline="darkorange", width=2)
            self.canvas.create_arc(x1, y1, x2, y2, start=210, extent=120, outline="darkorange", width=2)
    
            # Curved stem (using arcs)
            self.canvas.create_arc((x1 + x2) / 2 - 5, y1 - 20, (x1 + x2) / 2 + 5, y1, start=180, extent=180, outline="green", width=4)
    
        # Draw pumpkins on the side of the hangman chart
        draw_pumpkin(50, 320, 100, 370)  # Pumpkin 1
        draw_pumpkin(320, 320, 370, 370)  # Pumpkin 2
        draw_pumpkin(10, 320, 60, 370)  # Pumpkin 3

        # Draw hangman based on remaining attempts
        if self.remaining_attempts <= 5:
            self.canvas.create_oval(250, 100, 350, 200, outline="white", width=3)  # Head
        if self.remaining_attempts <= 4:
            self.canvas.create_line(300, 200, 300, 300, fill="white", width=3)     # Body
        if self.remaining_attempts <= 3:
            self.canvas.create_line(300, 230, 250, 270, fill="white", width=3)     # Left Arm
        if self.remaining_attempts <= 2:
            self.canvas.create_line(300, 230, 350, 270, fill="white", width=3)     # Right Arm
        if self.remaining_attempts <= 1:
            self.canvas.create_line(300, 300, 250, 350, fill="white", width=3)     # Left Leg
        if self.remaining_attempts <= 0:
            self.canvas.create_line(300, 300, 350, 350, fill="white", width=3)     # Right Leg
            messagebox.showinfo("Game Over", f"You lost! The movie was '{self.chosen_movie}'")

    def guess(self):
        """Handle the guessing logic and update the display."""
        letter = self.entry.get().upper()
        self.entry.delete(0, tk.END)

        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if letter in self.guessed_letters:
            messagebox.showwarning("Already Guessed", "You've already guessed that letter.")
            return

        self.guessed_letters.add(letter)

        if letter not in self.chosen_movie:
            self.remaining_attempts -= 1

        self.word_label.config(text=self.get_display_word())
        self.draw_hangman()

        if self.is_won():
            messagebox.showinfo("Congratulations!", "You've guessed the movie!")
        elif self.remaining_attempts == 0:
            self.draw_hangman()  # Final draw if lost

    def get_display_word(self):
        """Return the current state of the guessed word, keeping spaces visible."""
        return ' '.join(letter if letter in self.guessed_letters or letter == ' ' else '_' for letter in self.chosen_movie)

    def is_won(self):
        """Check if the player has won."""
        return all(letter in self.guessed_letters or letter == ' ' for letter in self.chosen_movie)

    def reset_game(self):
        """Reset the game to play again."""
        self.chosen_movie = random.choice(self.movies).upper()
        self.guessed_letters.clear()
        self.remaining_attempts = 6
        self.word_label.config(text=self.get_display_word())
        self.draw_hangman()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

