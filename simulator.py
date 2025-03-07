
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# # DIRECTED GRAPH USED. (U,V) REPRESENTS AN EDGE  FROM NODE 'U' TO NODE 'V'.
GRAPH = nx.DiGraph()
GRAPH.add_edge(1, 2)
GRAPH.add_edge(2, 3)
GRAPH.add_edge(3, 4)
GRAPH.add_edge(4,1)
GRAPH.add_edge(3,1)


edge_properties = {
    (1, 2): ("V", 1),
    (2, 3): ("R", 1),
    (3, 4): ("R" ,5),
    (4, 1): ("L", 1),
    (3,1): ("C", 1/3),
   
   
}

s, t = sp.symbols('s t', real=True) # LAPLACE AND TIME  DOMAIN SYMBOLS

for (edge,(component_type, value)) in edge_properties.items():
    if component_type == "V":
        edge_properties[edge] = ("V", value / s)
    elif component_type == "C":
        edge_properties[edge] = ("C", 1 / (value * s))
    elif component_type == "L":
        edge_properties[edge] = ("L", s * value)


#  MINIMUM SPANNING TREE (CONSIDERED AS UNDIRECTED)
# 'MST' IS UNDIRECTED. 'GRAPH' WAS DIRECTED.
MST = nx.minimum_spanning_tree(GRAPH.to_undirected())

# VISUALIZING THE GRAPH  AND MST
pos = nx.spring_layout(GRAPH)
nx.draw_networkx_nodes(GRAPH, pos, node_color="lightblue", node_size=520)
nx.draw_networkx_edges(GRAPH, pos, edge_color="grey", arrows=True ,arrowsize=30)    # DIRECTED GRAPH IS SHOWN WITH GREY COLOR( i.e with arrow)
nx.draw_networkx_labels(GRAPH, pos, font_size=15, font_family="DejaVu Sans")
nx.draw_networkx_edges(MST, pos, edge_color="green", width=3)     # DIRECTED GRAPH IS SHOWN WITH GREY COLOR (i.e without arrow)
plt.axis("off")
plt.show()


# NUMBERING OF EDGES. ( CONVENTION :FIRST NUMBERING IS DONE FOR MST BRANCHES . THEN FOR 'RED' BRANCHES...)
# (CONVENTION : 'RED' SYMBOL IS IS USED TO DENOTE THE BRANCHES WHICH IS NOT THE PART OF MST  i.e co-tree branches).

edge_numbering = {} #DICTIONARY  FOR (U,V)->NUMBER ASSIGNED
edge_counter = 1

#  GETTING A NEW GRAPH WHICH IS DIRECTED FORM OF MST
directed_MST = nx.DiGraph()
for (u,v) in MST.edges():
    if GRAPH.has_edge(u,v):
        directed_MST.add_edge(u,v)
    else:
        directed_MST.add_edge(v,u)
    edge_numbering[(u,v) if GRAPH.has_edge(u,v) else (v,u)] = edge_counter
    edge_counter+=1

# NUMBERING THE RED EDGES 
for edge in GRAPH.edges():
    if edge not in directed_MST.edges():
        edge_numbering[edge] = edge_counter
        edge_counter+=1

 # Print the edges with their numbering
# print("Edge numbering (MST edges first, then red edges):")
# for edge, number in edge_numbering.items():
#     print(f"Edge {edge} -> Number {number}")

print("Edge numbering (MST edges first, then RED edges), including properties:")
for (edge,number) in edge_numbering.items():
    (component,value) = edge_properties[edge]
    print(f" Edge {edge} : Number {number}, Component: {component}, Value: {value} ")


################################################################################################################################


# TIE-SET MATRIX INITIALISATION
num_total_edges = len(GRAPH.edges())
num_MST_edges =len(MST.edges())
num_red_edges = ( num_total_edges - num_MST_edges ) #i.e. no of co-tree edges
tie_set_matrix = np.zeros( (num_red_edges, num_total_edges), dtype=int )

#IF A RED EDGE IS ADDED TO THE MST A CYCLE IS FORMED....
print("\nCycles formed by adding each red edge to the MST:")
cycle_index = 0  # Row index for tie-set matrix


