#! /usr/bin/python

# This is a text based blackjack game with betting
# Regular win pays back bet and blackjack pays double and tie pays back to normal
# By Nico Mihalich, 2008
#################################################################################
# For dealing
from random import *
# To close program
import sys
# For string manipulation
import string
# For clearing term
import curses
# Creates a card with a suit and value
class Card:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2","3","4","5","6","7","8","9","Ten","Jack","Queen","King","Ace"]
    def __init__(self, value, suit):
        self.value, self.suit = value, suit
    def __str__(self):
        return self.values[self.value] + " of " + self.suits[self.suit] 
# Creates a 52 card deck with ability to deal from deck
class Deck:
    def __init__(self):
        self.cards = []
        for x in range(13):
            for y in range(4):
                self.cards.append(Card(x, y))
    def __str__(self):
        return self.cards
    def deal(self, handsize):
        dealtcards = []
        for i in range(handsize):
            dealtcards.append(str(self.cards[randrange(52)]))
        return dealtcards
    def printdeck(self):
        for card in self.cards:
            print card
# Player class with name, chips etc.
class Player:
    def __init__(self, name = "Player"):
        self.hand = []
        self.name = name
        self.chips = 100
        self.score = 0
    def getchips(self):
        return self.chips
    def sethand(self, card):
        self.hand.append(card)
    def gethand(self):
        return self.hand
    def setchips(self, add):
        self.chips = self.chips + add
    def setname(self):
        self.name = raw_input("What is your name? ")
    def getname(self):
        return self.name
    def setscore(self):
        self.score = self.score + 1
    def getscore(self):
        return self.score
    def clearhand(self):
        self.hand = []
class Dealer:
    def __init__(self):
        self.hand = []
        self.name = "The Dealer"
        self.score = 0
    def getname(self):
        return self.name
    def sethand(self,card):
        self.hand.append(card)
    def gethand(self):
        return self.hand
    def setscore(self):
        self.score = self.score + 1
    def getscore(self):
        return self.score
    def clearhand(self):
        self.hand = []
