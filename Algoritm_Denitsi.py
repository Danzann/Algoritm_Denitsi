from collections import deque, defaultdict

class DinicAlgorithm:
    def __init__(self, vertices):
        self.V = vertices  # Количество вершин
        self.graph = defaultdict(list)  # Граф в виде списка смежности
        self.capacity = {}  # Пропускная способность рёбер

    # Добавление ребра в граф
    def add_edge(self, u, v, capacity):
        self.graph[u].append(v)
        self.graph[v].append(u)  # Обратное ребро для остаточной сети
        self.capacity[(u, v)] = capacity
        self.capacity[(v, u)] = 0  # Обратное ребро изначально имеет нулевую пропускную способность

    # Построение уровневого графа с помощью BFS
    def bfs(self, source, sink):
        self.level = [-1] * self.V
        self.level[source] = 0
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if self.level[v] == -1 and self.capacity[(u, v)] > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[sink] != -1

    # Нахождение увеличивающего пути с помощью DFS
    def dfs(self, u, flow, sink, ptr):
        if u == sink:
            return flow
        while ptr[u] < len(self.graph[u]):
            v = self.graph[u][ptr[u]]
            if self.level[v] == self.level[u] + 1 and self.capacity[(u, v)] > 0:
                min_flow = min(flow, self.capacity[(u, v)])
                result = self.dfs(v, min_flow, sink, ptr)
                if result > 0:
                    self.capacity[(u, v)] -= result
                    self.capacity[(v, u)] += result
                    return result
            ptr[u] += 1
        return 0

    # Основной алгоритм
    def max_flow(self, source, sink):
        total_flow = 0

        while self.bfs(source, sink):
            ptr = [0] * self.V
            while True:
                flow = self.dfs(source, float('Inf'), sink, ptr)
                if flow == 0:
                    break
                total_flow += flow

        return total_flow

# Пример использования
if __name__ == "__main__":
    # Создаем граф с 6 вершинами
    dinic = DinicAlgorithm(6)

    # Добавляем рёбра и их пропускные способности
    dinic.add_edge(0, 1, 16)
    dinic.add_edge(0, 2, 13)
    dinic.add_edge(1, 2, 10)
    dinic.add_edge(1, 3, 12)
    dinic.add_edge(2, 4, 14)
    dinic.add_edge(3, 2, 9)
    dinic.add_edge(3, 5, 20)
    dinic.add_edge(4, 3, 7)
    dinic.add_edge(4, 5, 4)

    # Вычисляем максимальный поток от истока (0) к стоку (5)
    max_flow_value = dinic.max_flow(0, 5)
    print(f"Максимальный поток: {max_flow_value}")
