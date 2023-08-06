from distutils.version import Version
from functools import lru_cache
import json
import logging
import re
import subprocess
import pkg_resources
from typing import Set
import sys
import distutils.spawn
from packaging.version import parse as parse_version
from pkg_resources import Requirement
import easypip

try:
    from importlib.resources import files as resources_files
except:
    from importlib_resources import files as resources_files

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


def install_package(requirement: Requirement):
    if easypip.has_requirement(requirement):
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
    easypip.install(requirement, extra_args)

def install(name: str, processed: Set[str]):
    if name in processed:
        return

    path = resources_files("master_dac") / "requirements" / f"{name}.txt"

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
        logging.error("swig n'est pas installé: sous linux utilisez le gestionnaire de paquets: sous windows téléchargez swig sur http://www.swig.org, sous ubuntu: sudo apt install swig")
        sys.exit(1)


    install("deep", processed)
    install("rld", processed)

def amal(processed: Set[str]):
    install("deep", processed)
    install("amal", processed)
