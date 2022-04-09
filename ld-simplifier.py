import math
from re import L
from tkinter import ACTIVE

from numpy import ones_like


IN_NUM = 0
OUT_NUM = 0
OUTPUTS = []
OUT_COLS = []
ACTIVE_INS = []


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
                    #Do shit
                    if (bit == len(ACTIVE_INS[group][value]) - 1):
                        print("In" + str(bit + 1) + "^   +   ", end = "")
                    else:
                        print("In" + str(bit + 1) + "^ ", end = "")

                else:
                    #Do the other shit
                    if (bit == len(ACTIVE_INS[group][value]) - 1):
                        print("In" + str(bit + 1) + "   +   ", end = "")
                    else:
                        print("In" + str(bit + 1) + " ", end = "")
        print(" = Out" + str(group + 1))
        #print(ACTIVE_INS)
        #CALL SIMPLIFICATION FUNCTION HERE 
        quineMcCluskey(group)



def quineMcCluskey(group):
    groups = []
    #tracking = []
    #INITIALIZE ALL POSSIBLE GROUPS
    for num in range(IN_NUM + 1):
        set = []
        groups.append(set)

    #LOCATE ONES IN MINTERMS AND ORGANIZE INTO GROUPS
    for value in range(len(ACTIVE_INS[group])):
        one_count = 0
        for bit in range(len(ACTIVE_INS[group][value])):
            if ACTIVE_INS[group][value][bit] == '1':
                one_count = one_count + 1
        groups[one_count].append([str(int(ACTIVE_INS[group][value], 2)), ACTIVE_INS[group][value]])
    print(groups)

    #BEGIN FINDING MATCHED PAIRS
    diff_count = 0
    matched_pairs = []
    for each_group in range(len(groups)):
        if (each_group == len(groups) - 1): #IF LAST GROUP, BREAK
            break
        else:
            for val in range(len(groups[each_group])):
                for next_val in range(len(groups[each_group + 1])):
                    diff_count = 0
                    for bit in range(len(groups[each_group][val][1])):
                        if groups[each_group][val][1][bit] != groups[each_group + 1][next_val][1][bit]:
                            diff_count = diff_count + 1
                            stored_diff_bit = bit
                    if diff_count == 1:
                        #ORGANIZE MATCHED PAIRS BY ONES GROUPS AGAIN / STANDARDIZE DASHING TO MAKE pairMatching FUNCTION
                        replacement = groups[each_group][val][1][:stored_diff_bit]+'-'+groups[each_group][val][1][stored_diff_bit+1:]
                        matched_pairs.append([str(int(groups[each_group][val][1], 2)) + '-' + str(int(groups[each_group + 1][next_val][1], 2)), replacement])

    print(matched_pairs)
    #print(tracking)


#def pairMatching(groups):
#    










if __name__ == "__main__":
    main()