#!/usr/bin/python
# -*-coding: utf-8 -*-

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle


fig = plt.figure(FigureClass=Waffle, height=10, values=[10, 20, 30], interval_ratio_x=0.2, interval_ratio_y=0.2,
                 colors=("#969696", "#1879bf", "#009bda"),
                 labels=("cat1", "cat2", "cat3"),
                 title_args={'label': 'Test Figure', 'loc': 'left', 'fontdict': {'fontsize': 10}})
plt.show()