# ITERATING THROUGH EACH RED EDGE TO FIND THE CYCLES FORMED BY ADDING IT TO THE MST
for edge in GRAPH.edges():
    if edge not in directed_MST.edges():  # ie. RED EDGE
        
        # Creating a temporary directed graph with (directed_MST + red edge)
        temp_graph = directed_MST.copy()
        temp_graph.add_edge(*edge)

        # CONVERTING IT INTO UNDIRECTED GRAPH TO DETECT CYCLE
        undirected_temp = temp_graph.to_undirected()

        
        try:
            cycle = nx.find_cycle(undirected_temp, source=edge[0])
            print(f"Red edge {edge} (Number {edge_numbering[edge]}) forms cycle:", cycle)

            # FILLING THE TIE-SET MATRIX
            for (u,v) in cycle:
                if (u, v) in edge_numbering:
                    col = edge_numbering[(u, v)] - 1  # Column for this edge number
                    tie_set_matrix[cycle_index][col] = -1  # Aligns with removed edge direction
                elif (v, u) in edge_numbering:
                    col = edge_numbering[(v, u)] - 1  # Column for this edge number
                    tie_set_matrix[cycle_index][col] = 1  # Opposite direction

            cycle_index += 1  # Move to the next row in the tie-set matrix

        except nx.NetworkXNoCycle:
            print(f"Red edge {edge} (Number {edge_numbering[edge]}) does not form a cycle.")

cut_matrix = np.zeros( ( len(MST.edges()) , num_total_edges ), dtype=int )

def fill_matrix_with_identity(n, m):
    identity_matrix = np.eye(n)
    result_matrix = np.zeros((n, m), dtype=int)
    result_matrix[:, :n] = identity_matrix
    return result_matrix
    
cut_matrix = fill_matrix_with_identity(num_MST_edges,  num_total_edges)

for i in range(num_red_edges):
    for j in range(num_MST_edges):
        cut_matrix[j][num_MST_edges+ i] = -tie_set_matrix[i][j]


#  tie-set matrix
print("\nTie-set matrix (rows correspond to removed edges, columns correspond to all edges):")
print(tie_set_matrix)
# cut-set matrix
print("\nCut matrix:")
print(cut_matrix)

################################################################################################################################

# Number of edges and the number of link currents
#num_total_edges = len(GRAPH.edges())
# num_link_currents = len(GRAPH.edges()) - len(MST.edges())

# CREATE SYMBOLS DYNAMICALLY FOR BRANCH CURRENTS AND VOLTAGES
branch_current_symbols = sp.symbols(f'i1:{num_total_edges + 1}')  # i1, i2, ..., i(num_total_edges)
branch_voltage_symbols = sp.symbols(f'v1:{num_total_edges + 1}')  # v1, v2, ..., v(num_total_edges)

# ASSIGNING SYMBOLS FOR LINK CURRENTS (UPPERCASE I) AND TREE VOLTAGES (UPPERCASE V)
I_link = sp.Matrix([sp.symbols(f'I{i}') for i in range(num_MST_edges + 1, num_total_edges + 1)])  # LINK CURRENTS
V_tree = sp.Matrix([sp.symbols(f'V{i}') for i in range(1, num_MST_edges + 1)])  # MST VOLTAGES

# RELATIONS PROVIDED:
# 1. [TIE_SET_MATRIX]^T * I_LINK = I_EACH_EDGE
I_each_edge = sp.Matrix(branch_current_symbols)  # ALL CURRENT SYMBOLS (LOWER CASE i)
tie_set_relation = sp.Eq((tie_set_matrix.T * I_link), I_each_edge)

# 2. [CUT_SET_MATRIX]^T * V_TREE = V_EACH_EDGE
V_each_edge = sp.Matrix(branch_voltage_symbols)  # ALL VOLTAGE SYMBOLS (LOWER CASE v)
cut_set_relation = sp.Eq(cut_matrix.T * V_tree, V_each_edge)

# DISPLAY RELATIONS
print("TIE-SET RELATION (FOR CURRENTS):")
sp.pprint(tie_set_relation)

print("\nCUT-SET RELATION (FOR VOLTAGES):")
sp.pprint(cut_set_relation)

##################################################################################################################################

# Adding relations for capital voltages based on edge properties
capital_V_relationships = {}  #KEY->EDGE NUMBER , VALUE->PRPOERTY 2
for (edge, number) in edge_numbering.items():
    (component, value) = edge_properties[edge]
    if component == "V":  # Voltage source
        capital_V_relationships[number] = value  # Direct value
    else:  # Resistor
        capital_V_relationships[number] = sp.symbols(f'i{number}') * value  # Relation to small i

# SUBSTITUTING small i_j from the tie-set relation into the capital V relationships
# for (edge,number) in edge_numbering.items():
#     if edge in capital_V_relationships:
#         v_j_expr = capital_V_relationships[number]
#         # Substitute small i_j with the corresponding I_link variable
#         for j in range(len(I_link)):
#             v_j_expr = v_j_expr.subs(sp.symbols(f'i{number}'), I_link[j])  # Substitute small current with capital current
#         capital_V_relationships[number] = v_j_expr  # Update the expression


