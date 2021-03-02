import numpy as np
from collections import defaultdict
import heapq

def get_inv_count(arr):

    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[j] and arr[i] and arr[i] > arr[j]:
                inv_count += 1

    return inv_count

def find_0(matrix):
    pos = np.where(matrix == 0)
    i = pos[0][0]
    j = pos[1][0]
    return i, j

def is_solvable(matrix):
    inv_count = get_inv_count(matrix.flatten())
    row, _ = find_0(matrix)
    if matrix.shape[0] % 2:
        return not inv_count % 2
    else:
        if not row % 2 and inv_count % 2:
            return True
        else:
            return bool(row % 2 and not inv_count % 2)

def get_end_board(n):
    return np.array(list(range(1, n**2)) + [0]).reshape((n, n))


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, board=None):
        self.parent = parent
        self.board = board

        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, obj):
        return self.f < obj.f

    def __eq__(self, other):
        if not other:
            return False
        else:
            return (self.board == other.board).all()

    def get_children(self):
        children = []
        i, j = find_0(self.board)
        n = len(self.board)
        if i < n-1:
            new_board = self.board.copy()
            new_board[i][j] = new_board[i+1][j]
            new_board[i+1][j] = 0
            children.append(Node(self, new_board))
        if i > 0:
            new_board = self.board.copy()
            new_board[i][j] = new_board[i-1][j]
            new_board[i-1][j] = 0
            children.append(Node(self, new_board))
        if j < n-1:
            new_board = self.board.copy()
            new_board[i][j] = new_board[i][j+1]
            new_board[i][j+1] = 0
            children.append(Node(self, new_board))
        if j > 0:
            new_board = self.board.copy()
            new_board[i][j] = new_board[i][j-1]
            new_board[i][j-1] = 0
            children.append(Node(self, new_board))

        return children

best_fscores = defaultdict(lambda: np.inf)

class PriorityQueue(object):

    def __init__(self, object_list):
        self.queue_length = 0
        self.qheap = []
        for e in object_list:
            self.qheap.append((e.f, e))
            self.queue_length += 1
        heapq.heapify(self.qheap)

    def push(self, new_object):
        heapq.heappush(self.qheap,(new_object.f, new_object))
        self.queue_length += 1

    def pop(self):
        if self.queue_length < 1:
            return None
        f, node = heapq.heappop(self.qheap)
        self.queue_length -= 1
        global best_fscores
        best_f = best_fscores[str(node.board)]
        if best_f >= f:
            return node
        else:
            return self.pop()


def astar(start, end):

    n = start.shape[0]
    global best_fscores
    start_node = Node(None, start)
    end_node = Node(None, end)
    start_node.g = 0
    start_node.h = np.sum(start_node.board - end_node.board)**2

    open_set = PriorityQueue([start_node])

    while open_set.queue_length > 0:

        current_node = open_set.pop()
        if current_node == None:
            break

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.board)
                current = current.parent
            return path[::-1]

        for child in current_node.get_children():

            child.g = current_node.g + 1
            child.h = np.sum(child.board != end_node.board) - 1
            child.f = child.g + child.h


            if best_fscores[str(child.board)] > child.f:
                best_fscores[str(child.board)] = child.f
                open_set.push(child)



if __name__ == "__main__":
    n = int(input("Введите размер пазла: "))
    print("Введите пазл:")
    matrix = np.array([list(map(int, input().split())) for _ in range(n)])
    assert np.sum(matrix) == np.sum(range(n**2)), "Неверные входные данные"

    if is_solvable(matrix):
        print("Решение:")
        solution = astar(matrix, get_end_board(n))
        if solution:
            for board in solution:
                print(board)
        else:
            print("Не удалось найти решение")
    else:
        print("Нет решения")
