from copy import deepcopy
import Camouflage.output_corrupt

def camouflage(simulator, camo_num):
    # Variable declaration
    #   List
    corrupt_list = Camouflage.output_corrupt.corrupt(simulator)

    initial_logic_gate = deepcopy(simulator.logic_gate)
    camouflage_count_list = []
    first_camouflage_index = 0
    tmp_corrupt_list = deepcopy(corrupt_list)
    print(tmp_corrupt_list)

    while(True):
        first_camouflage = -1
        for i, value in enumerate(tmp_corrupt_list):
            if first_camouflage < value:
                first_camouflage = value
                first_camouflage_index = i
        tmp_corrupt_list[first_camouflage_index] = -1
        print(tmp_corrupt_list)
        camouflage_count_list.append(first_camouflage_index)
        if (camo_num == len(camouflage_count_list)):
            break

    modified_logic_gate = deepcopy(initial_logic_gate)

    while(True):
        print('\n', camo_num, 'gates have been camouflaged.')
        for i in camouflage_count_list:
            modified_logic_gate[i][0] = Camouflage.output_corrupt.gate_change(modified_logic_gate[i][0])
            print('\n', initial_logic_gate[i], '->', modified_logic_gate[i])
        if (camo_num == len(camouflage_count_list)):
            break
