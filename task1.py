from collections import deque, defaultdict

# =========================
# EDMONDS-KARP
# =========================
class EdmondsKarp:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        if u not in self.graph[v]:
            self.graph[v][u] = 0

    def bfs(self, s, t, parent):
        visited = {s}
        q = deque([s])

        while q:
            u = q.popleft()
            for v, cap in self.graph[u].items():
                if v not in visited and cap > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == t:
                        return True
                    q.append(v)
        return False

    def max_flow(self, s, t):
        max_flow = 0

        while True:
            parent = {}
            if not self.bfs(s, t, parent):
                break

            path_flow = float("inf")
            v = t

            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u

            v = t
            while v != s:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                self.flow[u][v] += path_flow
                v = u

            max_flow += path_flow

        return max_flow

# =========================
# BUILD GRAPH
# =========================
def build_network():
    ek = EdmondsKarp()

    S, T = "S", "T"
    T1, T2 = "T1", "T2"
    W1, W2, W3, W4 = "W1", "W2", "W3", "W4"

    stores = [f"M{i}" for i in range(1, 15)]

    # super source
    ek.add_edge(S, T1, 60)
    ek.add_edge(S, T2, 55)

    # terminals → warehouses
    ek.add_edge(T1, W1, 25)
    ek.add_edge(T1, W2, 20)
    ek.add_edge(T1, W3, 15)

    ek.add_edge(T2, W3, 15)
    ek.add_edge(T2, W4, 30)
    ek.add_edge(T2, W2, 10)

    # warehouses → stores
    ek.add_edge(W1, "M1", 15)
    ek.add_edge(W1, "M2", 10)
    ek.add_edge(W1, "M3", 20)

    ek.add_edge(W2, "M4", 15)
    ek.add_edge(W2, "M5", 10)
    ek.add_edge(W2, "M6", 25)

    ek.add_edge(W3, "M7", 20)
    ek.add_edge(W3, "M8", 15)
    ek.add_edge(W3, "M9", 10)

    ek.add_edge(W4, "M10", 20)
    ek.add_edge(W4, "M11", 10)
    ek.add_edge(W4, "M12", 15)
    ek.add_edge(W4, "M13", 5)
    ek.add_edge(W4, "M14", 10)

    # stores → sink
    for m in stores:
        ek.add_edge(m, T, 100)

    return ek, S, T

# =========================
# CORRECT DECOMPOSITION
# =========================
def decompose_terminal_store(ek):
    result = defaultdict(float)

    terminals = ["T1", "T2"]
    warehouses = ["W1", "W2", "W3", "W4"]

    # total inflow to warehouse
    inflow = defaultdict(float)
    for t in terminals:
        for w in warehouses:
            inflow[w] += ek.flow[t].get(w, 0)

    # distribute proportionally
    for w in warehouses:
        if inflow[w] == 0:
            continue

        for m, f_wm in ek.flow[w].items():
            if not m.startswith("M") or f_wm == 0:
                continue

            for t in terminals:
                f_tw = ek.flow[t].get(w, 0)
                if f_tw > 0:
                    share = f_tw / inflow[w] * f_wm
                    result[(t, m)] += share

    return result

# =========================
# PRINT RESULTS
# =========================
def print_results(ek, max_flow, flow_tm):
    print("\n" + "=" * 60)
    print(f"МАКСИМАЛЬНИЙ ПОТІК: {max_flow}")
    print("=" * 60)

    print("\nТермінал → Склад")
    print("-" * 60)
    for t in ["T1", "T2"]:
        for w, f in ek.flow[t].items():
            if f > 0:
                print(f"{t:<6}{w:<6}{f:<6}")

    print("\nСклад → Магазин")
    print("-" * 60)
    for w in ["W1", "W2", "W3", "W4"]:
        for m, f in ek.flow[w].items():
            if m.startswith("M") and f > 0:
                print(f"{w:<6}{m:<6}{f:<6}")

    print("\nТермінал → Магазин (ФІНАЛЬНА ТАБЛИЦЯ)")
    print("-" * 60)
    for (t, m), f in sorted(flow_tm.items()):
        print(f"{t:<6}{m:<6}{round(f, 2):<6}")

# =========================
# ANALYSIS
# =========================
def analyze(ek, flow_tm, max_flow):
    print("\n" + "=" * 60)
    print("АНАЛІЗ")
    print("=" * 60)

    # terminal flow
    t_flow = defaultdict(float)
    for (t, _), f in flow_tm.items():
        t_flow[t] += f

    print("\n1. Потік терміналів:")
    for t, v in t_flow.items():
        print(f"   {t}: {round(v, 2)}")

    # store flow
    s_flow = defaultdict(float)
    for (_, m), f in flow_tm.items():
        s_flow[m] += f

    weakest = sorted(s_flow.items(), key=lambda x: x[1])[:5]

    print("\n2. Найслабші магазини:")
    for m, v in weakest:
        print(f"   {m}: {round(v, 2)}")

    print("\n3. Вузькі місця:")
    for t in ["T1", "T2"]:
        for w in ek.graph[t]:
            if ek.graph[t][w] == 0:
                print(f"   {t} → {w}")

    print("\n4. Висновок:")
    print(f"   Max Flow = {max_flow}")
    print("   Потік оптимальний (augmenting paths відсутні)")

# =========================
# MAIN
# =========================
def main():
    ek, S, T = build_network()

    max_flow = ek.max_flow(S, T)

    flow_tm = decompose_terminal_store(ek)

    print_results(ek, max_flow, flow_tm)
    analyze(ek, flow_tm, max_flow)

if __name__ == "__main__":
    main()
