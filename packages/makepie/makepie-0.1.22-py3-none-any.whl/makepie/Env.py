import os, re
from pathlib import Path
from .Exceptions import MakepieException
from .Config import Config

class Env(Config):
	def config(self, key=None, default=None, throws=False, **kwargs):
		for value in kwargs.values():
			if type(value) != str:
				raise MakepieException(f"Env values must be strings: {value}")
				
		return super().config(key, default, throws, **kwargs)

# Env functions
_env = Env(os.environ)

def env(key=None, default=None, throws=False, **kwargs):
	return _env.config(key, default, throws, **kwargs)

def unsetenv(key):
	_env.unset(key)

key_val_reg = re.compile(r"^(?P<key>\w+)=(?P<value>.*)\b", re.M)
def env_file_parse(file:Path) -> dict:
	result = {}
	for match in key_val_reg.finditer(file.read_text()):
		result[match.group("key")] = match.group("value")
	return result

# Load env from file with key=value format
def env_load(file:Path):
	env(**env_file_parse(file))
