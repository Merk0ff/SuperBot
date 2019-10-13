import json
import logging
import sys
import core.controllers.controller_user as controller_user
import core.controllers.controller_moder as controller_moder

sys.path.append('../')

# Set up logger
logging.basicConfig(filename="text.log", level=logging.INFO)


def main():
    with open('config.json') as json_file:
        config = json.load(json_file)

    if sys.argv[1] == 'user':
        controller_user.set_up(config['user'])
        controller_user.run()
    elif sys.argv[1] == 'moder':
        controller_moder.set_up(config['moder'])
        controller_moder.run()

    logging.error("Wrong args")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Choose version user/moder")
        logging.error("Wrong args")
    else:
        main()
