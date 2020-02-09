class Reader:
    def __init__(self):
        self.find_gate = '.A'
        self.find_flip = '.D'
        self.find_input = 'input'
        self.find_output = 'output'
        self.find_wire = 'wire'

        self.input_number = 0
        self.output_number = 0
        self.wire_number = 0

    def extract(self, file_name):
        # Variables declaration
        #   Lists
        # Read file and store them into list of strings
        input_list, output_list, gate_list, flip_list, wire_list = self._extract_lists(file_name)
        input_list = self._process_lists('input', input_list)
        output_list = self._process_lists('output', output_list)
        wire_list = self._process_lists('wire', wire_list)
        logic_gate = self._process_logic_lists('logic_gate', gate_list)
        flip_flop = self._process_logic_lists('flip_flop', flip_list)
        # print(input_list, output_list, wire_list, logic_gate, flip_flop)

        return input_list, output_list, wire_list, logic_gate, flip_flop

    def _extract_lists(self, file_name):
        with open(file_name) as f:
            line_list = [line.rstrip('\n') for line in f]
        # Finding keywords from list of string
        #   List[1] is to store values
        input_list = []
        output_list = []
        gate_list = []
        flip_list = []
        wire_list = []
        for line in line_list:
            if self.find_input in line:
                input_list.append(line.strip())
                input_list.append(line.strip())
            if self.find_output in line:
                output_list.append(line.strip())
                output_list.append(line.strip())
            if self.find_gate in line:
                gate_list.append(line.strip())
            if self.find_flip in line:
                flip_list.append(line.strip())
            if self.find_wire in line:
                wire_list.append(line.strip())
                wire_list.append(line.strip())

        return input_list, output_list, gate_list, flip_list, wire_list

    def _process_lists(self, list_type, lists):
        replace_input_list = ['input ', 'CLK', 'NRST', ';']
        replace_output_list = ['output ', ';']
        replace_wire_list = ['wire ', ';']

        replace_list = []
        if list_type == 'input':
            replace_list = replace_input_list
        elif list_type == 'output':
            replace_list = replace_output_list
        elif list_type == 'wire':
            replace_list = replace_wire_list
        else:
            raise Exception('Invalid list type.')

        tmp_number = 0
        for i, line in enumerate(lists):
            line = line.split(',')
            for j in range(len(line)):
                for item in replace_list:
                    line[j] = line[j].replace(item, '')
            lists[i] = list(filter(None, line))
            tmp_number = len(lists[i])
        # Reset input values to 0
        for i in range(tmp_number):
            lists[1][i] = 0

        return lists

    def _process_logic_lists(self, list_type, lists):
        replace_logic_gate = ['(', ')', ',','.A','.B','.C','.D','.Z',';']
        replace_flip_flop_list = ['(', ')', ',','.D','.Q','.CP','.RN',';']

        replace_list = []
        if list_type == 'logic_gate':
            replace_list = replace_logic_gate
        elif list_type == 'flip_flop':
            replace_list = replace_flip_flop_list
        else:
            raise Exception('Invalid list type.')

        for i, line in enumerate(lists):
            line = line.split()
            for j in range(len(line)):
                for item in replace_list:
                    line[j] = line[j].replace(item, '')
            lists[i] = list(filter(None, line))

        return lists