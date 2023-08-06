import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from mindify.vision.modules.base import BasicConv2d

# 卷积块的注意力模块（Convolutional Block Attention Module）
# https://zhuanlan.zhihu.com/p/83665899


class ChannelGate(nn.Module):
    def __init__(self, gate_channels, reduction_ratio=16, pool_types=None, weight_alg='sigmoid'):
        """
        通道注意力
        :param gate_channels: 特征通道数
        :param reduction_ratio: 压缩比
        :param pool_types: 通常都是 avg + max
        """
        super(ChannelGate, self).__init__()

        self.pool_types = ['avg', 'max'] if pool_types is None else pool_types
        self.weight_alg = weight_alg
        self.gate_channels = gate_channels
        # MLP 多层感知机 Multi-Layer Perceptron
        self.mlp = nn.Sequential(
            nn.Flatten(),
            nn.Linear(gate_channels, gate_channels // reduction_ratio),
            nn.ReLU(),
            nn.Linear(gate_channels // reduction_ratio, gate_channels)
        )

    def forward(self, x):
        # 多个 pool 合并的结果
        channel_att_sum = None
        for pool_type in self.pool_types:
            if pool_type == 'avg':
                # 下面代码效果和 nn.AdaptiveAvgPool2d 一样
                avg_pool = F.avg_pool2d(x, (x.size(2), x.size(3)), stride=(x.size(2), x.size(3)))
                channel_att_raw = self.mlp(avg_pool)
            elif pool_type == 'max':
                # nn.AdaptiveMaxPool2d
                max_pool = F.max_pool2d(x, (x.size(2), x.size(3)), stride=(x.size(2), x.size(3)))
                channel_att_raw = self.mlp(max_pool)
            elif pool_type == 'lp':
                # 功率平均池化 https://pytorch.org/docs/stable/generated/torch.nn.LPPool2d.html
                lp_pool = F.lp_pool2d(x, 2, (x.size(2), x.size(3)), stride=(x.size(2), x.size(3)))
                channel_att_raw = self.mlp(lp_pool)
            elif pool_type == 'lse':
                # LogSumExp 顾名思义就是 log(sum(e^x))
                lse_pool = self.logsumexp_2d(x)
                channel_att_raw = self.mlp(lse_pool)
            else:
                raise f"unknown pool_type {pool_type}"

            # 输入的尺寸是 BxCxWxH, channel_att_sum 和 channel_att_raw 尺寸是 BxC
            if channel_att_sum is None:
                channel_att_sum = channel_att_raw
            else:
                channel_att_sum = channel_att_sum + channel_att_raw

        # F.sigmoid(channel_att_sum).unsqueeze(2).unsqueeze(3) 在 BxC 上增加2，3维度，变成 BxCx1x1
        # expand_as(x) 把 BxCx1x1 扩展为 BxCxWxH，便于和 x 相乘，获得注意力特征图
        # scale 就是通道注意力因子，表示每个通道的权重
        if self.weight_alg == 'normalize':
            min, max = torch.min(channel_att_sum), torch.max(channel_att_sum)
            scale = (channel_att_sum - min) / (max - min + 1e-12)
        elif self.weight_alg == 'sigmoid':
            scale = torch.sigmoid(channel_att_sum)
        else:
            raise f"unknown weight_alg {self.weight_alg}"

        scale = scale.unsqueeze(2).unsqueeze(3).expand_as(x)
        return x * scale

    @classmethod
    def logsumexp_2d(cls, tensor):
        tensor_flatten = tensor.view(tensor.size(0), tensor.size(1), -1)
        s, _ = torch.max(tensor_flatten, dim=2, keepdim=True)
        outputs = s + (tensor_flatten - s).exp().sum(dim=2, keepdim=True).log()
        return outputs


class ChannelPool(nn.Module):
    def __init__(self):
        super().__init__()
        self.max_pool = nn.MaxPool2d(1)

    def forward(self, x):
        # 对每个像素位的所有通道值取最大值，torch.max(x, 1) 有点像 argmax, 第二个数组返回位置
        # BxCxWxH -> BxWxH -> Bx1xWxH
        x_max = torch.max(x, 1)[0].unsqueeze(1)
        # BxCxWxH -> BxWxH -> Bx1xWxH
        x_avg = torch.mean(x, 1).unsqueeze(1)

        # 输出 Bx2xWxH，后面会用一个 2->1 的卷积把通道数再变成1
        x = torch.cat((x_max, x_avg), dim=1)
        return x


class SpatialGate(nn.Module):
    def __init__(self, kernel_size=7, weight_alg='sigmoid'):
        """
        空间注意力
        """
        super(SpatialGate, self).__init__()

        self.weight_alg = weight_alg
        self.compress = ChannelPool()
        self.spatial = BasicConv2d(2, 1, kernel_size=kernel_size, stride=1, padding=(kernel_size - 1) // 2, activation=False)

    def forward(self, x):
        # 输出 Bx2xWxH
        x_compress = self.compress(x)
        # 输出 Bx1xWxH
        x_out = self.spatial(x_compress)
        # 计算像素位的权重, 输出 Bx1xWxH
        if self.weight_alg == 'normalize':
            min, max = torch.min(x_out), torch.max(x_out)
            scale = (x_out - min) / (max - min + 1e-12)
        elif self.weight_alg == 'sigmoid':
            scale = torch.sigmoid(x_out) # broadcasting
        else:
            raise f"unknown weight_alg {self.weight_alg}"

        # 给每个通道的特征图乘以WxH的权重
        return x * scale


class CBAMBlock(nn.Module):
    def __init__(self, gate_channels, reduction_ratio=16, pool_types=None, no_spatial=False, weight_alg='sigmoid'):
        super(CBAMBlock, self).__init__()
        self.pool_types = ['avg', 'max'] if pool_types is None else pool_types

        self.ChannelGate = ChannelGate(gate_channels, reduction_ratio, self.pool_types, weight_alg=weight_alg)
        self.no_spatial = no_spatial
        if not no_spatial:
            self.SpatialGate = SpatialGate(weight_alg=weight_alg)

    def forward(self, x):
        x_out = self.ChannelGate(x)
        if not self.no_spatial:
            x_out = self.SpatialGate(x_out)
        return x_out


if __name__ == '__main__':
    inputs = torch.normal(0., 0.5, (128, 64, 28, 28))
    channel_gate = ChannelGate(64, weight_alg='normalize')
    cg_outputs = channel_gate(inputs)

    spatial_gate = SpatialGate(weight_alg='normalize')
    sg_outputs = spatial_gate(cg_outputs)

    print(cg_outputs.size(), sg_outputs.size())

