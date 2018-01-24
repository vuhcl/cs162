from datetime import datetime
import itertools
# See here to understand the click library:
# http://click.pocoo.org/5/quickstart/#basic-concepts
import click

class RANDU():
    __c = 65539
    __m = 2147483648
    def __init__(self, seed = None):
        if seed is not None:
            self.seed = seed
        else: self.seed = int((datetime.utcnow() - datetime.min).total_seconds())

    def random_number(self):
        ''' Produce a random number using the Park-Miller method.

        See http://www.firstpr.com.au/dsp/rand31/ for further details of this
        method. It is recommended to use the returned value as the value for x1,
        when next calling the method.'''
        seed = abs((self.__c * self.seed) % self.__m)
        return seed

class Card():
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    ranks = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    def __init__(self, suit, rank):
        if suit not in self.suits:
            raise Exception('Invalid suit')
        if rank not in self.ranks:
            raise Exception('Invalid rank')
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return self.suit + ' of ' + self.rank

    def blackjack_value(self):
        '''Return the value of a card when in the game of Blackjack.

        Input:
            card: A string which identifies the playing card.
        Strictly speaking, Aces can be valued at either 1 or 10, this
        implementation assumes that the value is always 1, and then determines
        later how many aces can be valued at 10.  (This occurs in
        blackjack_hand_value.)
        '''
        try:
            return int(self.rank)
        except ValueError:
            if self.rank == 'Ace':
                return 1
            else:
                return 10

    def is_ace(self):
        '''Identify whether or not a card is an ace.

        Input:
            card: A string which identifies the playing card.

        Returns:
            true or false, depending on whether the card is an ace or not.
        '''
        return self.rank == 'Ace'

class Deck():
    def __init__(self):
        self.cards = [Card(suit, rank) for suit, rank in itertools.product(Card.suits, Card.ranks)]

class Hand():
    def __init__(self):
        self.cards = []

    def get_random_card_from_deck(self, deck):
        ''' This element returns a random card from a given list of cards.

        Input:
        deck: list of available cards to return.
        x1: variable for use in the generation of random numbers.
        x2: variable for use in the generation of random numbers.
        '''

        x1 = RANDU()
        card = deck.cards.pop(x1.random_number() % len(deck.cards))
        self.cards.append(card)


    def blackjack_hand_value(self):
        '''Calculate the maximal value of a given hand in Blackjack.

        Input:
            cards: A list of strings, with each string identifying a playing card.

        Returns:
            The highest possible value of this hand if it is a legal blackjack
            hand, or -1 if it is an illegal hand.
        '''
        sum_cards = sum([card.blackjack_value() for card in self.cards])
        num_aces = sum([card.is_ace() for card in self.cards])
        aces_to_use = max(int((21 - sum_cards) / 10.0), num_aces)
        final_value = sum_cards + 10 * aces_to_use
        if final_value > 21:
            return -1
        else:
            return final_value


def display(player, dealer):
    '''Display the current information available to the player.'''
    print('The dealer is showing : ' + repr(dealer.cards[0]))
    print('Your hand is :' + repr(player.cards))


def hit_me():
    '''Query the user as to whether they want another car or not.

    Returns:
        A boolean value of True or False.  True means that the user does want
        another card.
    '''
    ans = ""
    while ans.lower() not in ('y', 'n'):
        ans = input("Would you like another card? (y/n):")
    return ans.lower() == 'y'


@click.command()
@click.option(
    '--language',
    default='en',
    help='The language to play blackjack in, e.g. "en"')
def game(language):
    if language != 'en':
        raise ValueError("Language not recognized or implemented.")
    # Initialize everything

    deck = Deck()
    my_hand = Hand()
    dealer_hand = Hand()

    # Deal the initial cards
    for a in range(2):
        my_hand.get_random_card_from_deck(deck)
        dealer_hand.get_random_card_from_deck(deck)

    # Give the user as many cards as they want (without going bust).
    display(my_hand, dealer_hand)
    while hit_me():
        my_hand.get_random_card_from_deck(deck)
        display(my_hand, dealer_hand)
        if my_hand.blackjack_hand_value() < 0:
            print("You have gone bust!")
            break

    # Now deal cards to the dealer:
    print("The dealer has : " + repr(dealer_hand.cards))
    while 0 < dealer_hand.blackjack_hand_value() < 17:
        dealer_hand.get_random_card_from_deck(deck)
        print("The dealer hits")
        print("The dealer has : " + repr(dealer_hand.cards))

    if dealer_hand.blackjack_hand_value() < 0:
        print("The dealer has gone bust!")
    else:
        print('The dealer sticks with: ' + repr(dealer_hand.cards))

    # Determine who has won the game:
    my_total = my_hand.blackjack_hand_value()
    dealer_total = dealer_hand.blackjack_hand_value()
    if dealer_total == my_total:
        print("It's a draw!")
    if dealer_total > my_total:
        print("The dealer won!")
    if dealer_total < my_total:
        print("You won!")


if __name__ == '__main__':
    game()
