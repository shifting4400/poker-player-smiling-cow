import collections

class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        player = game_state['players'][game_state['in_action']]
        cards = player['hole_cards']
        cards += player['community_cards']

        counter = Counter()
        for card in cards:
            counter[card['rank']] += 1

        for i in range(2, 10) + ['J', 'K', 'Q', 'A']:
            if counter[str(i)] > 1:
                return 1200

        return 0

    def showdown(self, game_state):
        pass

