from .inputstools import *
from .inputs import *
from .inputlib import *

all_ = []
from .inputstools import __all__
all_ += __all__
from .inputs import __all__
all_ += __all__
from .inputlib import __all__
all_ += __all__

__all__ = list(set(all_))
del all_
__version__ = "0.2.0"
__author__ = 'Alawi Hussein Adnan Al Sayegh'
__description__ = 'library of input functions. and an input API'

#__all__ = ['keys_', 'input_wait_for', 'check_input', 'limit_input', 'ignore_input', 'subprocess_input', 'system_input',
#			'SubString', 'cmdlexer', 'input_', 'any_input', 'char_input', 'key_input', 'password_input_', 
#			'password_input', 'amazing_input', 'commandline_input', 'any_input_', 'String', 'built_in_events_Input',
#			'InputExit', 'InputDeadLock', 'Input', 'urlparse_input', 'urlparse_input_','yn_input','regex_input']

def random_lower_upper_case(string,seed=None):
	if seed is not None:
		random.seed(seed)
	return random.choice(str.lower,str.upper)(string)
def random_lower_upper_case_chars(string:"list or str",seed=None):
	if seed is not None:
		random.seed(seed)
	return [random.choice(str.lower,str.upper)(char) for char in string]