# for (edge,number) in edge_numbering.items():
#     if edge in capital_V_relationships:
#         capital_V_relationships[number]= sp.symbols(f'i{number}')

# Substitute the expressions into the cut-set relation
for j in range(len(V_tree)):
    capital_index = j + 1  # Because our numbering starts from 1
    if capital_index in capital_V_relationships:
        cut_set_relation = cut_set_relation.subs(V_tree[j], capital_V_relationships[capital_index])

# Display relations
print("\nCut-set relation (for voltages):")
sp.pprint(cut_set_relation)

#branch_current_symbols = sp.symbols(f'i1:{num_total_edges + 1}')  # i1, i2, ..., i(num_total_edges)

# Create a system of equations from the tie-set relation
tie_set_eqs = [tie_set_relation.lhs[i] - tie_set_relation.rhs[i] for i in range(len(tie_set_relation.lhs))]

# Solve for small currents (i_j) in terms of capital currents (I_j)
small_currents_solution = sp.solve(tie_set_eqs, branch_current_symbols)

# Substitute small currents into the cut-set relation
for j in range(len(I_each_edge)):
    if branch_current_symbols[j] in small_currents_solution:
        cut_set_relation = cut_set_relation.subs(branch_current_symbols[j], small_currents_solution[branch_current_symbols[j]])

# Display the modified cut-set relation
print("\nModified Cut-set relation (after substituting i_j in terms of capital I_j):")
sp.pprint(cut_set_relation)



##################################################################################################################################


k = len(GRAPH.edges()) - len(MST.edges())  #NUMBER OF RED EDGES

# Extract the last k equations from the cut-set relation
cut_set_last_k_eqs = cut_set_relation.lhs[-k:]
cut_set_last_k_rhs = cut_set_relation.rhs[-k:]

# Display the last k equations (LHS and RHS)
print(f"\nLast {k} equations of the modified Cut-set relation:")
for (lhs, rhs) in zip(cut_set_last_k_eqs, cut_set_last_k_rhs):
    sp.pprint(sp.Eq(lhs, rhs))



# Replace RHS elements of the last k equations based on edge properties
modified_cut_set_last_k_eqs = []

for (lhs,rhs) in zip(cut_set_last_k_eqs, cut_set_last_k_rhs):
    # Iterate through all edges and update RHS terms
    updated_rhs = rhs
    for (edge,number) in edge_numbering.items():
        (component,value) = edge_properties[edge]

        # Replace v_i based on edge properties
        v_symbol = sp.symbols(f'v{number}')  # Symbol for voltage v_i
        if component == "V":  # Voltage source
            updated_rhs = updated_rhs.subs(v_symbol, value)  
        elif component in {"R", "C", "L"}:  
            I_symbol = sp.symbols(f'I{number}')  # Symbol for current I_i
            updated_rhs = updated_rhs.subs(v_symbol, value * I_symbol)  # Replace v_i with value * I_i

    # Append the modified equation to the list
    modified_cut_set_last_k_eqs.append(sp.Eq(lhs, updated_rhs))


print(f"\nModified Last {k} equations of the Cut-set relation (RHS replaced):")
for eq in modified_cut_set_last_k_eqs:
    sp.pprint(eq)
I_symbols = [sp.symbols(f'I{len(MST.edges()) + i + 1}') for i in range(k)]  # Link currents

# Extract LHS and RHS for solving
equations = [eq.lhs - eq.rhs for eq in modified_cut_set_last_k_eqs]

# Solve the equations for I_i
solutions = sp.solve(equations, I_symbols)

# Display the solutions for each I_i

print("\nSolutions for I_i (link currents) in terms of s (direction changed):")
for (I_symbol, solution) in solutions.items():
    sp.pprint(sp.Eq(I_symbol, (-1)*solution))

# all i_i (currents through edges) in terms of s
all_currents = []
for i, branch_current in enumerate(I_each_edge):
    current_expr = (-1)*tie_set_relation.lhs[i]  # Directly use the LHS of the tie-set relation
    for I_symbol, solution in solutions.items():
        current_expr = current_expr.subs(I_symbol, solution)  # Substitute independent I_i values
    all_currents.append(sp.simplify(current_expr))

#  all v_i (voltages across edges) in terms of s
all_voltages = []
for (i, branch_voltage) in enumerate(V_each_edge):
    voltage_expr = cut_set_relation.lhs[i]  # Directly use the LHS of the cut-set relation
    for (I_symbol, solution) in solutions.items():
        voltage_expr = voltage_expr.subs(I_symbol, solution)  # Substitute independent I_i values
    all_voltages.append(sp.simplify(voltage_expr))

