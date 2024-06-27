import argparse
import time
import threading
#from tot.methods.bfs import solve
#from tot.tasks.game24 import Game24Task
import sys
import os

# Add the directory containing the module to the system path
module_path = os.path.join("C:", "Users", "sheld", "Documents", "GitHub", "tree-of-thought-llm", "src")
if module_path not in sys.path:
    sys.path.append(module_path)

from src.tot.methods.bfs import solve,naive_solve, bfs_checker
from src.tot.tasks.game24 import Game24Task, checker

checker()
bfs_checker()
args = argparse.Namespace(backend='llama3', temperature=0.7, task='game24', naive_run=False, prompt_sample=None, method_generate='propose', method_evaluate='value', method_select='greedy', n_generate_sample=1, n_evaluate_sample=1, n_select_sample=1)

task = Game24Task()


ys, infos = solve(args, task, 900)
print('completed search')
print(ys)

#ys, infos = solve(args, task, 902)
#print('completed search')
#print(ys)
