from itertools import combinations
import numpy as np

table = [
    ['exp1','exp2','exp3','exp4','exp5','exp6','exp7','exp8','exp9','exp10'],
    [0.9, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.6, 0.5, 0.5],
    [340, 350, 260, 220, 180, 150, 170, 120, 110, 90 ],
]
max_n = 8
min_n = 4
C_lim = 1400

def create_range_N(max_n, min_n)->list:
    N = []
    for i in range(min_n, max_n+1):
        N.append(i)
    N.reverse()
    print("\nN = ", N)
    return N

def create_groups(N, table):
    for n in N:
        print(f"Формування груп з {n} експертів:")
        groups = {}
        count = -1
        dict_count = 1
        for arr in combinations(table[0], n):
            count+=1
            temp_arr = []
            temp_C_arr = []
            sum_C = 0
            for j in arr:
                ind = table[0].index(j)
                temp_arr.append( table[1][ind] )
                temp_C_arr.append( table[2][ind] )
                sum_C += table[2][ind]
            if sum_C <= C_lim:
                groups['G'+str(dict_count)] = [arr, temp_arr, temp_C_arr, sum_C]
                print(f" {arr} --> {sum_C}", sep='\n', end='\n')
                dict_count+=1
        if groups:
            print(f"Групи сформовані (всього: {len(groups)})\n")
            return groups
        else:
            print(f"Груп із {n} не сформовано\n")
    return groups

def calculating_arr(groups, comp:list):
    temp_0 = []
    temp_1 = []
    c, dc = -1, 1
    for expn in groups[comp[0]][0]:
        c+=1
        if (expn in groups[comp[1]][0]) == False:
            print(f"{comp[0]}[{expn}] є в {comp[1]} --> False")
            ind = groups[comp[0]][0].index(expn)
            temp_0.append([expn, groups[comp[0]][1][ind]])
    print('|')
    c, dc = -1, 1
    for expn in groups[comp[1]][0]:
        c+=1
        if (expn in groups[comp[0]][0]) == False:
            print(f"{comp[1]}[{expn}] є в {comp[0]} --> False")
            ind = groups[comp[1]][0].index(expn)
            temp_1.append([expn, groups[comp[1]][1][ind]])
    print(f" {comp[0]}: {temp_0}, {comp[1]}: {temp_1}\n")
    arr = [
        [ 1, (temp_0[0][1]/temp_1[0][1])  ],
        [ (temp_1[0][1]/temp_0[0][1]),  1 ],
    ]
    w, v = np.linalg.eig(arr)
    eig_vector = v[:,0].tolist()
    P_max_ind = eig_vector.index( max(eig_vector) )
    print('eig_vector[0] =\n', eig_vector)
    G_win = comp[P_max_ind]
    G_lose = comp[ 1 if P_max_ind==0 else 0 ]
    print('Group_win =', G_win)
    print('Group_lose =', G_lose)
    return G_win, G_lose, eig_vector

def choose_comparison(groups):
    groups_names = []
    for i in groups:
        groups_names.append(i)
    print('group_names = ', groups_names, end='\n')
    comp_start = groups_names[:2]
    def choose_next_comparison(comp, groups_names):
        G_win, G_lose, eig_vector = calculating_arr(groups, comp)
        G_current_ind = groups_names.index(G_win)
        G_lose_ind = groups_names.index(G_lose)
        if G_lose_ind < G_current_ind:
            G_next = groups_names[G_current_ind+1]
        else:
            try:
                G_next = groups_names[G_lose_ind+1]
            except IndexError:
                G_next = groups_names[G_lose_ind]
        print('next comparison is:', [groups_names[G_current_ind], G_next])
        return [groups_names[G_current_ind], G_next]
    comp = comp_start.copy()
    print('--- '*7 + '\n  comparison start =', comp)
    for i in range(len(groups_names)-2):    
        print('--- '*7 + '\n  comparison =', comp)
        comp = choose_next_comparison(comp, groups_names)
    print('--- '*7 + '\n  comparison =', comp)
    winner = choose_next_comparison(comp, groups_names)
    print('\n WINNER:', winner[0])
    return winner[0]

border="=== "

N = create_range_N(max_n, min_n)
print(border*15)
groups = create_groups(N, table)    
print('Groups:', groups)
print(border*15)
winner = choose_comparison(groups)
print(border*15)
print(f'WINNER is {winner}:\n{groups[winner][0]}')