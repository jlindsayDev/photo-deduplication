from argparse import ArgumentParser

import manager

def parse_args():
  parser = ArgumentParser(description='Launch Photo Manager')
  return parser.parse_args()

def main():
  args = parse_args()
  manager.launch(args)

if __name__ == "__main__":
  main()
