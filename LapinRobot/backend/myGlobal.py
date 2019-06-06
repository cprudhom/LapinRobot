# coding: utf-8

'''
file to init global variables in every files imported as glob
'''

tdata = []
ydata = []
NB_PARAMETERS = 6  # nb of colums we read in the file
state = 0  # 0 : repos // 1 : adrenaline // 2 : acetylcholine
need_change_file = False