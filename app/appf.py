import PySimpleGUI as sg
import os
import numpy as np
import pandas as pd
from dbfread import DBF
import re
import itertools
from pandas import Series, DataFrame

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from junciones import *
# parámetros y valores fijos
traerParametros()

print ("ef", traerParametros())