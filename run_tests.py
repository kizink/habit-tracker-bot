import os
from sys import exit
from pytest import main

if os.path.isdir('tests'):
    exit(main(['-vv', 'tests/']))
else:
    print("Tests directory not found, skipping tests.")

# exit(main(['-vv', 'tests/']))
