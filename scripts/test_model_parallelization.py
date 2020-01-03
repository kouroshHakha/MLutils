import torch.nn as nn
import torch
import GPUtil

class Model(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.sub_network1 = nn.Linear(10, 10)
        self.sub_network2 = nn.Linear(10, 10)

        availablity = GPUtil.getAvailability(GPUtil.getGPUs())
        self.available_devices = [i for i in range(len(availablity)) if availablity[i]==1]
        if len(self.available_devices) < 2:
            raise ValueError(f'there are only {len(self.available_devices)} cuda devices available')

        print(f'available devices: {self.available_devices}')
        self.sub_network1.cuda(self.available_devices[0])
        self.sub_network2.cuda(self.available_devices[1])

    def forward(self, x):
        x = x.cuda(self.available_devices[0])
        x = self.sub_network1(x)
        x = x.cuda(self.available_devices[1])
        x = self.sub_network2(x)
        return x

if __name__ == '__main__':
    xin = torch.rand((10, 10))
    model_parallel = Model()
    GPUtil.showUtilization()
    print(model_parallel(xin))

