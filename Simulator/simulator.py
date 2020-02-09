from copy import deepcopy

class Simulator:
    def __init__(self, file_path, input_list, output_list, wire_list, logic_gate, flip_flop):
        self.file_path = file_path
        self.input_list = deepcopy(input_list)
        self.output_list = deepcopy(output_list)
        self.wire_list = deepcopy(wire_list)
        self.logic_gate = deepcopy(logic_gate)
        self.flip_flop = deepcopy(flip_flop)
        self.find_list = ['_AND','_NAND','_OR','_NOR','_XOR','_XNOR','_IV']

    def simulate(self):
        total_number = 2 ** len(self.input_list[0])

        result_list = []
        tmp_input_list = deepcopy(self.input_list)

        for _ in range(total_number):
            if len(self.wire_list) != 0: 
                for i in range(len(self.wire_list[0])):
                    self.wire_list[1][i] = 0

            simulation_result = self._simulate_stable(tmp_input_list, self.output_list, self.wire_list, self.logic_gate, self.flip_flop)
            result_list.append(simulation_result)

            tmp_input_list[1][len(tmp_input_list[0]) - 1] += 1

            temp_count = len(tmp_input_list[0]) - 1
            while temp_count > -1:
                if tmp_input_list[1][temp_count] == 2:
                    tmp_input_list[1][temp_count] = 0
                    tmp_input_list[1][temp_count - 1] += 1
                temp_count -= 1
        return result_list

    def _simulate_stable(self,input_list, output_list, wire_list, logic_gate, flip_flop, upper_limit=20):
        ''' Simulate until stable by comparing results in each cycle of simulation
        '''
        result_output_list = []
        tmp_result_output = deepcopy(output_list)
        tmp_result_wire = deepcopy(wire_list)
        for i in range(upper_limit):
            if i < 2:
                tmp_result_output, tmp_result_wire = self._simulate_cycle(input_list, tmp_result_output, tmp_result_wire, logic_gate, flip_flop, True)
            else:
                tmp_result_output, tmp_result_wire = self._simulate_cycle(input_list, tmp_result_output, tmp_result_wire, logic_gate, flip_flop)
            # print(tmp_result_wire, '#######')
            result_output_list.append(tmp_result_output)
            if len(result_output_list) > 3:
                if result_output_list[-1] == result_output_list[-2] and result_output_list[-2] == result_output_list[-3] and result_output_list[-3] == result_output_list[-4]:
                    # print(tmp_result_wire, ' stable')
                    return result_output_list[-1][1]
        print('Last output combination used, as outputs not stable after {} cycles of simulation for input combination'.format(upper_limit), input_list[1])
        return result_output_list[-1][1]

    # Function definition
    def _simulate_cycle(self,input_list, output_list, wire_list, logic_gate, flip_flop, first_cycle=False):
        ''' Simulates one cycle
        '''
        # name of input: number of inputs
        input_param_names = {'2X':2, '3X':3, '4X':4, 'IVX2':1}

        output_number = len(output_list[0])
        flip_flop_number = len(flip_flop)

        output1_position = 0
        output1_location = 0
        output1_value = -1

        for gate in logic_gate:
            output1_location = 0
            output1_position = 0
            for key in input_param_names:
                # print('gate:',gate[0])
                if key in gate[0]:
                    param_num = input_param_names[key]
                    # print('key',key, param_num)
                    input_values = self._input_match(input_list, gate, param_num)
                    input_values, output1_location, output1_position = self._wire_match(input_values, wire_list, gate, output1_location, output1_position, param_num)
                    
                    input_values = self._output_match(input_values, output_list, gate, param_num)
                    output1_location, output1_position = self._logic_output_match(gate, output1_location, output1_position, output_list)
                    for find in self.find_list:
                        # print(find, gate[0])
                        if find in gate[0]:
                            output1_value = self._logic_output_calc(find, input_values)
            
            if output1_value == -1:
                print(logic_gate)
            assert output1_value != -1
            wire_list, output_list = self._update_node(wire_list, output_list, output1_location, output1_position, output1_value)

            # Flip flop logic.
            if flip_flop_number != 0:
                for g in range(flip_flop_number):
                    if len(wire_list) != 0:
                        wire_number = len(wire_list[0])
                    else:
                        wire_number = 0
                    if not first_cycle:
                        for h in range(wire_number):
                            if flip_flop[g][2] == wire_list[0][h]:
                                for i in range(wire_number):
                                    if flip_flop[g][5] == wire_list[0][i]:
                                        wire_list[1][i] = wire_list[1][h]
                                for j in range(output_number):
                                    if flip_flop[g][5] == output_list[0][j]:
                                        output_list[1][j] = wire_list[1][h]
        return output_list, wire_list

    def _input_match(self,input_list, gate, param_num):
        values_list = [0]*param_num
        for i in range(len(input_list[0])):
            for j in range(param_num):
                if gate[3+j] == input_list[0][i]:
                    values_list[j] = input_list[1][i]
        return values_list

    def _wire_match(self,input_values, wire_list, gate, output1_location, output1_position, param_num):
        values_list = deepcopy(input_values)
        if len(wire_list) != 0:
            for i in range(len(wire_list[0])):
                for j in range(param_num):
                    if gate[3+j] == wire_list[0][i]:
                        values_list[j] = wire_list[1][i]
                if gate[2] == wire_list[0][i]:
                    output1_location = 1
                    output1_position = i
            return values_list, output1_location, output1_position
        return input_values, output1_location, output1_position

    def _output_match(self,input_values, output_list, gate, param_num):
        values_list = deepcopy(input_values)
        for i in range(len(output_list[0])):
            for j in range(param_num):
                if gate[3+j] == output_list[0][i]:
                    values_list[j] = output_list[1][i]
        return values_list

    def _logic_output_match(self,gate, output1_location, output1_position, output_list):
        if output1_location == 0:
            for i in range(len(output_list[0])):
                if gate[2] == output_list[0][i]:
                    output1_location = 2
                    output1_position = i
        return output1_location, output1_position

    def _logic_output_calc(self,gate_type: str, input_values: list):
        if gate_type == '_AND':
            for value in input_values:
                if value == 0:
                    return 0
            return 1
        elif gate_type == '_NAND':
            for value in input_values:
                if value == 0:
                    return 1
            return 0
        elif gate_type == '_OR':
            for value in input_values:
                if value == 1:
                    return 1
            return 0
        elif gate_type == '_NOR':
            for value in input_values:
                if value == 1:
                    return 0
            return 1
        elif gate_type == '_XOR':
            count = [0,0]
            for value in input_values:
                if value == 0:
                    count[0] += 1
                else:
                    count[1] += 1
            if count[0] == 0 or count[1] == 0:
                return 0
            return 1
        elif gate_type == '_XNOR':
            count = [0,0]
            for value in input_values:
                if value == 0:
                    count[0] += 1
                else:
                    count[1] += 1
            if count[0] == 0 or count[1] == 0:
                return 1
            return 0
        elif gate_type == '_IV':
            if len(input_values) > 1:
                raise Exception('Inverter only takes 1 input!')
            for value in input_values:
                if value == 1:
                    return 0
            return 1
        else:
            raise Exception('Logic gate unknown.')

    def _update_node(self,wire_list, output_list, output1_location, output1_position, output1_value):
        ''' Returns updated wire_list, output_list
        '''
        if output1_location == 1:
            tmp_list = deepcopy(wire_list)
            tmp_list[1][output1_position] = output1_value
            return tmp_list, output_list
        else:
            tmp_list = deepcopy(output_list)
            tmp_list[1][output1_position] = output1_value
            return wire_list, tmp_list
