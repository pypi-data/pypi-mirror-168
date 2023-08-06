import torch.nn as nn
import torch
import torch.nn.functional as F


class DSequential(nn.Sequential):
    # """
    # 调试方便
    # """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_run = False

    def forward(self, x):
        for idx, (name, module) in enumerate(self.named_children()):
            input_size = x.size()
            if self.first_run:
                print(f"module({name})#{idx} {input_size}")
            try:
                x = module(x)
                output_size = x.size()

                if self.first_run:
                    print(f"module({name})#{idx} {input_size} => {output_size}")
            except Exception as ex:
                if self.first_run:
                    print(f"module({name})#{idx} {input_size} => error")
                raise ex

        self.first_run = False
        return x


class BasicConv2d(nn.Sequential):
    def __init__(self, input_channels, output_channels, activation: str = 'relu', inplace: bool = True, **kwargs):
        super(BasicConv2d, self).__init__()
        self.out_channels = output_channels

        self.add_module('conv', nn.Conv2d(input_channels, output_channels, **kwargs))
        self.add_module('bn', nn.BatchNorm2d(output_channels))

        if activation == 'relu':
            self.add_module('relu', nn.ReLU(inplace=inplace))
        elif activation == 'swish':
            self.add_module('swish', nn.Hardswish(inplace=inplace))


class ShortcutBlock(nn.Module):
    def __init__(self, block: nn.Module):
        super().__init__()
        self.block = block

    def forward(self, x):
        out = self.block(x)
        return torch.concat([x, out], dim=1)


if __name__ == '__main__':
    x = torch.normal(0, 1, (256, 10))
    module = DSequential()
    module.add_module("v1", nn.Linear(10, 20))
    module.append(nn.Linear(20, 20))

    module(x)