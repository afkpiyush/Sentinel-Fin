import networkx as nx
import pandas as pd

def build_transaction_graph(frame, source_col="source_account",
                             destination_col="destination_account", amount_col="amount"):
    required = {source_col, destination_col}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing graph columns: {sorted(required - set(frame.columns))}")
    graph = nx.DiGraph()
    for row in frame.itertuples(index=False):
        source, destination = str(getattr(row, source_col)), str(getattr(row, destination_col))
        amount = float(getattr(row, amount_col)) if amount_col in frame else None
        graph.add_edge(source, destination, amount=amount)
    return graph

def graph_features(graph):
    return pd.DataFrame([{"account": node, "in_degree": graph.in_degree(node),
                          "out_degree": graph.out_degree(node), "degree": graph.degree(node)}
                         for node in graph.nodes])
