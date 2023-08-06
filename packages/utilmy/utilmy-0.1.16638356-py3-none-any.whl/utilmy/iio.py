# -*- coding: utf-8 -*-
HELP= """ IO


"""
import os, glob, sys, math, string, time, json, logging, functools, random, yaml, operator, gc
from pathlib import Path; from collections import defaultdict, OrderedDict
# from utilmy import  to_file, date_now_jp
from box import Box


#####################################################################################



#####################################################################################
#####################################################################################
def test():
    """


    """
    pass





def screenshot( output='fullscreen.png', monitors=-1):
  """
  with mss() as sct:
    for _ in range(100):
        sct.shot()
  # MacOS X
  from mss.darwin import MSS as mss


  """
  try :
    # GNU/Linux
    from mss.linux import MSS as mss
  except :
    # Microsoft Windows
    from mss.windows import MSS as mss

  filename = sct.shot(mon= monitors, output= output)
  print(filename)





