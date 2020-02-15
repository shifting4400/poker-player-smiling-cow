import collections

class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        try:
            player = game_state['players'][game_state['in_action']]
            cards = player['hole_cards']
            cards += player['community_cards']

            counter = collections.Counter()
            for card in cards:
                if card['rank'] in ['J', 'K', 'Q', 'A']:
                    card['rank'] = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card['rank']]
                else:
                    card['rank'] = int(card['rank'])
                counter[card['rank']] += 1
            
            cards.sort(key=lambda x: x['rank'])

            highest_card_count = 1

            for rank, count in counter.items():
                if count > highest_card_count:
                    highest_card_count = count
                    
            if highest_card_count == 2:
                return game_state["current_buy_in"] - player['bet'] + game_state['minimum_raise']
            elif highest_card_count > 2:
                return 1500

        except:
            return 0

        return 0

    def showdown(self, game_state):
        pass

    def straight(self, cards):
        ranks = set(cards.keys())

        if len(ranks) < 5:
            return False

        return True

