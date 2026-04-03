import pandas as pd
from scc import find_sccs

# Load the CSV
df = pd.read_csv('wikiRfA.csv')

# Build graph: dict[str, list[str]]
graph = {}
for _, row in df.iterrows():
    source = row['SOURCE']
    target = row['TARGET']
    
    if source not in graph:
        graph[source] = []
    graph[source].append(target)
    
    # Ensure all nodes exist in graph
    if target not in graph:
        graph[target] = []

# Find strongly connected components
sccs = find_sccs(graph)

# Write results to file
with open('sccs_output.txt', 'w') as f:
    f.write(f"Found {len(sccs)} SCCs\n")
    for i, component in enumerate(sccs):
        f.write(f"SCC {i}: {component}\n")
    
print("Results written to sccs_output.txt")