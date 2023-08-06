import os, json, logging, sys, shutil, yaml
from pathlib import Path

from .Config import *
from .Env import *
from .MakepieLogging import applog, logging_load
from .Decorators import *
from .Version import *
from .Caches import *
from .Exceptions import *
from .Utils import *
from .ShellCmd import *
from .Environement import *

log = applog
init_log = logging.getLogger(__name__)

def makepie_load(**base_config):
	# Load makepie config
	config().update(**base_config)

	logging_load()
	
	# Try loading optional config
	try:
		env_load(config("ENV_FILE", ".env"))
	except Exception as e:
		init_log.info(f"Warning: Could not load optional config: {e}")

	init_log.debug(f"Loaded makepie")

# Makepie Facade
__all__ = [
	"makepie_load",
	"config",
	"log",
	"macro",
	"cache",
	"default",
	"Version",
	"MakepieException",
	"FileCache",
	"Environment",
	"DEV",
	"LOC",
	"STA",
	"TES",
	"PRE",
	"PRO",
	"env",
	"unsetenv",
	"rm",
	"cp",
	"mv",
	"rfile",
	"wfile",
	"replace",
	"tplsubst",
	"glob",
	"sh",
	"logging",
	"os",
	"shutil",
	"json",
	"sys",
	"yaml",
	"Path",
	"cd",
	"autocomplete",
]
