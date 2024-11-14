import actions

def setup_arg_parser():
    pass

def action_and_options_from_args(args):
    pass

def main():
    arg_parser = setup_arg_parser
    args = arg_parser.pars_args()

    action, options = action_and_options_from_args(args)
    action = getattr(actions, action)

    output = action(options) 
    print(output)

    #TODO: check if the -output arg is specified and save the output to a filie

if __name__ == '__main__':
    main()
