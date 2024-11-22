import os

class MyClassForArguments:
    def __init__(self, argumentValue, other=''):
        self.value = argumentValue
        self.other = other

    def check_input_file_existing(self):
        if os.path.exists(self.value):
            return self.value
        else: return False

    def check_output_file_existing(self):
        if self.value == None:
            return False
        if os.path.exists(self.value):
            print(f"File to output is exist! Result will be written in the {self.value} file!")
            # return self.value
        else:
            print(f"Your file to output is not exist! {self.value} will be created to output!")