from glob import glob
import math
from re import L
from tkinter import ACTIVE
from tokenize import group

from numpy import subtract


IN_NUM = 0
OUT_NUM = 0
OUTPUTS = []
OUT_COLS = []
ACTIVE_INS = []
PRIME_IMPLICANTS = []
ESSENTIAL_PRIME_IMPLICANTS = []


def main():
    global IN_NUM
    global OUT_NUM
    global OUTPUTS
    print("Welcome to the Logic Design Simplifier!\n")
    print("Please enter the number of inputs: ")
    ins = input()
    while int(ins) >= 10:
        print("Logic with 10 inputs or greater is currently unsupported.")
        print("Please enter the number of inputs: ")
        ins = input()
    IN_NUM = int(ins)
    print("Please enter the number of outputs: ")
    outs = input()
    OUT_NUM = int(outs)
    combo = pow(2, IN_NUM)
    OUT_COLS = [0] * combo
    OUTPUTS = [OUT_COLS.copy() for i in range(OUT_NUM)]
    truthTable()
    for set in range(combo):
        print("Please enter the desired output(s) for input set " + str(set + 1) + ": ")
        for out in range(OUT_NUM):
            print("Out" + str(out + 1) + ": ", end = "")
            temp = input()
            if (int(temp) < 0 or int(temp) > 1):
                print("Invlid input. Outputs must be single bit binary values. Please Re-enter:")
                print("Out" + str(out + 1) + ": ", end = "")
                temp = input()
            OUTPUTS[out][set] = int(temp)
        truthTable()
    logicEquation()
    #print(ACTIVE_INS)
    




def truthTable():
    #TRUTH TABLE HEADER
    for inp in range(IN_NUM):
        print("|  In" + str(inp + 1) + "  |", end = "")
    
    for out in range(OUT_NUM):
        if out == OUT_NUM - 1:
            print("|  Out" + str(out + 1) + "  |")
        else:
            print("|  Out" + str(out + 1) + "  |", end = "")

    combos = pow(2, IN_NUM)
    bit = 0

    #TRUTH TABLE BODY
    for row in range(combos):
        binary = str(format(row, f"0{IN_NUM}b"))
        for inp in range(IN_NUM):
            print("|   " + str(binary[bit]) + "   |", end = "")
            bit = bit + 1
        bit = 0
        outCol = 0
        for out in range(OUT_NUM):
            if out == OUT_NUM - 1:
                print("|   " + str(OUTPUTS[outCol][row]) + "   |")
                outCol = 0 #RESET ON NEXT ROW
            else:
                print("|   " + str(OUTPUTS[outCol][row]) + "   |", end = "")
                outCol = outCol + 1 #MOVE TO THE OTHER ARRAY (OTHER OUTPUT)





def logicEquation():
    #RETRIEVE THE INPUT SET FOR EVERY HIGH OUTPUT
    global ACTIVE_INS
    ACTIVE_INS = [[] for i in range(len(OUTPUTS))]
    for set in range(len(OUTPUTS)):
        for output in range(len(OUTPUTS[set])):
            if OUTPUTS[set][output] == 1:
                val = str(format(output, f"0{IN_NUM}b"))
                #print("Binary: " + str(val))
                ACTIVE_INS[set].append(str(val))
                #append here
            #move to next array here
        print("\n")
    for group in range(len(ACTIVE_INS)):
        for value in range(len(ACTIVE_INS[group])):
            for bit in range(len(ACTIVE_INS[group][value])):
                if ACTIVE_INS[group][value][bit] == '0':
                    if (bit == len(ACTIVE_INS[group][value]) - 1):
                        print("In" + str(bit + 1) + "^   +   ", end = "")
                    else:
                        print("In" + str(bit + 1) + "^ ", end = "")

                else:
                    if (bit == len(ACTIVE_INS[group][value]) - 1):
                        print("In" + str(bit + 1) + "   +   ", end = "")
                    else:
                        print("In" + str(bit + 1) + " ", end = "")
        print(" = Out" + str(group + 1))
        #print(ACTIVE_INS)
        #CALL SIMPLIFICATION FUNCTION HERE 
        quineMcCluskey(group)
        global PRIME_IMPLICANTS
        PRIME_IMPLICANTS.clear()





def quineMcCluskey(group):
    #GROUP ACTIVE INPUTS BY # OF ONES
    groups = firstGrouping(ACTIVE_INS[group])
    new_groups, break_cond = pairMatching(groups)

    while (break_cond != 1):
        new_groups, break_cond = pairMatching(new_groups)
        if break_cond == 1:
            break

    #REMOVE SUBSTRINGS (CONTIGUOUS AND NON-CONTIGUOUS) FOUND WITHIN PRIME IMPLICANTS (IDK IF THIS MESSES WITH ANYTHING YET, TEST WITHOUT DOING THIS FOR NOW)
    print("Prime Implicants: {}".format(PRIME_IMPLICANTS))
    primeImplication(group) 





def firstGrouping(chosen_set):
    #INITIALIZE ALL POSSIBLE GROUPS
    groups = []
    for num in range(IN_NUM + 1):
        set = []
        groups.append(set)

    #LOCATE ONES IN MINTERMS AND ORGANIZE INTO GROUPS
    for value in range(len(chosen_set)):
        one_count = 0
        for bit in range(len(chosen_set[value])):
            if chosen_set[value][bit] == '1':
                one_count = one_count + 1
        groups[one_count].append([str(int(chosen_set[value], 2)), chosen_set[value]])
    print("First Grouping: {}".format(groups))
    return groups   




