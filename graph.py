class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_outgoing_edges(self, node):
        return [
            edge
            for edge in self.edges
            if edge.source == node
        ]

    def get_next_node(self, current_node, state):
                    edges = self.get_outgoing_edges(current_node)
            
                    for edge in edges:
                        if edge.condition is None or edge.condition(state):
                            return edge.target
            
                    return None

    def display(self):
        print("\nGraph:\n")

        outgoing = {}

        for edge in self.edges:
            outgoing.setdefault(edge.source, []).append(edge)

        targets = {edge.target for edge in self.edges}

        start_nodes = [
            node
            for node in self.nodes
            if node not in targets
        ]

        visited = set()

        for start_node in start_nodes:
            self.render(
                start_node,
                outgoing,
                visited
            )

        print()

    def render(self, node, outgoing, visited, prefix=""):
        if node in visited:
            print(f"{prefix}↳ {node.name} (already visited)")
            return

        visited.add(node)

        print(f"{prefix}┌──────────────┐")
        print(f"{prefix}│ {node.name:<12} │")
        print(f"{prefix}└──────────────┘")

        edges = outgoing.get(node, [])

        if not edges:
            return

        for index, edge in enumerate(edges):
            is_last = index == len(edges) - 1

            if len(edges) == 1:
                print(f"{prefix}       │")
                print(f"{prefix}       ▼")

                self.render(
                    edge.target,
                    outgoing,
                    visited,
                    prefix
                )

            else:
                branch = "└" if is_last else "├"

                print(
                    f"{prefix}       {branch}──────────────┐"
                )

                if edge.condition:
                    print(
                        f"{prefix}       "
                        f"{' ' * 4}"
                        f"[{edge.condition.__name__}]"
                    )

                child_prefix = prefix + (
                    "                      "
                    if is_last
                    else "       │              "
                )

                self.render(
                    edge.target,
                    outgoing,
                    visited,
                    child_prefix
                )