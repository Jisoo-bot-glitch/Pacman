""" """
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print('Use python3 pac-man.py <config.json>', file=sys.stderr)
        return 1
    try:
        print(f'Config file: {sys.argv[1]}')
    except KeyboardInterrupt:
        return 0
    except Exception as err:
        print(f'Error: {err}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
