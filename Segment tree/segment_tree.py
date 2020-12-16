
ans = []

# Ужасное объявление переменных, делалось для себя
class Tree():
    def __init__(self):
        self.ary = []
        self.tree = []

    def build_tree(self, v, tl, tr):
        if tl == tr:
            self.tree[v] = self.ary[tl]
            return self.tree[v]
        mid = (tl+tr) // 2
        self.tree[v] = self.build_tree(v*2, tl, mid) + self.build_tree(v*2+1, mid+1, tr)
        return self.tree[v]

    def ret_sum(self, v, tl, tr, ls, rs):
        if ls > rs:
            return 0
        if ls == tl and rs == tr:
            return self.tree[v]
        mid = (tl+tr) // 2
        return (self.ret_sum(v*2, tl, mid, ls, min(rs, mid)) + self.ret_sum(v*2+1, mid+1, tr, max(ls, mid+1), rs))

    def update_tree(self, v, tl, tr, i, x):
        if tl == tr:
            self.tree[v] = x
        else:
            mid = (tl+tr) // 2
            if i <= mid:
                self.update_tree(v*2, tl, mid, i, x)
            else:
                self.update_tree(v*2+1, mid+1, tr, i, x)
            self.tree[v] = self.tree[v*2]+self.tree[v*2+1]

sumtree = Tree()

with open("segment_tree_input.txt") as file:
    N, K = file.readline().strip().split()
    sumtree.ary = [0 for i in range(int(N))]
    sumtree.tree = [0 for i in range(int(N)*4)] #4N т.к. возможно N  не степень двойки
    for i in range(int(K)):
        query, x, y = file.readline().strip().split()
        x = int(x)
        y = int(y)
        if query == "A":

            sumtree.update_tree(1, 0, int(N) - 1, x-1, y)
        else:
            print(sumtree.ret_sum(1, 0, int(N) - 1, x-1, y-1))

with open("segment_tree_output.txt", "w") as file:
    for i in range(len(ans)):
        file.write(str(ans[i])+"\n")