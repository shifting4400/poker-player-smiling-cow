import collections

class Player:
    VERSION = "Default Python folding player"

    def min_bet(self, game_state, player):
        try:
            return game_state["current_buy_in"] - player['bet'] + game_state['minimum_raise']
        except:
            return 100

    def betRequest(self, game_state):
        try:
            player = game_state['players'][game_state['in_action']]
            cards = player['hole_cards']
            cards += game_state['community_cards']

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
                return self.min_bet(game_state, player)
            elif highest_card_count > 2 or self.flush(cards) or self.straight(cards):
                return 1500

            if len(game_state['community_cards']) == 0 and (cards[0]['rank'] in range(10, 15)
                    or cards[1]['rank'] in range(10, 15)):

                return self.min_bet(game_state, player)

        except Exception as e:
            print('Fatal error')
            print(str(e))
            return 0

        return 0

    def showdown(self, game_state):
        pass

    def straight(self, cards):
        ranks = set(map(lambda x: x['rank'], cards))

        if len(ranks) < 5:
            return False

        if 14 in ranks and 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks:
            return True

        for rank in ranks:
            if rank + 1 in ranks and rank + 2 in ranks and rank + 3 in ranks and rank + 4 in ranks:
                return True

        return False
    
    def flush(self, cards):
        suits = collections.Counter()

        for card in cards:
            suits[card['suit']] += 1

        for suit, count in suits.items():
            if count > 4:
                return True

        return False

