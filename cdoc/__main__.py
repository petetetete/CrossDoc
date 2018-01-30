# Python Standard Library imports
import sys

# Our module imports
from .parsing import process_command


def main():
  process_command(sys.argv)


if __name__ == '__main__':
  main()
