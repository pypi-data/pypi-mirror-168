import math

import torch
import torch.nn as nn

from mindify.vision.modules import CBAMBlock


def conv3x3(in_channels, out_channels, stride=1):
    """
    3x3 convolution with padding
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride,
                     padding=1, bias=False)


def conv1x1(in_channels, out_channels):
    """
    3x3 convolution with padding
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False)


class ResBasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, expansion=1, cbam: bool = False):
        """

        :param in_channels:
        :param out_channels:
        :param stride:
        :param downsample: 下采样模块
        :param expansion: 扩充比
        """
        super().__init__()
        self.conv1 = conv3x3(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels * expansion)
        self.bn2 = nn.BatchNorm2d(out_channels * expansion)
        self.cbam = CBAMBlock(out_channels * expansion) if cbam else None

        if out_channels * expansion != in_channels:
            self.identity = nn.Conv2d(in_channels, out_channels * expansion, 1, stride=stride, bias=False)
        else:
            self.identity = None

        self.stride = stride

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.cbam is not None:
            out = self.cbam(out)

        if self.identity is not None:
            identity = self.identity(x)
        else:
            identity = x

        out += identity
        out = self.relu(out)

        return out


class ResBottleneckBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, expansion=4, cbam: bool = False):
        """

        :param in_channels:
        :param out_channels:
        :param stride:
        :param expansion: 通道扩充比例
        :param cbam: 是否使用 CBAM
        """
        super().__init__()
        self.conv1 = conv1x1(in_channels, out_channels)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = conv3x3(out_channels, out_channels, stride)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = conv1x1(out_channels, out_channels * expansion)
        self.bn3 = nn.BatchNorm2d(out_channels * expansion)
        self.relu = nn.ReLU(inplace=True)
        self.cbam = CBAMBlock(out_channels * expansion) if cbam else None

        if out_channels * expansion != in_channels:
            self.identity = nn.Conv2d(in_channels, out_channels * expansion, 1, stride=stride, bias=False)
        else:
            self.identity = None

        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.cbam is not None:
            out = self.cbam(out)

        if self.identity is not None:
            identity = self.identity(x)
        else:
            identity = x

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):

    def __init__(self, input_channels, block, layers, init_channels=64, num_classes=1000):
        super(ResNet, self).__init__()

        self.conv1 = nn.Conv2d(input_channels, init_channels, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.in_channels = init_channels

        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def _make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * block.expansion),
            )

        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.in_channels, out_channels))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x


def resnet18_cbam(**kwargs):
    """Constructs a ResNet-18 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = ResNet(ResBasicBlock, [2, 2, 2, 2], **kwargs)
    return model


def resnet34_cbam(**kwargs):
    """Constructs a ResNet-34 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = ResNet(ResBasicBlock, [3, 4, 6, 3], **kwargs)
    return model


def resnet50_cbam(**kwargs):
    """Constructs a ResNet-50 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = ResNet(ResBottleneckBlock, [3, 4, 6, 3], **kwargs)
    return model


def resnet101_cbam(**kwargs):
    """Constructs a ResNet-101 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = ResNet(ResBottleneckBlock, [3, 4, 23, 3], **kwargs)
    return model


def resnet152_cbam(**kwargs):
    """Constructs a ResNet-152 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = ResNet(ResBottleneckBlock, [3, 8, 36, 3], **kwargs)
    return model


if __name__ == '__main__':
    inputs = torch.normal(0., 0.5, (128, 64, 28, 28))

    module = ResBasicBlock(64, 128, expansion=2, cbam=True)
    outputs = module(inputs)
    print(outputs.size())

    module = ResBottleneckBlock(64, 128, expansion=2, cbam=True)
    outputs = module(inputs)
    print(outputs.size())
