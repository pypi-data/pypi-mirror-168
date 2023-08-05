from distutils.version import Version
from functools import cached_property, lru_cache
import json
import logging
import re
import subprocess
import pkg_resources
from typing import Set
import sys
import importlib
import distutils.spawn
from packaging.version import parse as parse_version
from pkg_resources import Requirement

REQUIREMENTS = {
    "amal": ["deep", "amal"],
    "rld": ["deep", "rld"]
}

@lru_cache()
def cuda_version() -> Version:
    try:
        re_cuda = re.compile(br".*CUDA version: ([\d\.]+)", re.IGNORECASE)
        out = subprocess.check_output("nvidia-smi")
        for line in out.splitlines():
            if m := re_cuda.match(line):
                return parse_version(m.group(1).decode("utf-8"))
    except:
        pass
    logging.info("No CUDA detected")


@lru_cache
def packages():
    # First 2 lines, and last line are not packages
    re_split = re.compile(r"[\t\s]+")
    packages = {}
    for p in json.loads(subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format', 'json']).decode()):
        packages[p["name"].lower()] = p
    return packages

def has_requirement(requirement: Requirement):
    package = packages().get(requirement.project_name.lower(), None)
    if package is None:
        return False

    for comparator, desired_version in requirement.specs:
        desired_version = parse_version(desired_version)
        
        version = parse_version(package["version"])
        if comparator == '<=':
            return version <= desired_version
        elif comparator == '>=':
            return version >= desired_version
        elif comparator == '==':
            return version == desired_version
        elif comparator == '>':
            return version > desired_version
        elif comparator == '<':
            return version < desired_version


    return True
  

def install_package(requirement: Requirement):
    if has_requirement(requirement):
        logging.info("Package %s is already installed", requirement)
        return

    extra_args = []

    if requirement.key == "torch":
        if cuda_version() is None:
            pass
        elif cuda_version() >= parse_version("11.6"):
            extra_args = ["--extra-index-url", "https://download.pytorch.org/whl/cu116"]
        elif cuda_version() >= parse_version("11.3"):
            extra_args = ["--extra-index-url", "https://download.pytorch.org/whl/cu113"]

    logging.info("Installing %s", requirement)
    subprocess.check_call([sys.executable, "-m", "pip", "install", str(requirement)] + extra_args)

def install(name: str, processed: Set[str]):
    if name in processed:
        return

    path = importlib.resources.files("master_dac") / "requirements" / f"{name}.txt"

    for value in pkg_resources.parse_requirements(path.read_text()):
        install_package(value)

    processed.add(name)



def rld(processed: Set[str]):
    # Check that swig is installed
    if sys.platform == "win32":
        has_swig = distutils.spawn.find_executable("swig.exe")
    else:
        has_swig = distutils.spawn.find_executable("swig")

    if not has_swig:
        logging.error("swig n'est pas installé: sous linux utilisez le gestionnaire de paquets, sous windows télécharger swig sur http://www.swig.org")
        sys.exit(1)


    install("deep", processed)
    install("rld", processed)

def amal(processed: Set[str]):
    install("deep", processed)
    install("amal", processed)
