# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:53:44 2022

@author: ScottStation
"""
import asyncio
import nest_asyncio
from qesdk2 import *
nest_asyncio.apply()

auth('quantease','$1$$k7yjPQKv8AJuZERDA.eQX.')

#print(repr(qesdk2))
df = asyncio.run(aio_get_bar_data(['AG2212.SFE'],'20220921'))
print(df)