# Electrical Circuit Simulator

## Installation

To use the Electrical Circuit Simulator, you will need to have the following dependencies installed:

- `networkx`
- `numpy`
- `matplotlib`
- `sympy`

You can install these dependencies using pip:

```
pip install networkx numpy matplotlib sympy
```

## Usage

The `simulator.py` file contains the code for the Electrical Circuit Simulator. You can run the script to simulate the behavior of an electrical circuit.

The script defines a directed graph `GRAPH` that represents the circuit, and assigns properties to each edge in the graph, such as the type of component (voltage source, resistor, capacitor, or inductor) and its value.

The script then performs the following steps:

1. Constructs the minimum spanning tree (MST) of the graph.
2. Assigns a unique number to each edge in the graph, with the MST edges numbered first, followed by the "red" edges (edges not in the MST).
3. Initializes the tie-set matrix and the cut-set matrix, which are used to represent the relationships between the branch currents and voltages.
4. Solves for the branch currents and voltages in the Laplace domain, and then converts the results to the time domain using inverse Laplace transforms.
5. Plots the time-domain currents and voltages for each edge in the circuit.

To run the simulator, simply execute the `simulator.py` file:

```
python simulator.py
```

This will generate two plots, one for the currents and one for the voltages, which you can view and analyze.

## API

The `simulator.py` file defines the following functions and variables:

- `GRAPH`: a directed graph that represents the electrical circuit.
- `edge_properties`: a dictionary that maps each edge in the graph to its component type and value.
- `edge_numbering`: a dictionary that maps each edge in the graph to a unique number.
- `tie_set_matrix`: a matrix that represents the relationships between the branch currents and the link currents.
- `cut_matrix`: a matrix that represents the relationships between the branch voltages and the tree voltages.
- `branch_current_symbols`: a list of symbols representing the branch currents.
- `branch_voltage_symbols`: a list of symbols representing the branch voltages.
- `I_link`: a matrix of symbols representing the link currents.
- `V_tree`: a matrix of symbols representing the tree voltages.
- `time_domain_currents`: a list of functions that represent the time-domain branch currents.
- `time_domain_voltages`: a list of functions that represent the time-domain branch voltages.

## Contributing

If you would like to contribute to the Electrical Circuit Simulator, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

The Electrical Circuit Simulator is licensed under the [MIT License](LICENSE).

## Testing

To test the Electrical Circuit Simulator, you can run the `simulator.py` script and verify that the output matches your expectations. You can also add additional test cases to the script to ensure that it works correctly for a variety of circuit configurations.