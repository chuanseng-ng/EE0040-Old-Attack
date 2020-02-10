import os
import pandas as pd
import Simulator
import Camouflage
import Attack
import time

start = time.time()

folder_path = os.path.join(os.getcwd(), 'Netlist')

# corrupt_list = Camouflage.corrupt(simulator)
# print('\n', corrupt_list)

# choice = input('\n Choose 1 to camouflage, 2 to attack the logic circuit and 3 to exit.\n :')
choice = 2
while(choice != 3):
    try:
        # choice = int(input('\nSelect an option.\n 1. Camouflage\n 2. Attack\n 3. Exit\n Your choice: '))
        if choice == 1:
            user_input = input('\n State percentage of gates to be camouflaged.\n Default choice is 10% of total logic gates. (%): ')
            start = time.time()
            file_name = 's298_clean.v'
            file_path = os.path.join(folder_path, file_name)
            reader = Simulator.Reader()

            input_list, output_list, wire_list, logic_gate, flip_flop = reader.extract(file_path)
            simulator = Simulator.Simulator(file_path, input_list, output_list, wire_list, logic_gate, flip_flop)

            try:
                camo_num = int(int(user_input) * len(simulator.logic_gate) * 0.01)
                if camo_num <= 0:
                    print('\n No gates selected to be camouflaged. Camouflaging 10% of total logic gates.')
                    camo_num = int(len(simulator.logic_gate)*0.1)
                elif camo_num > 0 and camo_num <= len(simulator.logic_gate):
                    print('\n Camouflaging {}% of total logic gates.'.format(int(user_input)))
                else:
                    print('\n Invalid input. Camouflaging 10% of total logic gates.')
                    camo_num = int(len(simulator.logic_gate)*0.1)
            except ValueError:
                print('\n Invalid input. Camouflaging 10% of total logic gates.')
                camo_num = int(len(simulator.logic_gate)*0.1)

            Camouflage.camouflage(simulator, camo_num)
            choice = 3
        elif choice == 2:
            user_input = 0
            camo_combi = 0

            print("\n Please input the possible logic gate combinations, one at a time. \n")
            print("1 - AND")
            print("2 - NAND")
            print("3 - OR")
            print("4 - NOR")
            print("5 - XOR")
            print("6 - XNOR")
            print("7 - End")

            user_input = input("Selection: ")
            chosen_camo = []
            while user_input != "7":
                camo_combi = camo_combi + 1
                if user_input == "1":
                    chosen_camo.append('HS65_LH_AND2X4')
                    user_input = input("Selection: ")
                elif user_input == "2":
                    chosen_camo.append('HS65_LH_NAND2X2')
                    user_input = input("Selection: ")
                elif user_input == "3":
                    chosen_camo.append('HS65_LH_OR2X4')
                    user_input = input("Selection: ")
                elif user_input == "4":
                    chosen_camo.append('HS65_LH_NOR2X2')
                    user_input = input("Selection: ")
                elif user_input == "5":
                    chosen_camo.append('HS65_LH_XOR2X3')
                    user_input = input("Selection: ")
                elif user_input == "6":
                    chosen_camo.append('HS65_LH_XNOR2X3')
                    user_input = input("Selection: ")
                else:
                    break

            # chosen_camo = ['HS65_LH_AND2X4', 'HS65_LH_NAND2X2', 'HS65_LH_NOR2X2']
            print('\n')

            start = time.time()

            file_name = 's27_clean.v'
            file_path = os.path.join(folder_path, file_name)
            reader = Simulator.Reader()
            input_list, output_list, wire_list, logic_gate, flip_flop = reader.extract(file_path)
            simulator = Simulator.Simulator(file_path, input_list, output_list, wire_list, logic_gate, flip_flop)
            correct_result_list = simulator.simulate()
            # print(correct_result_list, '???')

            file_name = 's27_edited.v'
            file_path = os.path.join(folder_path, file_name)
            reader = Simulator.Reader()
            input_list, output_list, wire_list, logic_gate, flip_flop = reader.extract(file_path)
            simulator = Simulator.Simulator(file_path, input_list, output_list, wire_list, logic_gate, flip_flop)
            attack_output, camo_gate_names = Attack.attack(chosen_camo, simulator, correct_result_list)

            print('\n')
            attack_output_keys = list(attack_output.keys())
            # print(camo_gate_names)
            columns = camo_gate_names + ['Result']
            # print(columns)
            table_columns = []
            for i in range(len(attack_output_keys)):
                tmp_column = []
                for j in range(len(attack_output_keys[0])):
                    tmp_column.append(attack_output_keys[i][j])
                tmp_column.append(attack_output[attack_output_keys[i]][0])
                table_columns.append(tmp_column)
            df = pd.DataFrame(table_columns, columns=columns)
            print(df.to_string())
            choice = 3
        elif choice == 3:
            break

    except ValueError:
        print('Invalid menu choice')
        choice = 0

end = time.time()
runtime = end-start

print('\n Runtime:', runtime, 'sec')
if runtime > 60:
    runtime = runtime/60
    print('\n Runtime:', runtime, 'min')
    if runtime > 60:
        runtime = runtime/60
        print('\n Runtime:', runtime, 'hr')