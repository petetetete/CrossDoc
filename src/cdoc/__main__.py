# Python Standard Library imports
import sys

# Our module imports
from .parsing import processCommand


def main():
  processCommand(sys.argv)


if __name__ == '__main__':
  main()
