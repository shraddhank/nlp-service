########################################################################
# File: Singleton.py
########################################################################

""" Singleton metaclass implementation
"""

class Singleton( type ):
  """ simple singleton pattern using metaclass

  If you want to make your class a singleton, just set its  __metaclass__ to 
  Singleton, i.e.::

  from R88R.Core.Utilities.Singleton import Singleton
  class CheesShop( object ):
    __metaclass__ = Singleton
    ...

  """
  def __init__( cls, name, bases, dic ):
    """ c'tor
    """
    super( Singleton, cls ).__init__( name, bases, dic )
    cls.instance = None

  def __call__( cls, *args, **kwargs ):
    """ get the only one instance of cls
    """
    if cls.instance is None:
      cls.instance = super( Singleton, cls ).__call__( *args, **kwargs )
    return cls.instance
