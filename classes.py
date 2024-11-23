import os

class MyClassForArguments:
    def __init__(self, argumentValue, other=''):
        self.value = argumentValue
        self.other = other


    def check_input_file_existing(self):
        if os.path.exists(self.value):
            return self.value

    def check_output_file_existing(self):
        if not self.value is None:
            if os.path.exists(self.value):
                print(f"File to output is exist! Result will be written in the {self.value} file!")
                return self.value
            else:
                print(f"Your file to output is not exist! {self.value} will be created to output!")

    def check_medals(self):
        if not self.value is None:
            if len(self.value) < 2:
                print(f"To use command 'medals' you have to enter the country and the year!")
                pass
            else:
                try:
                    year = int( self.value[-1] )
                    team = " ".join( self.value[:-1] )
                    print(f"Year {year} , team: {team}")
                    return year, team
                except Exception:
                    print(f"To use command 'medals' the entered year must be a valid number!")


    def check_total(self):
        if not self.value is None:
            try:
                return int(self.value)
            except ValueError:
                print(f"To use command 'total' the entered year must be a valid number!")

    def check_overall(self):
        if not self.value is None:
            return self.value