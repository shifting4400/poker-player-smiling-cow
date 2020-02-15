import collections

class Player:
    VERSION = "Default Python folding player"

    def min_bet(self, game_state, player, extra):
        mr = 0
        if 'minimum_raise' in game_state:
            mr = game_state['minimum_raise']

        extra = int((player['bet'] + player['stack']) / 100 * extra)

        if extra > mr:
            mr = extra
            
        return game_state["current_buy_in"] - player['bet'] + mr

    def betRequest(self, game_state):
        try:
            player = game_state['players'][game_state['in_action']]
            tcards = game_state['community_cards']
            cards = player['hole_cards'] + tcards
            
            cards.sort(key=lambda x: x['rank'])
            tcards.sort(key=lambda x: x['rank'])

            tcounter = collections.Counter()
            for card in tcards:
                if card['rank'] in ['J', 'K', 'Q', 'A']:
                    card['rank'] = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card['rank']]
                else:
                    card['rank'] = int(card['rank'])
                tcounter[card['rank']] += 1
            thighest_card_count = 1
            
            counter = collections.Counter()
            for card in cards:
                if card['rank'] in ['J', 'K', 'Q', 'A']:
                    card['rank'] = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card['rank']]
                else:
                    card['rank'] = int(card['rank'])
                counter[card['rank']] += 1
            highest_card_count = 1

            for rank, count in tcounter.items():
                if count > thighest_card_count:
                    thighest_card_count = count

            for rank, count in counter.items():
                if count > highest_card_count:
                    highest_card_count = count
                    
            if (highest_card_count > 3 or (self.flush(cards) and not self.flush(tcards)) or 
                (self.straight(cards) and not self.straight(tcards))):
                return self.min_bet(game_state, player, 100)
            if self.full_house(counter) and not self.full_house(tcounter):
                return self.min_bet(game_state, player, 100)
            if highest_card_count == 3 and thighest_card_count < 3:
                return self.min_bet(game_state, player, 50)
            if self.two_pairs(counter) and not self.two_pairs(tcounter):
                return self.min_bet(game_state, player, 25)
            if highest_card_count == 2 and thighest_card_count < 2:
                return self.min_bet(game_state, player, 15)

            if (thighest_card_count >= 3 or self.flush(tcards) or 
                self.straight(tcards) or self.full_house(tcounter)):

                if (player['hole_cards'][0]['rank'] in range(10, 15) or player['hole_cards'][1]['rank'] in range(10, 15)):

                    return self.min_bet(game_state, player, 2)

            if len(game_state['community_cards']) == 3 and self.almost_flush(cards) and self.dual_color(player['hole_cards']):
                return self.min_bet(game_state, player, 30)

            if len(game_state['community_cards']) == 4 and self.almost_flush(cards) and self.dual_color(player['hole_cards']):
                return self.min_bet(game_state, player, 10)

            if len(game_state['community_cards']) == 0 and ((player['hole_cards'][0]['rank'] in range(10, 15)
                    and player['hole_cards'][1]['rank'] in range(10, 15)) or 
                    (player['hole_cards'][0]['rank'] in range(10, 15)
                    or player['hole_cards'][1]['rank'] in range(10, 15)) and
                    game_state["current_buy_in"] - player['bet'] <= game_state["small_blind"]):

                #if player['bet'] == 2 * small_blind:

                return self.min_bet(game_state, player, 2)

            if (len(game_state['community_cards']) == 5 and game_state["current_buy_in"] - player['bet'] == 0
                and game_state['in_action'] == game_state['dealer'] and (player['hole_cards'][0]['rank'] in range(10, 15)
                    or player['hole_cards'][1]['rank'] in range(10, 15))):

                return self.min_bet(game_state, player, 1)

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
    
    def dual_color(self, cards):
        suits = collections.Counter()

        for card in cards:
            suits[card['suit']] += 1

        for suit, count in suits.items():
            if count >= 2:
                return True

        return False
    
    def almost_flush(self, cards):
        suits = collections.Counter()

        for card in cards:
            suits[card['suit']] += 1

        for suit, count in suits.items():
            if count > 3:
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

    def full_house(self, counter):

        for rank1, count1 in counter.items():
            for rank2, count2 in counter.items():
                if rank1 != rank2 and count1 > 2 and count2 > 1:
                    return True

        return False

    def two_pairs(self, counter):

        for rank1, count1 in counter.items():
            for rank2, count2 in counter.items():
                if rank1 != rank2 and count1 > 1 and count2 > 1:
                    return True

        return False
