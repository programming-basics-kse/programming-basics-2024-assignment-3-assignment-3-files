from args_handlers.total_handler import handle_total_arg
from argument_config import *
from file_reader import read_file
from args_handlers.medals_handler import *

def main():
    config = receive_application_args()
    data = read_file(config['filename'], "r")

    if config["medals"]:
        handle_medals_arg(data, config['medals'])
    elif config["total"]:
        handle_total_arg(data, config['total'])
    elif config["overall"]:
        pass
    elif config["interactive"]:
        pass

main()