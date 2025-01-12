# Import required libraries
from matplotlib import pyplot as plt
import networkx as nx

# Define functions to build and visualize diagrams for C4 models
def build_graph(tree, parent=None, graph=None):
    if graph is None:
        graph = nx.DiGraph()
    for key, value in tree.items():
        graph.add_node(key)
        if parent:
            graph.add_edge(parent, key)
        if isinstance(value, dict):
            build_graph(value, key, graph)
        else:
            graph.add_node(value)
            graph.add_edge(key, value)
    return graph

def draw_graph(graph, title, figsize=(12, 8)):
    plt.figure(figsize=figsize)
    pos = nx.nx_pydot.graphviz_layout(graph, prog="dot")
    nx.draw(graph, pos, with_labels=True, arrows=False, node_size=3000, font_size=10, node_color="lightblue")
    plt.title(title, fontsize=14)
    plt.show()

# Define structures for the C4 diagrams

# 1. Context Diagram
context = {
    "User": {
        "Optimization Service API": {
            "Auth Module": "Handles authentication",
            "Problem Management": "Manages optimization problems",
            "Preset Configurations": "Predefined optimization tasks",
            "Logs and Analytics": "Tracks and analyzes optimization usage"
        }
    }
}

# 2. Containers Diagram
containers = {
    "Optimization Service API": {
        "Web Server": {
            "Authentication Service": "Manages user authentication",
            "Optimization Engine": "Core solver for optimization problems",
            "Preset Manager": "Manages predefined configurations",
            "Analytics Service": "Handles logs and analytics"
        },
        "Database": {
            "Problems": "Stores problem definitions and solutions",
            "Presets": "Stores predefined configurations",
            "Logs": "Stores log entries and analytics data"
        }
    }
}

# 3. Components Diagram (for the Optimization Engine)
components = {
    "Optimization Engine": {
        "Input Validator": "Validates problem input data",
        "Solver Manager": {
            "Linear Solver": "Solves linear optimization problems",
            "Nonlinear Solver": "Handles nonlinear problems",
            "Integer Solver": "Solves integer programming problems"
        },
        "Result Formatter": "Formats and returns the solution"
    }
}

# 4. Code Diagram (Simplified example of Solver Manager implementation)
code_structure = {
    "Solver Manager": {
        "LinearSolver": {
            "solve_linear_problem()": "Executes linear optimization logic"
        },
        "NonlinearSolver": {
            "solve_nonlinear_problem()": "Executes nonlinear optimization logic"
        },
        "IntegerSolver": {
            "solve_integer_problem()": "Executes integer programming logic"
        }
    }
}

# Build and draw graphs for each C4 model
graphs = {
    "Context Diagram": build_graph(context),
    "Containers Diagram": build_graph(containers),
    "Components Diagram": build_graph(components),
    "Code Diagram": build_graph(code_structure)
}

# Draw all diagrams
for title, graph in graphs.items():
    draw_graph(graph, title)
