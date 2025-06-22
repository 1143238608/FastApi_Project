# -*- coding: utf-8 -*-
"""
    @Time   : 2025/5/17 11:11
    @Author : mxy
"""


import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(device)