# Main game class
class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.thedealer = Dealer()
        self.humanplayer = Player()
    def intro(self):
        print "Welcome to Blackjack!"
        self.humanplayer.setname()
    def replay(self):
        print "The score is >>"
        print str(self.thedealer.getname()) + ": " + str(self.thedealer.getscore())
        print str(self.humanplayer.getname()) + ": " + str(self.humanplayer.getscore())
        print "You now have " + str(self.humanplayer.getchips()) + " chips."
        if self.humanplayer.getchips() == 0:
            print "You are broke!"
            print "Come again soon!"
            sys.exit()
        wanttoreplay = raw_input("Want to play again? (y/q) ")
        if wanttoreplay == "y":
            ## FROM http://swapoff.org/wiki/blog/2006-11-01-terminal-manipulation-in-python
            curses.setupterm()
            # Escape sequence used to clear the terminal
            clear = curses.tigetstr('clear')
            sys.stdout.write(clear)
            ## End citation
            self.playgame()
        else:
            print "Goodbye"
            sys.exit()
    def checkresults(self, totalofhand, dealertotal, bet):
        # Checks who won the hand
        if totalofhand > 21:
            print "You have " + str(totalofhand)
            print self.thedealer.getname() + " has " + str(dealertotal)
            print "Bust..."
            self.thedealer.setscore()
            self.replay()
        if dealertotal > 21:
            print "You have " + str(totalofhand)
            print self.thedealer.getname() + " has " + str(dealertotal)
            print "Dealer busts!"
            self.humanplayer.setscore()
            self.humanplayer.setchips(2*bet)
            self.replay()
        if totalofhand == dealertotal:
            print "You both have " + str(totalofhand)
            print "It is a tie!"
            self.humanplayer.setchips(bet)
            self.thedealer.setscore()
            self.humanplayer.setscore()
            self.replay()
        if totalofhand == 21:
            print "You have " + str(totalofhand)
            print self.thedealer.getname() + " has " + str(dealertotal)
            print "BLACKJACK!"
            self.humanplayer.setchips(3*bet)
            self.humanplayer.setscore()
            self.replay()
        if totalofhand > dealertotal:
            print "You have " + str(totalofhand)
            print self.thedealer.getname() + " has " + str(dealertotal)
            print "You win!"
            self.humanplayer.setchips(2*bet)
            self.humanplayer.setscore()
            self.replay()
        if totalofhand < dealertotal:
            print "You have " + str(totalofhand)
            print self.thedealer.getname() + " has " + str(dealertotal)
            print "You lose..."
            self.thedealer.setscore()
            self.replay()
    def totalhand(self, cardstototal):
        # Totals entire hand
        playertotal = 0
        for i in [0,1]:
            firstcard = str(cardstototal[i])[2]
            if firstcard == "K":
                firstcard = 10
            elif firstcard == "Q":
                firstcard = 10
            elif firstcard == "J":
                firstcard = 10
            elif firstcard == "T":
                firstcard = 10
            elif firstcard == "A":
                firstcard = 11
            else:
                firstcard = int(firstcard)
            playertotal = playertotal + firstcard
        return playertotal
    def totalshowing(self, cardtototal):
        # Totals showing card of dealer
        onlycard = str(cardtototal[0])[2]
        if onlycard == "K":
            onlycard = 10
        elif onlycard == "Q":
            onlycard = 10
        elif onlycard == "J":
            onlycard = 10
        elif onlycard == "T":
            onlycard = 10
        elif onlycard == "A":
            onlycard = 11
        else:
            onlycard = int(onlycard)
        return onlycard
    def hit(self, total, player, cardstocount):
        # Hits one card and totals
        newcard = self.deck.deal(1)
        hitcard = str(newcard[0])[0]
        if player == "You":
            self.humanplayer.sethand(newcard)
        if player == "The Dealer":
            self.thedealer.sethand(newcard)
        if hitcard == "K":
            hitcard = 10
        elif hitcard == "Q":
            hitcard = 10
        elif hitcard == "J":
            hitcard = 10
        elif hitcard == "T":
            hitcard = 10
        elif hitcard == "A":
            hitcard = 11
        else:
            hitcard = int(hitcard)
        newtotal = total + hitcard
        acecount = self.countaces(cardstocount)
        if (newtotal > 21 and acecount >=1):
            newtotal = newtotal - 10
        return player + " were dealt a " + str(newcard) + " The hand totals " + str(newtotal) + " ."
    def countaces(self, hand):
        # Counts aces so they can go from 11-1 if needed
        hand2 = str(hand)
        aces = int(hand2.count("A"))
        return aces
    def playgame(self):
        # Main game sequence
        self.humanplayer.clearhand()
        self.thedealer.clearhand()
        self.humanplayer.sethand(self.deck.deal(1))
        self.thedealer.sethand(self.deck.deal(1))
        self.humanplayer.sethand(self.deck.deal(1))
        self.thedealer.sethand(self.deck.deal(1))
        NT2 = self.totalhand((self.humanplayer.gethand()))
        dealertotal = self.totalhand(self.thedealer.gethand())
        showingtotal = self.totalshowing(self.thedealer.gethand())
        playeraces = self.countaces(self.humanplayer.gethand())
        dealeraces = self.countaces(self.thedealer.gethand())
        print "You have " + str(self.humanplayer.getchips()) + " chips."
        chiploop = 0
        while chiploop == 0:
            try:
                moneybet = input("How much do you want to bet? ")
                # Ensures bet amount is not greater than amount that you have
                while moneybet > self.humanplayer.getchips():
                    print "You don't have that much money..."
                    moneybet = input("How much do you want to bet? ")
                chiploop = 1
                while moneybet <=0:
                    print "You have to bet something! "
                    moneybet = input("How much do you want to bet? ")
            except NameError:
                print "Please enter a number..."
                chiploop = 0
            except SyntaxError:
                print "Please enter a number..."
                chiploop = 0
        self.humanplayer.setchips((0-moneybet))
        print "Dealing..."
        print "You hold " + str(self.humanplayer.gethand())
        print "Your hand totals "+ str(NT2)
        print self.thedealer.getname() + " shows " + str(showingtotal)
        newshowingtotal = showingtotal
        while NT2 <= 21:
            hittheguy = raw_input("Do you want to hit? (y/n) ")
            if hittheguy == "y":
                NT22 = self.hit(NT2, "You", self.humanplayer.gethand())
                print NT22
                improvedtotal = str(NT22)
                newimprovedtotal = string.split(improvedtotal)
                NT22 = str(newimprovedtotal[-2])
                NT2 = int(NT22)
                while (NT2 > 21 and self.countaces(self.humanplayer.gethand()) >=1):
                    NT2 = NT2 - 10
                if NT2 > 21:
                    print "Bust!"
                    self.thedealer.setscore()
                    self.replay()
            else:
                break
        while dealertotal < 16:
            dealertotal2 = self.hit(dealertotal, str(self.thedealer.getname()), self.thedealer.gethand())
            hitcard = string.split(str(self.thedealer.gethand()))
            hitcard2 = hitcard[-3:]
            improveddt = str(dealertotal2)
            NIDT = string.split(improveddt)
            NDT2 = str(NIDT[-2])
            dealertotal = int(NDT2)
      
            print self.thedealer.getname() + " hits a " + str(str(string.join(hitcard[-3:])))
            while (newshowingtotal > 21 and self.countaces(self.thedealer.gethand()) >=1):
                newshowingtotal = newshowingtotal - 10
            newshowingtotal = newshowingtotal + int(self.totalshowing(hitcard2))
            if newshowingtotal > 21:
                print self.thedealer.getname() + " busts!"
                self.humanplayer.setscore()
                self.replay()
            else:
                print self.thedealer.getname() + " shows " + str(newshowingtotal)
        self.checkresults(NT2, dealertotal, moneybet)
    
def main():
    game = Blackjack()
    game.intro()
    game.playgame()
if __name__ == '__main__':
    main()
