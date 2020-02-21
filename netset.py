import numpy as np
import scipy.special


class NetSet:
    def __init__(self, inp_nodes, hidd_nodes, out_nodes, rate):
        self.i_nodes = inp_nodes
        self.h_nodes = hidd_nodes
        self.o_nodes = out_nodes

        self.rate = rate

        self.wih = np.random.normal(
            0.0, pow(self.i_nodes, -0.5), (self.h_nodes, self.i_nodes))
        self.who = np.random.normal(
            0.0, pow(self.h_nodes, -0.5), (self.o_nodes, self.h_nodes))

        self.act_fun = lambda x: scipy.special.expit(x)

    def train(self, inpt, targ):
        target = [0.01] * 10
        target[targ] = 0.99

        inputs = np.array(inpt, ndmin=2).T
        tagets = np.array(target, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_out = self.act_fun(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_out)
        final_out = self.act_fun(final_inputs)

        out_err = tagets - final_out
        hid_err = np.dot(self.who.T, out_err)

        self.who += self.rate * \
            np.dot((out_err * final_out * (1.0 - final_out)),
                   np.transpose(hidden_out))

        self.wih += self.rate * \
            np.dot((hid_err * hidden_out * (1.0 - hidden_out)),
                   np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.act_fun(hidden_inputs)

        fin_inp = np.dot(self.who, hidden_outputs)
        fin_out = self.act_fun(fin_inp)

        return fin_out
