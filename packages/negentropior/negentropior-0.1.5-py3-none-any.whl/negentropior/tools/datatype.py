import argparse


def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--start-time', required=False, type=str, dest='start_time')
    parser.add_argument('--end-time', required=False, type=str, dest='end_time')

    return parser


parser = get_parser()
args = vars(parser.parse_args())


def run():
    print(args['start_time'], args['end_time'])


if __name__ == '__main__':
    run()


