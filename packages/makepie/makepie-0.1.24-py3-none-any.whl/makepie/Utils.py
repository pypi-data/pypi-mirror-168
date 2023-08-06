import logging, re, shutil, os
from pathlib import Path

from .Exceptions import MakepieException
from .Env import env

log = logging.getLogger(__name__)

# --- File operations ---
def rfile(path:str, default=None, throws=True):
	try:
		with open(path, 'r') as f:
			return f.read()
	except Exception as e:
		if throws:
			raise MakepieException(f"Could not read file {path}") from e
		log.info(f"Could not read file {path}: {e}")
		return default

def wfile(path:str, content:str):
	with open(path, 'w') as f:
		f.write(content)

# Allow to select multiple files matching a Unix glob pattern
def glob(pattern:str, root:str="."):
	return list(map(str, Path(root).glob(pattern)))

def rm(*patterns, ignore_errors=False):
	for pattern in patterns:
		if isinstance(pattern, Path):
			files = [str(pattern)]
		else:
			files = glob(pattern)
			
		if len(files) == 0 and not ignore_errors:
			raise MakepieException(f"No file found matching {pattern}")

		for file in files:
			if os.path.isfile(file):
				try:
					os.remove(file)
				except Exception as e:
					if not ignore_errors:
						raise MakepieException(f"Could not remove file {file}") from e
			elif os.path.isdir(file):
				shutil.rmtree(file, ignore_errors=ignore_errors)
			else:
				raise MakepieException(f"{file} is not a file or directory")

def cp(src:str, dst:str, overwrite=False, **kwargs):
	# Single file copy
	if os.path.isfile(src) and not os.path.isdir(dst) and not dst.endswith(("/", "\\")):
		if os.path.exists(dst) and not overwrite:
			raise MakepieException(f"Destination file {dst} already exists")
			
		shutil.copy(src, dst)
		return
	
	# Glob copy
	files = glob(src)
	for file in files:
		if os.path.isfile(file):
			shutil.copy(file, dst)
		elif os.path.isdir(file):
			shutil.copytree(file, dst, **kwargs)
		else:
			raise MakepieException(f"{file} is not a file or directory")

def mv(src:str, dst:str, overwrite=False):
	files = glob(src)
	for file in files:
		try:
			shutil.move(file, dst)
		except shutil.Error as e:
			log.warning(f"Could not move {file} to {dst}: {e}")
			# Try to copy then remove
			cp(file, dst, overwrite=overwrite)
			rm(file)

def mkdir(path:str, mode=0o777, make_parents=True, exist_ok=False):
	if make_parents:
		os.makedirs(path, mode, exist_ok)
	else:
		try:
			os.mkdir(path, mode)
		except FileExistsError as e:
			if not exist_ok:
				raise e

# Regex need to have a named group named "key"
def replace(content: str, values: dict, regex, throws=True):
	def _replace(match: re.Match):
		try:
			result = values[match.group("key")]
			log.info(f"Replacing {match.group(0)} with '{result}'")
			return result
		except KeyError as e:
			if throws:
				raise MakepieException(f"Key '{match.group('key')}' not found") from e

	return re.sub(regex, _replace, content)

# envsubst alike using replace
env_var_reg = r"\$\{?(?P<key>\w+)\}?"
def tplsubst(file:str, out_file=None, throws=True, var_regex=env_var_reg, **environment):
	content = rfile(file)

	if environment == {}:
		environment = env()
	if out_file is None:
		out_file = file.replace(".tpl", "")

	result = replace(content, environment, var_regex, throws)

	wfile(out_file, result)

def dict2env(d: dict) -> str:
	return "\n".join([f"{k}={v}" for k, v in d.items()])

# Load a .env file into a dict
def env2dict(path: Path) -> dict:
	env = {}
	with open(path) as stream:
		for line in stream:
			if line.startswith("#"):
				continue
			k, v = line.split("=", 1)
			env[k] = v.strip()
	return env

class WorkingDirContextManager:
	def __init__(self, path):
		self.path = path
		self.old_cwd = os.getcwd()

	def __enter__(self):
		os.chdir(self.path)

	def __exit__(self, exc_type, exc_val, exc_tb):
		os.chdir(self.old_cwd)

# TODO write tests for this
def cd(path: str):
	return WorkingDirContextManager(path)

def autocomplete(needle, haystack, throws=True):
	matches = list(filter(lambda x: x.startswith(needle), haystack))
	if len(matches) == 1:
		return matches[0]
	if not throws:
		return None
	if len(matches) > 1:
		raise Exception(f"Ambiguous option '{needle}' (matches: {matches})")
	raise Exception(f"Can't autocomplete '{needle}' from {haystack}")
