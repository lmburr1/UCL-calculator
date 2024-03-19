import random
import math
import csv

class Team:
    """represents a team/football club

    attributes: name (str), rating (int), results (list)
    """

def ingest_teams(list_text):
    group_list = []
    dummy_list = []
    with open(list_text, 'r') as f:
        dummy_list = f.read().splitlines()
    for item in dummy_list:
        group_list.append(item.split(","))

    return group_list

def elo_calc(home_team, away_team):
    outcomes = []
    home_win = (1/(1+pow(10,((away_team.rating - home_team.rating - 100)/400))))**2
    away_win = (1/(1+pow(10,((home_team.rating - away_team.rating + 100)/400))))**2
    draw = 1 - home_win - away_win
    
# adding 100 to the elo calculation to account for home field advantage    
    
    outcomes.append(home_win)
    outcomes.append(draw)
    outcomes.append(away_win)
    return outcomes

def elo_update(home_team, away_team, match_result):
    match_eo_h = (1/(1+pow(10,((away_team.rating - home_team.rating - 100)/400))))
    match_eo_a = (1/(1+pow(10,((home_team.rating - away_team.rating + 100)/400)))) 

# adding 100 to the elo calculation to account for home field advantage

    if match_result == 1:
        away_out = 0
    elif match_result == 0:
        away_out = 1
    else:
        away_out = match_result

    home_team.rating = home_team.rating + 5* (match_result - match_eo_h)
    away_team.rating = away_team.rating + 5* (away_out - match_eo_a)

    return None

def play_match(home_team, away_team):
    match_odds = elo_calc(home_team, away_team)
    result_decider = random.randint(0, 1000)
    result_decider = result_decider/1000
    if result_decider <= match_odds[0]:
        result = 1.0
        home_team.results.append(1.0)
        away_team.results.append(0.0)
    elif result_decider <= (match_odds[0] + match_odds[1]):
        result = 0.5
        home_team.results.append(0.5)
        away_team.results.append(0.5)
    else:
        result = 0.0
        home_team.results.append(0.0)
        away_team.results.append(1.0)

    return result

def create_group_table(list_of_teams):
    i = 0
    results_table = []
    while i < len(list_of_teams):
        points = 0
        j = 0
        while j < len(list_of_teams[i].results):
            if list_of_teams[i].results[j] ==1:
                points +=3
            elif list_of_teams[i].results[j] == 0.5:
                points +=1

            j+=1
        results_table.append((points, list_of_teams[i].name))
        list_of_teams[i].results.clear()
        i+=1

    results_table.sort(reverse=True)

    return results_table

def store_positions(group_table, store_table):
    #group_table should be a list of tuples containing points and teams
    #sorted in descending order by points

    #store_table is a matrix with team names and their positions in the table
    #over multiple simulations

    if not store_table:
        for team in group_table:
            store_table.append([])
        i =0
        while i < len(store_table):
            store_table[i].append(group_table[i][1])
            i+=1

    for team in group_table:
        i =0
        while i < len(store_table):
            if store_table[i][0] == team[1]:
                store_table[i].append(group_table.index(team) +1)
                break
            else:
                i +=1

    return store_table

def heatmap(l_rin):
    heatmap = []

    for team in l_rin:
        heatmap.append([team[0]])
    i = 0
    while i < len(l_rin):
        first = l_rin[i].count(1)
        heatmap[i].append(first/(len(l_rin[i])-1))

        second = l_rin[i].count(2)
        heatmap[i].append(second/(len(l_rin[i])-1))

        third = l_rin[i].count(3)
        heatmap[i].append(third/(len(l_rin[i])-1))

        fourth = l_rin[i].count(4)
        heatmap[i].append(fourth/(len(l_rin[i])-1))

        i+=1

    return heatmap

def run_the_matches(group_list):
    i = 0
    while i < len(group_list):
        current_team = group_list.pop(0)
        for team in group_list:
            match_result = play_match(current_team, team)
            elo_update(current_team, team, match_result)
            
        group_list.append(current_team)
        i +=1
    return None

def main():
    groups2324 = ingest_teams('football_clubs.txt')
    fields = ['team', '1st','2nd','3rd', '4th']


    letters_list = []
    list_of_groups = []
    for group in groups2324:
        if group[0] not in letters_list:
            letters_list.append(group[0])
    for letter in letters_list:
        list_of_groups.append([])
    for team in groups2324:
        new_team = Team()
        new_team.name = team[1]
        new_team.rating = int(team[2])
        new_team.results = []
        for letter in letters_list:
            if team[0] == letter:
                list_of_groups[letters_list.index(letter)].append(new_team)

# defines an 8x4 matrix of team objects, organized by group

# -- begin test case with group B
    # group_tables =[]
    # i = 0
    # while i < 1000:
    #     run_the_matches(list_of_groups[1])
    #     groupB = create_group_table(list_of_groups[1])
    #     store_positions(groupB, group_tables)
    #     i+=1
    # #print(group_tables)
    # rout = heatmap(group_tables)

    # with open('heatmap.csv', 'w') as fout:
    #     csvwriter = csv.writer(fout)
    #     csvwriter.writerow(fields)
    #     for team in rout:
    #         csvwriter.writerow(team)

# -- end test case
    
    group_tables = []
    final_map = []
    for letter in letters_list:
        i = 0
        while i < 100:
            run_the_matches(list_of_groups[letters_list.index(letter)])
            group_i = create_group_table(list_of_groups[letters_list.index(letter)])
            store_positions(group_i, group_tables)
            i+=1
        final_map.append(heatmap(group_tables))
        group_tables.clear()

    with open('heatmap.csv', 'w', newline='') as fout:
        csvwriter = csv.writer(fout)
        csvwriter.writerow(fields)
        for maps in final_map:
            for team in maps:
                csvwriter.writerow(team)
            csvwriter.writerow('\n')

    return None

if __name__ == '__main__':
    main()