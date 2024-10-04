import tkinter as tk
from tkinter import messagebox
import random

class BattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kahraman Savaşları")
        self.root.geometry("400x400")
        self.root.configure(bg="#333333")
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10, bg="#333333")
        self.frame.pack(pady=20)

        self.label1 = tk.Label(self.frame, text="İlk kahramanın ismini giriniz:", bg="#333333", fg="white", font=("Helvetica", 12))
        self.label1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.entry1 = tk.Entry(self.frame, font=("Helvetica", 12))
        self.entry1.grid(row=0, column=1, padx=10, pady=5)
        
        self.label2 = tk.Label(self.frame, text="İkinci kahramanın ismini giriniz:", bg="#333333", fg="white", font=("Helvetica", 12))
        self.label2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.entry2 = tk.Entry(self.frame, font=("Helvetica", 12))
        self.entry2.grid(row=1, column=1, padx=10, pady=5)
        
        self.start_button = tk.Button(self.frame, text="Oyunu Başlat", command=self.start_game, bg="#007acc", fg="white", font=("Helvetica", 12), width=20)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.attack_label = tk.Label(self.frame, text="Saldırı büyüklüğünüzü 1 ile 50 arasında seçin:", bg="#333333", fg="white", font=("Helvetica", 12))
        self.attack_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.attack_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.attack_entry.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.attack_button = tk.Button(self.frame, text="Saldır!", command=self.attack, bg="#007acc", fg="white", font=("Helvetica", 12), width=20)
        self.attack_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.result_label = tk.Label(self.frame, text="", bg="#333333", fg="white", font=("Helvetica", 12))
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def reset_game(self):
        self.player1_name = ""
        self.player2_name = ""
        self.player1_hp = 100
        self.player2_hp = 100
        self.turn = 1
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.attack_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def start_game(self):
        self.player1_name = self.entry1.get()
        self.player2_name = self.entry2.get()
        
        if self.player1_name == self.player2_name:
            messagebox.showerror("Hata", "Kahramanlar aynı isimde olamaz")
            return
        
        self.turn = random.randint(1, 2)
        first_player = self.player1_name if self.turn == 1 else self.player2_name
        self.result_label.config(text=f"Yazı tura sonucu: {first_player} önce başlar!")
        
        self.attack_entry.delete(0, tk.END)
        self.update_turn_display()

    def attack(self):
        try:
            attack_size = int(self.attack_entry.get())
            if attack_size < 1 or attack_size > 50:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen 1 ile 50 arasında bir sayı girin")
            return
        
        if self.turn == 1:
            self.player2_hp = self.calculate_damage(attack_size, self.player2_hp)
            self.turn = 2
        else:
            self.player1_hp = self.calculate_damage(attack_size, self.player1_hp)
            self.turn = 1

        self.attack_entry.delete(0, tk.END)
        self.update_hp_display()
        self.update_turn_display()
        self.check_winner()

    def calculate_damage(self, percentage, player_hp):
        random_value = random.randint(1, 100)
        if random_value < (100 - percentage):
            return player_hp - percentage
        return player_hp

    def update_hp_display(self):
        player1_hp_display = self.get_hp_bar(self.player1_hp)
        player2_hp_display = self.get_hp_bar(self.player2_hp)
        self.result_label.config(
            text=f"{self.player1_name}\t\t\t\t\t\t\t\t{self.player2_name}\n"
                 f"HP[{self.player1_hp}]:{player1_hp_display}\t"
                 f"HP[{self.player2_hp}]:{player2_hp_display}"
        )

    def get_hp_bar(self, hp_value):
        hp_bar = ""
        for _ in range(1, int(hp_value / 2)):
            hp_bar += "|"
        return hp_bar

    def update_turn_display(self):
        current_turn_player = self.player1_name if self.turn == 1 else self.player2_name
        self.result_label.config(
            text=self.result_label.cget("text") + f"\nSıradaki: {current_turn_player}"
        )

    def check_winner(self):
        if self.player1_hp <= 0 or self.player2_hp <= 0:
            winner = self.player1_name if self.player1_hp > 0 else self.player2_name
            messagebox.showinfo("Oyun Bitti", f"{winner} kazandı!")
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleGame(root)
    root.mainloop()
