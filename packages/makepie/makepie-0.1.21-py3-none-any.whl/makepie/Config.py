import logging
from .Exceptions import MakepieException

log = logging.getLogger(__name__)

class Config:
	def __init__(self, _dict={}, support_edit=True):
		self.dict: dict = _dict
		self.support_edit = support_edit

	def unset(self, key):
		if not self.support_edit:
			raise MakepieException("Config is not editable")
		del self.dict[key]

	def config(self, key=None, default=None, throws=False, **kwargs):
		if kwargs != {}:
			# Update config
			if not self.support_edit:
				raise MakepieException("Config is not editable")
			self.dict.update(kwargs)

		# Retrieving key
		if key is None:
			return self.dict

		try:
			return self.dict[key]
		except KeyError as e:
			if throws:
				raise MakepieException(f"Config '{key}' was not found") from e

			log.info(f"Key '{key}' not found, using default '{default}'")
			return default

# Main config
_config = Config({}, support_edit=False)

def config(key=None, default=None, throws=False, **kwargs):
	return _config.config(key, default, throws, **kwargs)

def unsetconfig(key):
	_config.unset(key)
