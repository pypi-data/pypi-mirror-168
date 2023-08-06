import numpy as np

# calculate:
# takes an array with the shape(n,)

# calculate_single:
# takes a single float

# derivative:
# takes a single float

class Sigmoid:
    def calculate(weighted_inputs):
        result = []
        
        for weighted_input in weighted_inputs:
            result.append(Sigmoid.calculate_single(weighted_input))

        return result

    def calculate_single(weighted_input):
        return 1 / (1 + np.exp(-weighted_input))

    def derivative(weighted_input):
        activation = Sigmoid.calculate_single(weighted_input)
        return activation * (1 - activation)

class ReLU:
    def calculate(weighted_inputs):
        result = []
        
        for weighted_input in weighted_inputs:
            result.append(ReLU.calculate_single(weighted_input))

        return result

    def calculate_single(weighted_input):
        return max(0, weighted_input)

    def derivative(weighted_input):
        return int(weighted_input > 0)