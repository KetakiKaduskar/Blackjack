import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from package.gameLogic import determineWinner


class BettingAppGUI(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self["style"] = "Custom.TFrame"
        self.columnconfigure(0, weight=1)
        self.container = container
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        
        self.bank_label = ttk.Label(self, text=f"Bank: ${self.controller.pl.bank}", padding=20, style="Custom.TLabel")
        
        self.bank_label.grid(row=0, column=0, sticky="S")
        
        self.bet_label = ttk.Label(self, text="Your Bet: $0", padding=20, style="Custom.TLabel")
        self.bet_label.grid(row=1, column=0)
        
        deal_btn = ttk.Button(self, text="Deal", command=lambda: self.showGameFrame(), style='Custom.TButton')
        deal_btn.grid(row=3, column=0, sticky="N", pady=10)

        self.buttons_frame = ttk.Frame(self, style='Custom.TFrame', padding=20)
        self.buttons_frame.grid(row=2, column=0, sticky="N")

        self.create_buttons()
        

    def showGameFrame(self):
        gameFrame = GameInterfaceGUI(self.container, self.controller, self)
        gameFrame.configure(height=910)
        self.controller.frames[BettingAppGUI] = gameFrame
        gameFrame.grid(row=0, column=0, sticky="nsew")


    def create_buttons(self):
        amounts = [1, 5, 25, 50, 100, 500, 1000]
        self.buttons = []
        for i, amount in enumerate(amounts):
            btn = ttk.Button(self.buttons_frame, text=str(amount), command=lambda a=amount: self.place_bet(a), style='Custom.TButton')
            
            btn.grid(row=0, column=i, padx=5)
            
            self.buttons.append(btn)
            if self.controller.bank_value < amount:
                self.buttons[i].config(state=tk.DISABLED)
        

    def place_bet(self, amount):
        if self.controller.bank_value - amount >= 0:
            self.controller.bank_value -= amount
            self.controller.bet_amount += amount
            self.controller.hasBetBeenPlaced = True
            self.update_labels()
            self.check_bank_value()
        else:
            print("Insufficient funds")
    

    def update_labels(self):
        self.check_bank_value()
        self.bank_label_text = f"Bank: ${self.controller.bank_value}"
        self.bank_label["text"] = self.bank_label_text
        self.bet_label_text = f"Your Bet: ${self.controller.bet_amount}"
        self.bet_label["text"] = self.bet_label_text
    

    def check_bank_value(self):
        for i, amount in enumerate([1, 5, 25, 50, 100, 500, 1000]):
            if self.controller.bank_value - amount < 0:
                self.buttons[i].config(state=tk.DISABLED)
            else:
                self.buttons[i].config(state=tk.NORMAL)


class GameInterfaceGUI(ttk.Frame):
    def __init__(self, container, controller, bettingAppInstance, **kwargs):
        super().__init__(container, **kwargs)
        self.bettingAppInstance = bettingAppInstance
        self.controller = controller
        self.isGameOver = False
        self.create_widgets()
        self.custom_style = ttk.Style()
        self.custom_style.configure('Custom.TButton', font=('Arial', 12), background="#007700")
        self.custom_style.configure('Custom.TFrame', background='#007700', foreground='#FFFFFF')


    def create_widgets(self):
        self.dealerFrame = ttk.Frame(self, style='Custom.TFrame')
        self.dealerFrame.place(relx=0, rely=0, relheight=0.4, relwidth=1)

        self.playerFrame = ttk.Frame(self, style='Custom.TFrame')
        self.playerFrame.place(relx=0, rely=0.55, relheight=0.45, relwidth=1)

        self.middleFrame = ttk.Frame(self, style='Custom.TFrame')
        self.middleFrame.place(relx=0, rely=0.4, relheight=0.15, relwidth=1)

        self.hitButton = ttk.Button(self.middleFrame, text='Hit', command=self.hitPressed, style='Custom.TButton')
        self.hitButton.place(rely=0.5, relx=0.17, anchor='center')

        self.standButton = ttk.Button(self.middleFrame, text='Stand', command=self.standPressed, style='Custom.TButton')
        self.standButton.place(rely=0.5, relx=0.82, anchor='center')

        self.bankLabel = ttk.Label(self.playerFrame, text="Bank: $", style='Custom.TLabel')
        self.bankLabel.place(anchor='sw', relx=0, rely=1)    
        self.update_bank_label_text(self.controller.bank_value)   

        self.playerValueLabel = ttk.Label(self.playerFrame, text=f"Player: {self.controller.pl.getPlayerHandValue()}", style='Custom.TLabel')
        self.playerValueLabel.place(rely=0.5, relx=0.82, anchor='center')

        self.dealerValueLabel = ttk.Label(self.dealerFrame, text=f"Dealer: {self.controller.pl.getDealerHandValue()}", style='Custom.TLabel')
        self.dealerValueLabel.place(rely=0.5, relx=0.82, anchor='center')

        self.deal_initial_cards()

        self.controller.roundComplete = True


    def placeNextButton(self):
        nextRoundButton = ttk.Button(self.middleFrame, text='Next Round', command=self.showBetFrame, style='Custom.TButton')
        nextRoundButton.place(rely=0.5, relx=0.65, anchor='center')


    def disableButtons(self):
        self.hitButton.config(state=tk.DISABLED)
        self.standButton.config(state=tk.DISABLED)


    def updateDealerValue(self):
        self.dealerValueLabel["text"] = f"  Dealer: {self.controller.pl.getDealerHandValue()}"


    def updatePlayerValue(self):
        self.playerValueLabel["text"] = f"Player: {self.controller.pl.getPlayerHandValue()}"
        

    def displayWinner(self):
        winner = determineWinner(self.controller.pl.getPlayerHandValue(), self.controller.pl.getDealerHandValue())

        result = ttk.Label(self.middleFrame, text=f"{winner}", style='Custom.TLabel')
        result.place(rely=0.4, relx=0.5, anchor='center')
        
        if self.controller.hasBetBeenPlaced:
            if winner == "Push":
                self.push()
            elif winner == "Player wins!":
                self.playerWins()
            elif winner == "Dealer wins!":
                self.dealerWins()
            else:
                self.dealerBusts()

        self.controller.bet_amount = 0
        self.bettingAppInstance.update_labels()

        if self.controller.bank_value > 0 and self.isGameOver == False:
            self.placeNextButton()


    def update_bank_label_text(self, new_bank_value):
        self.bank_label_text = f"Bank: ${new_bank_value}"
        self.bankLabel["text"] = self.bank_label_text
    
    
    def dealerTurn(self):
        while self.controller.pl.getDealerHandValue() < 17:
            self.controller.pl.addDealCard()
            lenDealHand = len(self.controller.pl.dealhand)
        
            self.hitdealerCard = [0,1,2,3,4,5,6,7]
        
            self.hitDealrelxInit = 0.55
            for i in range(1, lenDealHand):
                self.hitimage = Image.open(f"./package/cards/{self.controller.pl.dealhand[i]}.png").resize((100, 160))
                self.hitdealerCard[i] = ImageTk.PhotoImage(self.hitimage)
                if i < 6:
                    ttk.Label(self.dealerFrame, image=self.hitdealerCard[i], style='Custom.TLabel').place(rely=0.5, relx=self.hitDealrelxInit-(i*0.1), anchor='center')
                else:
                    self.hitDealrelxInit = 0.05
                    ttk.Label(self.dealerFrame, image=self.hitdealerCard[i], style='Custom.TLabel').place(rely=0.5, relx=self.hitDealrelxInit+(i*0.1), anchor='center')

            self.updateDealerValue()

            if self.controller.pl.getDealerHandValue() > 21:
                break


    def deal_initial_cards(self):
        self.relxInit = 0.55
        self.playerCard = [0, 1]

        for i in range(2):
            self.image = Image.open(f"./package/cards/{self.controller.pl.playhand[i]}.png").resize((100, 160))
            self.playerCard[i] = ImageTk.PhotoImage(self.image)
            ttk.Label(self.playerFrame, image=self.playerCard[i], style='Custom.TLabel').place(rely=0.5, relx=self.relxInit-(i*0.1), anchor='center')

        self.dealerCard = [0]

        self.image = Image.open(f"./package/cards/{self.controller.pl.dealhand[0]}.png").resize((100, 160))
        self.dealerCard[0] = ImageTk.PhotoImage(self.image)
        ttk.Label(self.dealerFrame, image=self.dealerCard[0], style='Custom.TLabel').place(rely=0.5, relx=0.55, anchor='center')

        self.image = Image.open("./package/cards/back.png").resize((100, 160))
        self.backCard = ImageTk.PhotoImage(self.image)
        ttk.Label(self.dealerFrame, image=self.backCard, style='Custom.TLabel').place(rely=0.5, relx=0.45, anchor='center')

        self.updatePlayerValue()
        if self.controller.pl.getPlayerHandValue() == 21:
            self.blackjack()
            self.controller.bet_amount = 0
            self.bettingAppInstance.update_labels()
        self.updateDealerValue()


    def amountGainedPlace(self, labelTextAmount):
        amountGained = ttk.Label(self.middleFrame, text=f"+{labelTextAmount}", style='Custom.TLabel')
        amountGained.place(rely=0.65, relx=0.5, anchor='center')


    ### Buttons Pressed ###


    def showBetFrame(self):
        self.controller.bettingFrame.tkraise()
        self.controller.pl.newRoundHand()


    def standPressed(self):
        self.disableButtons()
        self.dealerTurn()
        self.displayWinner()

    def hitPressed(self):
        self.controller.pl.addPlayCard()
        lenPlayHand = len(self.controller.pl.playhand)
        
        self.hitplayerCard = [0,1,2,3,4,5,6,7]
        
        self.hitrelxInit = 0.55
        for i in range(2, lenPlayHand):
            self.hitimage = Image.open(f"./package/cards/{self.controller.pl.playhand[i]}.png").resize((100, 160))
            self.hitplayerCard[i] = ImageTk.PhotoImage(self.hitimage)
            if i < 6:
                ttk.Label(self.playerFrame, image=self.hitplayerCard[i], style='Custom.TLabel').place(rely=0.5, relx=self.hitrelxInit-(i*0.1), anchor='center')
            else:
                self.hitrelxInit = 0.05
                ttk.Label(self.playerFrame, image=self.hitplayerCard[i], style='Custom.TLabel').place(rely=0.5, relx=self.hitrelxInit+(i*0.1), anchor='center')

        self.updatePlayerValue()

        if self.controller.pl.getPlayerHandValue() == 21:
            self.blackjack()
            self.controller.bet_amount = 0
            self.bettingAppInstance.update_labels()
        elif self.controller.pl.getPlayerHandValue() > 21:
            self.playerBust()
            self.controller.bet_amount = 0
            self.bettingAppInstance.update_labels()


    ### Possible Outcomes ###
        

    def dealerBusts(self):
        self.disableButtons()
        result = ttk.Label(self.middleFrame, text="Dealer Busts", style='Custom.TLabel')
        result.place(rely=0.4, relx=0.5, anchor='center')
        self.controller.bank_value = self.controller.bank_value + (2 * self.controller.bet_amount)
        self.update_bank_label_text(self.controller.bank_value)
        self.amountGainedPlace(2 * self.controller.bet_amount)
        
        self.placeNextButton()


    def push(self):
        self.controller.bank_value = self.controller.bank_value + self.controller.bet_amount
        self.update_bank_label_text(self.controller.bank_value)

        self.amountGainedPlace(self.controller.bet_amount)


    def playerWins(self):
        self.controller.bank_value = self.controller.bank_value + (2 * self.controller.bet_amount)
        self.update_bank_label_text(self.controller.bank_value)

        self.amountGainedPlace(2 * self.controller.bet_amount)


    def dealerWins(self):
        if self.controller.bank_value >= 1:
            self.update_bank_label_text(self.controller.bank_value)
        else:
            self.gameOverFunc()
            

    def gameOverFunc(self):
        self.isGameOver = True
        self.controller.bank_value = 0
        self.update_bank_label_text(self.controller.bank_value)
        gameOver = ttk.Label(self.middleFrame, text="Game Over", style='Custom.TLabel')
        gameOver.place(rely=0.75, relx=0.5, anchor='center')

        self.controller.bank_value = self.controller.initial_bank_value
        self.controller.bet_amount = 0
        self.bettingAppInstance.update_labels()
        newGameButton = ttk.Button(self.middleFrame, text="New Game", command=self.showBetFrame, style='Custom.TButton')
        newGameButton.place(rely=0.5, relx=0.65, anchor='center')


    def blackjack(self):
        self.disableButtons()
        Blackjack = ttk.Label(self.middleFrame, text="Blackjack", style='Custom.TLabel')
        Blackjack.place(rely=0.4, relx=0.5, anchor='center')
        self.controller.bank_value = self.controller.bank_value + (2.5 * self.controller.bet_amount)
        self.update_bank_label_text(self.controller.bank_value)
        
        self.amountGainedPlace(2.5 * self.controller.bet_amount)
        
        self.placeNextButton()


    def playerBust(self):
        self.disableButtons()
        Bust = ttk.Label(self.middleFrame, text="Bust", style='Custom.TLabel')
        Bust.place(rely=0.4, relx=0.5, anchor='center')
        if self.controller.bank_value < 1:
            self.gameOverFunc()
        if self.isGameOver == False:
            self.update_bank_label_text(self.controller.bank_value)
            if self.controller.bank_value > 0:
                self.placeNextButton()