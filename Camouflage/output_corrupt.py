from copy import deepcopy

def corrupt(simulator):
    # Variables declaration
    #   Lists
    corrupt_list = []
    simulation_result = simulator.simulate()
    # print(simulation_result)
    original_result = deepcopy(simulation_result)
    original_logic = deepcopy(simulator.logic_gate)
    modified_logic = deepcopy(original_logic)
    count = 0

    for i in range(len(original_logic)):
        # Reset input values to 0
        for j in range(len(simulator.input_list[0])):
            simulator.input_list[1][j] = 0

        if "_IV" not in modified_logic[i][0]:
            modified_logic[i][0] = gate_change(modified_logic[i][0])

            # Change logic
            # a = deepcopy(simulator.logic_gate)
            simulator.logic_gate = modified_logic
            # assert a == simulator.logic_gate

            print('Camouflaged gate name: ', original_logic[count][1])
            count += 1

            simulation_result = simulator.simulate()
            modified_result = simulation_result
            # print(modified_result)

            # Revert logic
            modified_logic[i][0] = gate_change(modified_logic[i][0])
            simulator.logic_gate = modified_logic

            corrupt_list.append(_output_corrupt(original_result, modified_result))

        # print('\n')
        '''for w in range(len(modified_result)):
            print('\n', modified_result[w])'''
    return corrupt_list

def gate_change(logic_gate):
    # NAND <-> OR
    # NOR <-> AND
    # XOR <-> XNOR

    find_and = '_AND'
    find_nand = '_NAND'
    find_or = '_OR'
    find_nor = '_NOR'
    find_xor = '_XOR'
    find_xnor = '_XNOR'

    if find_and in logic_gate:
        logic_gate = 'HS65_LH_NOR2X2'
    elif find_nand in logic_gate:
        logic_gate = 'HS65_LH_OR2X4'
    elif find_or in logic_gate:
        logic_gate = 'HS65_LH_NAND2X2'
    elif find_nor in logic_gate:
        logic_gate = 'HS65_LH_AND2X4'
    elif find_xor in logic_gate:
        logic_gate = 'HS65_LHS_XNOR2X3'
    elif find_xnor in logic_gate:
        logic_gate = 'HS65_LHS_XOR2X3'
    # else:
    #     print('No change')

    return logic_gate


def _output_corrupt(original_result, modified_result):
    corrupt_count = 0

    for i in range(len(original_result)):
        for j in range(len(original_result[i])):
            if original_result[i][j] != modified_result[i][j]:
                corrupt_count += 1
            else:
                pass

    return corrupt_count