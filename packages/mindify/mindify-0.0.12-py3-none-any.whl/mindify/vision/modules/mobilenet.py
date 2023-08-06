from collections import OrderedDict

import torch
import torch.nn as nn
import torch.nn.functional as F


class MobileBlock(nn.Sequential):
    def __init__(self, in_channels, out_channels, activation='relu', stride=1, padding=1, dropout=0.):
        super().__init__()

        """
        MobileBlock 的中心思想是深度可分离卷积，普通的卷积是用卷积核在每个特征图某一位置计算后的结果在所有通道层叠加起来，深度可分离卷积
        则是先做深度卷积，每个特征图自己做，所以这里的groups=in_channels, 卷积核是 3x3 不是 Cx3x3
        """
        self.add_module('conv1', nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride, padding=padding,
                                           groups=in_channels, bias=False))
        self.add_module('bn1', nn.BatchNorm2d(in_channels))
        if activation == 'relu':
            self.add_module('relu1', nn.ReLU(inplace=True))
        else:
            self.add_module('swish1', nn.Hardswish(inplace=True))
        """
        在 Depthwise 的操作中，不难发现，这样的计算根本无法整合不同通道的信息，因为上一步把所有通道都拆开了，
        所以在这一步要用C×1×1的卷积核去整合不同通道上的信息，用out_channels个C×1×1的卷积核，产生out_channels×W×H的特征图。
        """
        self.add_module('conv2', nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False))
        self.add_module('bn2', nn.BatchNorm2d(out_channels))
        if activation == 'relu':
            self.add_module('relu2', nn.ReLU(inplace=True))
        else:
            self.add_module('swish2', nn.Hardswish(inplace=True))

        if dropout > 0.:
            self.add_module('dropout3', nn.Dropout(p=dropout, inplace=True))


class MobileNet(nn.Module):
    # (128,2) means conv planes=128, conv stride=2,
    # by default conv stride=1
    def __init__(self, config=None, num_classes=10):
        super(MobileNet, self).__init__()

        self.config = [64, (128, 2), 128, (256, 2), 256, (512, 2), 512, 512, 512, 512, 512, (1024, 2),
                       1024] if config is None else config
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(32)
        self.layers = self._make_layers(in_channels=32)
        self.linear = nn.Linear(1024, num_classes)

    def _make_layers(self, in_channels):
        layers = []
        for x in self.config:
            out_planes = x if isinstance(x, int) else x[0]
            stride = 1 if isinstance(x, int) else x[1]
            layers.append(MobileBlock(in_channels, out_planes, stride))
            in_channels = out_planes
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layers(out)
        out = F.avg_pool2d(out, 2)
        # https://zhuanlan.zhihu.com/p/244768971 作者做的一个尝试
        # out = F.adaptive_avg_pool2d(out, output_size=1)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out


if __name__ == '__main__':
    net = MobileNet()
    x = torch.randn(1, 3, 32, 32)
    y = net(x)
    print(y.size())
