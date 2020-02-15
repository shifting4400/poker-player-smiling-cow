import collections

class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        try:
            player = game_state['players'][game_state['in_action']]
            cards = player['hole_cards']
            cards += player['community_cards']

            counter = Counter()
            for card in cards:
                counter[card['rank']] += 1

            highest_card_count = 1

            for i in range(2, 10) + ['J', 'K', 'Q', 'A']:
                if counter[str(i)] > highest_card_count:
                    highest_card_count = counter[str(i)]
                    
            if highest_card_count == 2:
                return game_state["current_buy_in"] - player['bet'] + game_state['minimum_raise']
            elif highest_card_count > 2:
                return 1500

        except:
            return 0

        return 0

    def showdown(self, game_state):
        pass

