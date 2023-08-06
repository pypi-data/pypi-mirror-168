# calculate:
# takes two floats
# calculates cost for a single data point

# derivative:
# takes two floats

class MeanSquaredError:
    def calculate(activation, expected_activation):
        return (expected_activation - activation) ** 2

    def derivative(activation, expected_activation):
        return (expected_activation - activation) * 2