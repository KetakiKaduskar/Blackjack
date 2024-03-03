import tkinter as tk
from tkinter import ttk
from package import BettingAppGUI, Player, set_dpi_awareness


set_dpi_awareness()


class GameInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Blackjack Game")
        self.geometry("1560x910")
        self.resizable(False, False)
        self.frames = dict()

        style = ttk.Style()
        style.theme_use('vista')
        style.configure('Custom.TFrame', background='#007700', foreground='#FFFFFF')
        style.configure('Custom.TButton', font=('Arial', 12), background='#007700')
        style.configure('Custom.TLabel', background='#007700', font="Arial 14 bold")

        container = ttk.Frame(self, style="Custom.TFrame")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pl = Player()

        self.initial_bank_value = self.pl.bank

        self.bank_value = self.pl.bank
        self.bet_amount = 0

        self.hasBetBeenPlaced = False
        self.roundComplete = False

        self.bettingFrame = BettingAppGUI(container, self)
        self.bettingFrame.configure(height=910)
        self.frames[BettingAppGUI] = self.bettingFrame
        self.bettingFrame.grid(row=0, column=0, sticky="nsew")


try:
    game_interface = GameInterface()
    game_interface.mainloop()
except:
    import traceback
    traceback.print_exc()
    input("Press Enter to end...")