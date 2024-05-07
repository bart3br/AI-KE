from enum import Enum
from game import Game
from heuristics import Heuristics

class NodeState(Enum):
    ROOT = 'root'
    NODE = 'node'
    LEAF = 'leaf'

class Node:
    def __init__(self, game: Game, parent: 'Node' = None, children: dict = {}, value: float = -1.0) -> None:
        self.game = game
        self.parent = parent
        self.children = children
        self.value = value
        self.node_state = self.__define_node_state()
    
    def __define_node_state(self) -> str:
        if not self.children:
            return NodeState.LEAF
        if self.parent is None:
            return NodeState.ROOT
        return NodeState.NODE
    
    def add_child(self, child: 'Node', move: tuple) -> None:
        self.children[move] = child
        child.parent = self
        self.node_state = self.__define_node_state()
    
    def evaluate_game(self, player_num: int, evaluate_func) -> None:
        if (self.node_state == NodeState.LEAF):
            self.value = evaluate_func(self.game, player_num)
        # match (self.node_state, maximize):
        #     case (NodeState.LEAF, _):
        #         self.value = Heuristics.evaluate_func(self.game, player_num)
        #     case (_, True):
        #         # max_value = -float('inf')
        #         # for child in self.children.values():
        #         #     child.evaluate_game(player_num, not maximize, evaluate_func)
        #         #     max_value = max(max_value, child.value)
        #         # self.value = max_value
        #         self.value = max(child.value for child in self.children.values())
        #     case (_, False):
        #         # min_value = float('inf')
        #         # for child in self.children.values():
        #         #     child.evaluate_game(player_num, not maximize, evaluate_func)
        #         #     min_value = min(min_value, child.value)
        #         # self.value = min_value
        #         self.value = min(child.value for child in self.children.values())
    
    