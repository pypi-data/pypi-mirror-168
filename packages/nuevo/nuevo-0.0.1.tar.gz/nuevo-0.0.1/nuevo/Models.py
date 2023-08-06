import nuevo.Layers

class Sequential:
    def __init__(self, input_layer, hidden_layers, output_layer):
        self.__input_layer = input_layer
        self.__hidden_layers = hidden_layers
        self.__output_layer = output_layer

        self.__hidden_and_output_layers = list(self.__hidden_layers).copy()
        self.__hidden_and_output_layers.append(self.__output_layer)

        self.__all_layers = self.__hidden_and_output_layers.copy()
        self.__all_layers.insert(0, self.__input_layer)

        for i in range(1, len(self.__all_layers)):
            layer = self.__all_layers[i]
            prev_layer = self.__all_layers[i - 1]
            layer.initialize(prev_layer.num_nodes)

    def run(self, inputs):
        if len(inputs) != self.__input_layer.num_nodes:
            print("run: Invalid input dimensions.")
            return

        # the "result" of the first layer are the inputs
        last_layer_result = inputs

        for layer in self.__hidden_and_output_layers:
            outputs = layer.forward_pass(last_layer_result)
            last_layer_result = outputs

        return last_layer_result

    def learn(self, inputs, labels, epochs, batch_size, cost, learn_rate=0.3):
        for epoch in range(epochs):
            batch = inputs # split batch up

            # do an entire forward pass first
            # each layer will store the inputs it's received

            batch_cost = 0.0
            outputs = []

            for i in range(len(batch)):
                output = self.run(batch[i])
                # print("otput, label", output[0], labels[i][0])
                outputs.append(output)
                batch_cost += cost.calculate(output[0], labels[i][0])
                self.calculate_all_node_values(labels[i], cost)
                self.update_all_gradients()

            print("Epoch %d:" % epoch)
            print("\tOutputs:", outputs)
            print("\tCost:", batch_cost)
            print("")

            # we are dividing by len(batch) since we are increasing
            # each gradient len(batch) times
            # this way, the learn_rate parameter will behave
            # independently of the batch size
            self.apply_all_gradients(learn_rate / len(batch))

            for layer in self.__hidden_and_output_layers:
                layer.clear_gradients()
            
    def calculate_all_node_values(self, labels, cost):
        next_node_values = self.__output_layer.calculate_output_layer_node_values(labels, cost)        

        # loop through all hidden layers backwards
        for i in range(len(self.__hidden_and_output_layers) - 2, -1, -1):
            layer = self.__hidden_and_output_layers[i]
            next_layer = self.__hidden_and_output_layers[i + 1]

            next_node_values = layer.calculate_hidden_layer_node_values(next_node_values, next_layer.weights)

    def update_all_gradients(self):
        for layer in self.__hidden_and_output_layers:
            layer.update_gradients()

    def apply_all_gradients(self, learn_rate):
        for layer in self.__hidden_and_output_layers:
            layer.apply_gradients(learn_rate)