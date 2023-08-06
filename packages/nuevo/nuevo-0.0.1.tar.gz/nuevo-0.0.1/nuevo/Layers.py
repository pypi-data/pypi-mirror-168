import numpy as np

class InputLayer:
    def __init__(self, num_nodes):
        self.__num_nodes = num_nodes

    @property
    def num_nodes(self):
        return self.__num_nodes

class Dense:
    def __init__(self, num_nodes, activation):
        self.__num_nodes = num_nodes
        self.__activation_function = activation

    def initialize(self, num_inputs):
        self.__num_inputs = num_inputs

        self.__weights = np.random.random((self.__num_nodes, self.__num_inputs))
        self.__biases = np.zeros((1, self.__num_nodes))

        self.__gradientsWeights = np.zeros((self.__num_nodes, self.__num_inputs))
        self.__gradientsBiases = np.zeros((self.__num_nodes,))

    def forward_pass(self, inputs):
        # store inputs for backpropagation
        self.__inputs = inputs

        # the weighted_inputs and activations will be stored for backpropagation
        self.__weighted_inputs = np.dot(self.__weights, self.__inputs) + self.__biases
        
        # converting the shapes of weighted_inputs from (1, n) to (n,)
        # activations will have the same shape as weighted_inputs

        self.__weighted_inputs = self.__weighted_inputs[0]
        self.__activations = self.__activation_function.calculate(self.__weighted_inputs)

        return self.__activations

    def calculate_output_layer_node_values(self, expected_outputs, cost_function):
        self.__node_values = []

        for i in range(self.__num_nodes):
            activation = self.__activations[i]
            expected_output = expected_outputs[i]
            weighted_input = self.__weighted_inputs[i]

            # δc/δa:
            node_value = cost_function.derivative(activation, expected_output)

            # δa/δz:
            node_value *= self.__activation_function.derivative(weighted_input)

            self.__node_values.append(node_value)

        return self.__node_values

    def calculate_hidden_layer_node_values(self, next_node_values, next_layer_weights):
        self.__node_values = []
        next_num_nodes = len(next_node_values)

        for node in range(self.__num_nodes):
            # activation of this node
            activation = self.__activations[node]

            node_value = 0
            for next_node in range(next_num_nodes):
                # first get all weights of next_node
                # then, take the weights that's connected to node

                weight = next_layer_weights[next_node][node]
                next_node_value = next_node_values[next_node]

                node_value += next_node_value * weight

            weighted_input = self.__weighted_inputs[node]
            node_value *= self.__activation_function.derivative(weighted_input)

            self.__node_values.append(node_value)

        return self.__node_values

    def update_gradients(self):
        for node in range(self.__num_nodes):
            node_value = self.__node_values[node]

            for inp in range(self.__num_inputs):
                # update gradient for weights[node][inp]

                gradient = self.__inputs[inp] * node_value
                self.__gradientsWeights[node][inp] += gradient
            
            # update gradient for biases[node]

            gradient = node_value
            self.__gradientsBiases[node] += gradient

    def apply_gradients(self, learn_rate):
        for node in range(self.__num_nodes):
            for inp in range(self.__num_inputs):
                # apply gradient for weights[node][inp]

                gradient = self.__gradientsWeights[node][inp]
                self.__weights[node][inp] += gradient * learn_rate

            # applys gradient for biases[node]

            gradient = self.__gradientsBiases[node]
            self.__biases[0][node] += gradient * learn_rate

    def clear_gradients(self):
        self.__gradientsWeights = np.zeros((self.__num_nodes, self.__num_inputs))
        self.__gradientsBiases = np.zeros((self.__num_nodes,))

    @property
    def num_nodes(self):
        return self.__num_nodes

    @property
    def weights(self):
        return self.__weights