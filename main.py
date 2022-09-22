import random
import statistics
from dataclasses import dataclass
from enum import Enum

CARDS_COUNT = 52
CARDS = [i for i in range(CARDS_COUNT)]
TURNS_THRESHOLD = 10000

GAMES_COUNT = 10000

DEBUG = True
DEBUG = False


def play_games():
    """ Play N games and calculate mean number of turns """
    results = [TheGame().play() for i in range(GAMES_COUNT)]
    valid_results = [r for r in results if r.end_state is not EndState.GAME_TOO_LONG]
    valid_turns = [r.turns for r in valid_results]
    avg_turns = statistics.fmean(valid_turns)
    p1_wins = sum([1 for r in valid_results if r.end_state is EndState.P1_WIN])
    p2_wins = sum([1 for r in valid_results if r.end_state is EndState.P2_WIN])

    print()
    # print(sorted(valid_turns))
    print(f'After {len(valid_results)} games with {CARDS_COUNT} cards, on average the game took {avg_turns} turns. P1 won {p1_wins} times, P2 won {p2_wins} '
          f'times.')


class EndState(Enum):
    P1_WIN = 1
    P2_WIN = 2
    GAME_TOO_LONG = 3


@dataclass(init=False)
class GameResult:
    turns: int
    strength_diff: int
    end_state: EndState = None


class TheGame:

    @staticmethod
    def play():
        deck = CARDS.copy()
        random.shuffle(deck)

        half = int(CARDS_COUNT / 2)
        p1_deck = deck[:half]
        p2_deck = deck[half:]

        TheGame.print_game_start(p1_deck, p2_deck)

        result = GameResult()
        result.strength_diff = sum(p1_deck) - sum(p2_deck)

        turns = 0
        p1_score = 0
        TheGame.print_game_state(turns, p1_deck, p2_deck, p1_score)
        while p1_deck and p2_deck:
            turns += 1

            p1_card = p1_deck.pop(0)
            p2_card = p2_deck.pop(0)

            both = [p1_card, p2_card]
            random.shuffle(both)

            p1_win = p1_card > p2_card
            p1_score += 1 if p1_win else -1
            winning_deck = p1_deck if p1_win else p2_deck
            winning_deck += both

            TheGame.print_game_state(turns, p1_deck, p2_deck, p1_score, p1_card, p2_card, p1_win)

            if turns > TURNS_THRESHOLD:
                result.end_state = EndState.GAME_TOO_LONG
                break

        result.turns = turns
        if not result.end_state:
            result.end_state = EndState.P1_WIN if not p2_deck else EndState.P2_WIN

        TheGame.print_game_end(result)
        return result

    @staticmethod
    def print_game_start(p1_deck, p2_deck):
        if not DEBUG:
            return

        p1_strength = sum(p1_deck)
        p2_strength = sum(p2_deck)
        total_strength = p1_strength + p2_strength
        strength_diff = p1_strength - p2_strength

        print(f'[Game start] with {CARDS_COUNT} total cards, {total_strength} total strength, {strength_diff} strength difference. '
              f'P1: {len(p1_deck)} cards, {p1_strength}pts {p1_deck}, '
              f'P2: {len(p2_deck)} cards, {p2_strength}pts {p2_deck}')

    @staticmethod
    def print_game_state(turns, p1_deck, p2_deck, p1_score, p1_card=None, p2_card=None, p1_win=None):
        if not DEBUG:
            return

        msg = f'{f"[Turn {turns}]":12}score {"+" if p1_score > 0 else "=" if p1_score == 0 else ""}{p1_score}, ' \
              f'deck size {len(p1_deck)}:{len(p2_deck)}'
        if p1_card is not None and p2_card is not None:
            msg += f', cards: {p1_card} vs {p2_card} ({"P1 wins" if p1_win else "P2 wins"})'
        msg += f', decks: {p1_deck} vs {p2_deck}'
        print(msg)

    @staticmethod
    def print_game_end(result):
        if not DEBUG:
            return
        print(f'{result.end_state}! The game took {result.turns} turns to end given initial strength difference of {abs(result.strength_diff)}')


if __name__ == '__main__':
    play_games()
