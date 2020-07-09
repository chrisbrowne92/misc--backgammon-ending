import numpy as np
import pandas as pd
import random

international_rules = False
C = 15
games_per_permutation = 1000

if international_rules:
    max_per_position = C
else:
    max_per_position = 5


def role():
    return sorted([random.randint(1, 6), random.randint(1, 6)], reverse=True)

def place_counter(player):
    pos = random.randint(1, 6)
    if player[pos] < max_per_position:
        player[pos] += 1
    else:
        place_counter(player)
    return player

def assign(player, num_counters):
    for c in range(num_counters):
        place_counter(player)
    return player

def play_move(player):
    dice = role()
    if dice[0] == dice[1]:  # sort out doubles
        dice = dice + dice
    for d in dice: # remove counter
        if player[d] > 0:  # if there's a counter on the position
            player[d] -= 1  # remove it
        else:  # else move a counter that's higher
            if international_rules:
                for pos in range(6, d, -1):  # go back from the 6th position
                    if player[pos] > 0:  # if there is a counter on pos
                        new_pos = pos - d  # new position if counter were to be moved
                        if new_pos < 1:  # if the roll can take the counter out
                            player[pos] -= 1  # remove it
                        else:  # if not
                            player[pos] -= 1  # move it
                            player[new_pos] += 1  # move it
                        break  # move completed
            else:
                for pos in range(6, d, -1):  # go back from the 6th position
                    new_pos = pos - d
                    if (player[pos] > 0) and (player[new_pos] < max_per_position):  # if counter on the position and next pos is available
                        player[pos] -= 1  # move it
                        player[new_pos] += 1  # move it
                        break  # move completed
    return player

def play_until(player, num_counters_remaining):
    move_count = 0
    while sum(player) > num_counters_remaining:
        play_move(player)
        move_count += 1
    return player

winner_code = {0: 'losing', 1: 'winning', -1: 'error'}

results = pd.DataFrame({'lead': [], 'itr': [], 'winner': []})

for lead in range(1, C):
    for i in range(games_per_permutation):
        winner = -1
        # distribute counters randomly in home area
        winning = assign(pd.Series(np.zeros(6), index=range(1, 7)), C)
        losing = assign(pd.Series(np.zeros(6), index=range(1, 7)), C)
        # play the winning player until they have the simulated lead
        winning = play_until(winning, C - lead)
        # take in turns to play and see who wins
        end_of_game = False
        while not end_of_game:
            random.randint(0, 1)
            winning = play_move(winning)
            if sum(winning) == 0:
                end_of_game = True
                winner = 1
            else:
                losing = play_move(losing)
                if sum(losing) == 0:
                    end_of_game = True
                    winner = 0
        won_by = abs(sum(winning) - sum(losing))
        results = pd.concat([results, pd.DataFrame({'lead': [lead],
                                                    'itr': [i],
                                                    'winner': [winner],
                                                    'won_by': [won_by]})], sort=False)
        #print('lead: ' + str(lead) + ',   itr: ' + str(i) + ',   winner: ' + winner_code[winner])
    win_rate = sum(results.loc[results['lead'] == lead, 'winner']) / games_per_permutation
    won_by_avg = results.loc[results['won_by'] == lead, 'won_by'].mean()
    print('lead: ' + str(lead) + ',   ' +
          'winning win rate: ' + str(round(win_rate, 2)) + ',   ' +
          'avg win margin: ' + str(round(won_by_avg, 2)))

    pass

