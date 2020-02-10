import Simulator
import os

def test(file_name):
    folder_path = os.path.join(os.getcwd(), 'Tests')
    file_path = os.path.join(folder_path, file_name)
    reader = Simulator.Reader()
    input_list, output_list, wire_list, logic_gate, flip_flop = reader.extract(file_path)
    print(input_list, output_list, wire_list, logic_gate, flip_flop)
    simulator = Simulator.Simulator(file_path, input_list, output_list, wire_list, logic_gate, flip_flop)
    result_list = simulator.simulate()
    return result_list

# # Logic gate tests
# assert test('test_and.v') == [[0], [0], [0], [1]]
# assert test('test_nand.v') == [[1], [1], [1], [0]]
# assert test('test_or.v') == [[0], [1], [1], [1]]
# assert test('test_nor.v') == [[1], [0], [0], [0]]
# assert test('test_xor.v') == [[0], [1], [1], [0]]
# assert test('test_xnor.v') == [[1], [0], [0], [1]]
# assert test('test_iv.v') == [[1], [0]]
# print('All logic gate tests passed!')
# # print(test('test_iv.v'))

# # sample file tests
# assert test('camouflage.v') == [[1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
# print(test('s27_clean.v'))
assert test('s27_clean.v') == [[1], [0], [1], [0], [1], [1], [1], [1], [1], [0], [1], [0], [1], [1], [1], [1]]
assert test('s298_clean.v') == [[1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]]
print('All sample file tests passed!')

