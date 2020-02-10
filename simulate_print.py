import time
import Simulator
import os

#   Variables
# file = input('State the netlist file name, with the file type: ')
# file_name = 'camouflage.v'
# file_name = 's27_clean.v'
# file_name = 's298_clean.v'
file_name = input('Provide file name of original netlist: ')
start = time.time()
folder_path = os.path.join(os.getcwd(), 'Netlist')
file_path = os.path.join(folder_path, file_name)
reader = Simulator.Reader()
input_list, output_list, wire_list, logic_gate, flip_flop = reader.extract(file_path)
simulator = Simulator.Simulator(file_path, input_list, output_list, wire_list, logic_gate, flip_flop)
result_list = simulator.simulate()

for w in range(len(result_list)):
    print('\n', result_list[w])

end = time.time()
runtime = end - start

print("Runtime: ", runtime, "s")
