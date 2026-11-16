import networkx as nx
import pandas as pd

def build_transaction_graph(frame, source_col="source_account", destination_col="destination_account", amount_col="amount", timestamp_col="timestamp"):
    required = {source_col, destination_col}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing graph columns: {sorted(required - set(frame.columns))}")
    graph = nx.MultiDiGraph()
    for idx, row in frame.iterrows():
        attrs = {"amount": float(row[amount_col]) if amount_col in frame and pd.notna(row[amount_col]) else None,
                 "timestamp": str(row[timestamp_col]) if timestamp_col in frame else None, "transaction_id": str(row.get("transaction_id", idx))}
        graph.add_edge(str(row[source_col]), str(row[destination_col]), key=str(row.get("transaction_id", idx)), **attrs)
    return graph

def graph_features(graph):
    rows=[]
    for node in graph.nodes:
        in_edges=list(graph.in_edges(node, data=True)); out_edges=list(graph.out_edges(node, data=True))
        rows.append({"account":node,"in_degree":len(in_edges),"out_degree":len(out_edges),"degree":len(in_edges)+len(out_edges),
                     "weighted_in_amount":sum((d.get("amount") or 0) for _,_,d in in_edges),
                     "weighted_out_amount":sum((d.get("amount") or 0) for _,_,d in out_edges)})
    return pd.DataFrame(rows)
