def determineWinner(playerValue, dealerValue):
    if playerValue == dealerValue:
        return "Push"
    elif playerValue > dealerValue:
        return "Player wins!"
    elif dealerValue < 22:
        return "Dealer wins!"
    else:
        return "Dealer Busts"
    


if __name__ == "__main__":
    determineWinner()