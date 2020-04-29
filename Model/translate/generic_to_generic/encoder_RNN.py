import torch
from torch.autograd import Variable
import torch.nn as nn


class EncoderRNN(nn.Module):
    """
    class for the encoder
    """
    def __init__(self, input_size, hidden_size, layers=1, dropout=0.1, bidirectional=True):
        super(EncoderRNN, self).__init__()
        if bidirectional:
            self.directions = 2
        else:
            self.directions = 1
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = layers
        self.dropout = dropout
        self.embedder = nn.Embedding(input_size, hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.lstm = nn.LSTM(input_size=hidden_size, hidden_size=hidden_size, num_layers=layers, dropout=dropout,
                            bidirectional=bidirectional, batch_first=False)
        self.fc = nn.Linear(hidden_size*self.directions, hidden_size)

    def forward(self, input_data, h_hidden, c_hidden):
        embedded_data = self.embedder(input_data)
        embedded_data = self.dropout(embedded_data)
        hiddens, outputs = self.lstm(embedded_data, (h_hidden, c_hidden))
        return hiddens, outputs

    def create_init_hiddens(self, batch_size):
        """
        creates initial hidden states for encoder corresponding to batch size
        :param batch_size: the size of the batch
        :return: initial hidden states
        """
        h_hidden = Variable(torch.zeros(self.num_layers*self.directions, batch_size, self.hidden_size))
        c_hidden = Variable(torch.zeros(self.num_layers*self.directions, batch_size, self.hidden_size))
        return h_hidden.cuda(), c_hidden.cuda()  # .cuda()