def otherGrouping(pairs_list):
    #INITIALIZE ALL POSSIBLE GROUPS
    new_groups = []
    for num in range(IN_NUM + 1):
        set = []
        new_groups.append(set)
    
    #LOCATE ONES IN MINTERMS AND ORGANIZE INTO GROUPS
    for pair in pairs_list:
        one_count = 0
        for bit in range(len(pair[1])):
            if pair[1][bit] == '1':
                one_count = one_count + 1
        new_groups[one_count].append(pair)
    print("New Groups: {}".format(new_groups))
    return new_groups



def pairMatching(groups):
    diff_count = 0
    matched_pairs = []
    none_used = 1
    is_present = 0
    for each_group in range(len(groups)):
        if (each_group == len(groups) - 1): #IF LAST GROUP, BREAK
            break
        else:
            for val in range(len(groups[each_group])):
                used = 0
                for next_val in range(len(groups[each_group + 1])):
                    diff_count = 0
                    for bit in range(len(groups[each_group][val][1])):
                        if groups[each_group][val][1][bit] != groups[each_group + 1][next_val][1][bit]:
                            diff_count = diff_count + 1
                            stored_diff_bit = bit
                    if diff_count == 1:
                        used = 1
                        none_used = 0
                        replacement = groups[each_group][val][1][:stored_diff_bit]+'-'+groups[each_group][val][1][stored_diff_bit+1:]
                        matched_pairs.append([groups[each_group][val][0] + '-' + groups[each_group + 1][next_val][0], replacement])
                if used == 0:
                    #ADD CHECK IF IMPLICANT IS ALREADY PRESENT, IF SO DONT ADD
                    is_present = 0
                    global PRIME_IMPLICANTS
                    for element in range(len(PRIME_IMPLICANTS)):
                        #print("why {} {}".format(groups[each_group][val][0], PRIME_IMPLICANTS[element][0]))
                        if is_permutation(groups[each_group][val][0], PRIME_IMPLICANTS[element][0]): #DO NOT ADD EQUIVALANT PERMUTATIONS
                            is_present = 1
                    if is_present == 0:
                        PRIME_IMPLICANTS.append(groups[each_group][val])

    print("Matched Pairs: {}".format(matched_pairs))
    new_groups = otherGrouping(matched_pairs)
    return new_groups, none_used




def is_permutation(first_string, other_string):
    if len(first_string) != len(other_string):
        return False

    count_first = {}
    count_other = {}

    for char in first_string:
        if char in count_first.keys():
            count_first[char] += 1
        else:
            count_first[char] = 1

    for char in other_string:
        if char in count_other.keys():
            count_other[char] += 1
        else:
            count_other[char] = 1

    for char in count_first.keys():
        if char not in count_other.keys():
            return False
        elif count_first[char] != count_other[char]:
            return False

    return True



def transpose(A):
    result = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    return result



def primeImplication(group):
    minterms = []
    for i in range(len(ACTIVE_INS[group])):
        minterms.append(int(ACTIVE_INS[group][i], 2))
    i = 0

    table = [['-'] * len(minterms) for i in range(len(PRIME_IMPLICANTS))]

    #PRINT STARTING TABLE
    print(minterms)
    for k in range(len(table)):
        for l in range(len(table[k])):
            if l == len(table[k]) - 1:
                print(table[k][l])
            else:
                print(table[k][l] + ', ', end='')
    print("\n")

    char = 0
    for tuple in range(len(PRIME_IMPLICANTS)):
        for char in range(len(PRIME_IMPLICANTS[tuple][0])):
            for val in range(len(minterms)):
                #print("Implicant Char: {}, Minterm Val: {}, ".format(PRIME_IMPLICANTS[tuple][0][char], str(minterms[val])))
                if PRIME_IMPLICANTS[tuple][0][char] == str(minterms[val]):
                    #print("please dont print 20 times uwu. tuple: {}, val: {}".format(tuple, val))
                    table[tuple][val] = 'x' #<--
                    #print(table)

    #COMPLETION PRINT
    print(minterms)
    for m in range(len(table)):
        for n in range(len(table[m])):
            if n == len(table[m]) - 1:
                print(table[m][n])
            else:
                print(table[m][n] + ', ', end='')
    print("\n")

    #FIND COLUMNS WITH ONLY ONE X, THEN FIND WHICH ROW X IS IN (THIS WILL GIVE INDEX OF USEFUL PRIME IMPLICANTS)
    table_transpose = transpose(table)
    print(table_transpose)
    for it in range(len(table_transpose)):
        x_count = 0
        for it2 in range(len(table_transpose[it])):
            if table_transpose[it][it2] == 'x':
                x_count = x_count + 1
                x_store = it2
        if x_count == 1:
            global ESSENTIAL_PRIME_IMPLICANTS
            ESSENTIAL_PRIME_IMPLICANTS.append(PRIME_IMPLICANTS[x_store])
    
    print(ESSENTIAL_PRIME_IMPLICANTS)
    simplifiedEquation(group)




def simplifiedEquation(group):
    global ESSENTIAL_PRIME_IMPLICANTS
    for iter in range(len(ESSENTIAL_PRIME_IMPLICANTS)):
        for bit in range(len(ESSENTIAL_PRIME_IMPLICANTS[iter][1])):
            if ESSENTIAL_PRIME_IMPLICANTS[iter][1][bit] == '1':
                print("In" + str(bit + 1), end='')
                if bit == len(ESSENTIAL_PRIME_IMPLICANTS[iter][1]) - 1:
                    print(" + ", end='')
            elif ESSENTIAL_PRIME_IMPLICANTS[iter][1][bit] == '0':
                print("In" + str(bit + 1) + "^", end='')
                if bit == len(ESSENTIAL_PRIME_IMPLICANTS[iter][1]) - 1:
                    print(" + ", end='')
    ESSENTIAL_PRIME_IMPLICANTS.clear()
    print(" = Out" + str(group + 1))
    












if __name__ == "__main__":
    main()