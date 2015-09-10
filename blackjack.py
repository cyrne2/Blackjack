# Rice University - Blackjack
#Simple blackjack with classes
#If you tie, you lose the round. If you deal without playing you lose the round.
#Modified outside of codeskulptor by adding pillow for images (pip install image)
#Modified outside of codeskulptor by importing simpleguitk to access
#simplegui files from codeskulptor
import simpleguitk as simplegui
import random


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], 
                                                             pos[1] + CARD_CENTER[1]], CARD_SIZE)     
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        string_card = ""
        for card in self.hand:
            string_card += str(card) + " "
        return "Hand contains " + string_card
       
    def add_card(self, card):# add a card object to a hand
        self.hand.append(card)# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        ace = False
        for amount in self.hand:
            value += VALUES.get(amount.get_rank())
            if amount.get_rank() == "A":
                ace = True
        if ace and value <= 11:
            value += 10
        return value    
                
    def draw(self, canvas, pos):
        for card in self.hand:
            pos[0] = pos[0] + CARD_SIZE [0]+ 10
            card.draw(canvas, pos)# draw a hand on the canvas, use the draw method for cards
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck) 
            # use random.shuffle()

    def deal_card(self):
            # deal a card object from the deck
        return self.deck.pop(0)
        #return self.deck[0]
    
    def __str__(self):
        deck_string = ""
        for card in self.deck:
            deck_string += str(card) + " "
        return "Deck contains: " + deck_string 	# return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play, my_hand, dealer_hand, deck, score
    if in_play:
        score -= 1
    if not in_play:
        in_play = True
        outcome = "Hit or stand?"
        deck = Deck()
        deck.shuffle()
        my_hand = Hand()
        dealer_hand = Hand()
        for card in range(2):
            my_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
def hit():
    global outcome, in_play, my_hand, dealer_hand, deck, score
    if in_play:
        if my_hand.get_value() <= 21:
            my_hand.add_card(deck.deal_card())
            if my_hand.get_value() > 21:
                outcome = "BUSTED! You lose New deal?"
                in_play = False
                score -= 1
    
def stand():
    global outcome, in_play, my_hand, dealer_hand, deck, score
    if not in_play: outcome = "Sorry, round over"
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer BUST! You Win! New deal?"
            in_play = False
            score += 1
        elif my_hand.get_value() > dealer_hand.get_value():
            outcome = "You win! New deal?"
            score += 1
            in_play = False
        else:
            outcome = "You lose :( New deal?"
            score -= 1
            in_play = False
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack" , (200, 70), 50, "Blue")
    canvas.draw_text(("Outcome: "+ str(outcome)), (100, 150), 25, "DeepPink")
    canvas.draw_text(("Score: " + str(score)), (100, 525), 30, "DeepPink")
    my_hand.draw(canvas, [15, 200])
    dealer_hand.draw(canvas, [15, 350])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, 
                          CARD_BACK_SIZE, (CARD_BACK_CENTER[1] + 85, 398), CARD_BACK_SIZE)
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Silver")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