# Display results
print("\nAll currents (i_i) through edges in terms of s:")
for i, current_expr in enumerate(all_currents, start=1):
    sp.pprint(sp.Eq(sp.symbols(f'i{i}'), current_expr))

print("\nAll voltages (v_i) across edges in terms of s:")
for i, voltage_expr in enumerate(all_voltages, start=1):
    sp.pprint(sp.Eq(sp.symbols(f'v{i}'), voltage_expr))

################################################################################################################################


from sympy import inverse_laplace_transform, symbols, simplify
t = symbols('t', real=True, positive=True)

# TIME-DOMAIN CURRENTS i_i(t)
time_domain_currents = []
for i, current_expr in enumerate(all_currents):
    current_time_expr = inverse_laplace_transform(current_expr, s, t)
    time_domain_currents.append(simplify(current_time_expr))

# TIME-DOMAIN VOLTAGES v_i(t)
time_domain_voltages = []
for i, voltage_expr in enumerate(all_voltages):
    voltage_time_expr = inverse_laplace_transform(voltage_expr, s, t)
    time_domain_voltages.append(simplify(voltage_time_expr))

# DISPLAY RESULTS
print("\nALL CURRENTS (i_i) THROUGH EDGES IN TERMS OF t:")
for i, current_time_expr in enumerate(time_domain_currents, start=1):
    sp.pprint(sp.Eq(sp.symbols(f'i{i}(t)'), current_time_expr))

print("\nALL VOLTAGES (v_i) ACROSS EDGES IN TERMS OF t:")
for i, voltage_time_expr in enumerate(time_domain_voltages, start=1):
    sp.pprint(sp.Eq(sp.symbols(f'v{i}(t)'), voltage_time_expr))



################################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from sympy import inverse_laplace_transform, symbols, lambdify

# Define symbolic time variable
t = symbols('t', real=True, positive=True)

# Compute time-domain currents i_i(t)
time_domain_currents = []
for (i, current_expr) in enumerate(all_currents):
    current_time_expr = inverse_laplace_transform(current_expr, s, t)
    current_time_func = lambdify(t,current_time_expr, "numpy")
    time_domain_currents.append(current_time_func)

# Compute time-domain voltages v_i(t)
time_domain_voltages = []
for i, voltage_expr in enumerate(all_voltages):
    voltage_time_expr = inverse_laplace_transform(voltage_expr, s, t)
    # Convert to a lambda function for numerical evaluation
    voltage_time_func = lambdify(t, voltage_time_expr, "numpy")
    time_domain_voltages.append(voltage_time_func)

# Define a time range for plotting
time_values = np.linspace(0, 10, 1000)  # Adjust this range as needed

# Evaluate the functions over the time range for currents and voltages
i_values = []
for i_t_func in time_domain_currents:
    i_result = i_t_func(time_values)
    if np.ndim(i_result) == 0:  # Check if the result is a constant
        i_values.append(np.full_like(time_values, i_result))
    else:
        i_values.append(i_result)

# Debugging: check if voltage functions can handle time_values
v_values = []
for v_t_func in time_domain_voltages:
    try:
        v_result = v_t_func(time_values)
        if np.ndim(v_result) == 0:  # If result is a constant, handle it as such
            v_values.append(np.full_like(time_values, v_result))
        else:
            v_values.append(v_result)
    except Exception as e:
        print(f"Error evaluating voltage function: {e}")
        v_values.append(np.zeros_like(time_values))  # Fallback to zeros if there's an error

# Convert v_values to a NumPy array
v_values = np.array(v_values)

# Plot all currents i_i(t) in one graph
plt.figure(figsize=(15, 7.5))
for i in range(len(i_values)):
    plt.plot(time_values, abs(i_values[i]), label=f'i_{i+1}(t)')
plt.title('Currents i_i(t) vs Time')
plt.xlabel('Time (t)')
plt.ylabel('Current (i_i(t))')
plt.legend()
plt.grid(True)
plt.show()

# Plot all voltages v_i(t) in one graph
plt.figure(figsize=(15, 7.5))
for i in range(len(v_values)):
    plt.plot(time_values, abs(v_values[i]), label=f'v_{i+1}(t)')
plt.title('Voltages v_i(t) vs Time')
plt.xlabel('Time (t)')
plt.ylabel('Voltage (v_i(t))')
plt.legend()
plt.grid(True)
plt.show()




