##  batch 16    /rpcan-rcspan batch 16  Enhanced RCSPAN
from model import common
#from os import closerange # Tolou
import torch.nn as nn
import skimage.measure
from MyEntropy1 import MyEntropy1
from CalVariance import CalVAriance
from CalContrastbatch import CalContrastbatch
import torch    # tolou
from pathlib import Path # Tolou
import math
import numpy

def make_model(args, parent=False):
    return RCAN(args)

## Channel Attention (CA) Layer
class CALayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(CALayer, self).__init__()
        # global average pooling: feature --> point
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        # Use Varince Instead of  AVG
        #self.avg_pool = CalVAriance()
        # feature channel downscale and upscale --> channel weight
        self.conv_du = nn.Sequential(
                nn.Conv2d(channel, channel // reduction, 1, padding=0, bias=True),
               # nn.ReLU(inplace=True),
                #nn.Conv2d(channel // reduction, channel, 1, padding=0, bias=True),
               ## #nn.Conv2d(channel , channel, 1, padding=0, bias=True),
               # nn.Sigmoid()
        )
        self.conv2_du = nn.Sequential(
                nn.Conv2d(channel, channel // reduction, 1, padding=0, bias=True),
               # nn.ReLU(inplace=True),
                #nn.Conv2d(channel // reduction, channel, 1, padding=0, bias=True),
               ### #nn.Conv2d(channel , channel, 1, padding=0, bias=True),
               # nn.Sigmoid()
        )
        self.conv3_du = nn.Sequential(
               # nn.Conv2d(channel, channel // reduction, 1, padding=0, bias=True),
                nn.ReLU(inplace=True),
                nn.Conv2d(channel // reduction, channel, 1, padding=0, bias=True),
               ### #nn.Conv2d(channel , channel, 1, padding=0, bias=True),
                nn.Sigmoid()
        )
        
    def forward(self, x):
        y1 = self.avg_pool(x)
        y1 = self.conv_du(y1)
        y2=CalContrastbatch(x)
        y2 = self.conv2_du(y2)
        y=y1+y2
        y = self.conv3_du(y)
      #  b=x*y
      #  SaveVar={'x-channels':x,'Y-AVG':y } # TOLOU
       # torch.save(SaveVar,path/'CA-Channels')  #['figure_' num2str(n) ] TOLOU
        return x * y
## Residual Channel Attention Block (RCAB)
class RCAB(nn.Module):
    def __init__(
        self, conv, n_feat, kernel_size, reduction,
        bias=True, bn=False, act=nn.ReLU(True), res_scale=1):

        super(RCAB, self).__init__()
        modules_body = []
        for i in range(2):
            modules_body.append(conv(n_feat//2, n_feat//2, kernel_size, bias=bias))
            modules_body.append(conv(n_feat//2, n_feat//2, kernel_size, bias=bias))
            if bn: modules_body.append(nn.BatchNorm2d(n_feat))
            if i == 0: modules_body.append(act)
        modules_body.append(CALayer(n_feat, reduction))
        self.body = nn.Sequential(*modules_body)
        self.res_scale = res_scale
    def forward(self, x):
        res1 = self.body[0](x[:,:32,:,:])
        res2 = self.body[1](x[:,32:,:,:])
        res = torch.cat([res1,res2],dim=1)
        res=self.body[2](res)
        res1 = self.body[3](res[:,:32,:,:])
        res2 = self.body[4](res[:,32:,:,:])
        res = torch.cat([res1,res2],dim=1)
        res= self.body[5](res)
        res += x
        return res
 

## Residual Group (RG)
class ResidualGroup(nn.Module):
    def __init__(self, conv, n_feat, kernel_size, reduction, act, res_scale, n_resblocks):
        super(ResidualGroup, self).__init__()
        modules_body = []
        modules_body = [
            RCAB(
                conv, n_feat, kernel_size, reduction, bias=True, bn=False, act=nn.ReLU(True), res_scale=1) \
            for _ in range(n_resblocks)]
        modules_body.append(conv(n_feat, n_feat, kernel_size))
        self.body = nn.Sequential(*modules_body)

    def forward(self, x):
        res = self.body(x)
        res += x
        return res


## Residual Channel Attention Network (RCAN)
class RCAN(nn.Module):
    def __init__(self, args, conv=common.default_conv):
        super(RCAN, self).__init__()
        
        n_resgroups = args.n_resgroups
        n_resblocks = args.n_resblocks   # I think its number of RCAB(AMIN)
        n_feats = args.n_feats
        kernel_size = 3
        reduction = args.reduction 
        scale = args.scale[0]
        act = nn.ReLU(True)
        
        # RGB mean for DIV2K
        self.sub_mean = common.MeanShift(args.rgb_range)
        
        # define head module
        modules_head = [conv(args.n_colors, n_feats, kernel_size)]

        # define body module
        modules_body = [
            ResidualGroup(
                conv, n_feats, kernel_size, reduction, act=act, res_scale=args.res_scale, n_resblocks=n_resblocks) \
            for _ in range(n_resgroups)]

        modules_body.append(conv(n_feats, n_feats, kernel_size))

        # define tail module
        modules_tail = [
            common.Upsampler(conv, scale, n_feats, act=False),
            conv(n_feats, args.n_colors, kernel_size)]

        self.add_mean = common.MeanShift(args.rgb_range, sign=1)

        self.head = nn.Sequential(*modules_head)
        self.body = nn.Sequential(*modules_body)
        self.tail = nn.Sequential(*modules_tail)

    def forward(self, x):
        x = self.sub_mean(x)
        x = self.head(x)

        res = self.body(x)
        res += x

        x = self.tail(res)
        x = self.add_mean(x)

        return x 
    
    #def count_parameters(model):
           # return sum(p.numel() for p in model.parameters() if p.requires_grad)
    #print(count_parameters(model))

    def load_state_dict(self, state_dict, strict=False):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') >= 0:
                        print('Replace pre-trained upsampler to new one...')
                    else:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

        if strict:
            missing = set(own_state.keys()) - set(state_dict.keys())
            if len(missing) > 0:
                raise KeyError('missing keys in state_dict: "{}"'.format(missing))
