"""
GAM toolkit
"""

from __future__ import absolute_import

from .pygam import GAM
from .pygam import LinearGAM
from .pygam import LogisticGAM
from .pygam import GammaGAM
from .pygam import PoissonGAM
from .pygam import InvGaussGAM
from .pygam import ExpectileGAM

from .terms import l
from .terms import s
from .terms import f
from .terms import te
from .terms import intercept

__all__ = ['GAM', 'LinearGAM', 'LogisticGAM', 'GammaGAM', 'PoissonGAM',
           'InvGaussGAM', 'ExpectileGAM', 'l', 's', 'f', 'te', 'intercept']

__version__ = '0.8.1'
