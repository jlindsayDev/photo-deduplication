# https://docs.python.org/3/library/__main__.html#main-py-in-python-packages
# python3 -m dedupe
import sys
from main import safe_main
sys.exit(safe_main())
