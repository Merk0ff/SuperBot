import json
import src.core.controller as controller


def main():
    with open('config.json') as json_file:
        config = json.load(json_file)

    controller.set_up(config)


if __name__ == '__main__':
    main()