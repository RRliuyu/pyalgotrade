from MyStrategy1 import run_strategy
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
config = Config(max_depth=100)
graphviz = GraphvizOutput(output_file=r'trace_detail.png')
with PyCallGraph(output=graphviz,config=config):
    run_strategy(3,8)