"""
Module bundling all functions needed to run a SIESTA calculation or analyse SIESTA output files
"""
from __future__ import absolute_import
import glob
import os
from subprocess import Popen
from subprocess import run as sprun
import shlex
from itertools import zip_longest
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelmin, argrelmax
from sh import tail
from .helpers import (
    create_fdf,
    read_fdf,
    read_energy,
    get_it,
    print_run,
    check_restart,
    check_userbasis,
    copy_file,
    sort_,
    remove_nones
)


class Settings:
    """Settings"""

    def __init__(self):
        """Initialise settings"""
        self.cwd = os.getcwd()
        self.log = "log"
        self.cores = None
        self.conda = None
        self.cont = "continue"
        self.contfiles = []
        self.contextensions = ["psf", "fdf"]
        self.siesta = "siesta"

    def get_cwd(self):
        """Get cwd value"""
        return self.cwd

    def set_cwd(self, newcwd):
        """Set cwd value"""
        self.cwd = newcwd

    def get_log(self):
        """Get log value"""
        return self.log

    def set_log(self, newlog):
        """Set log value"""
        self.log = newlog

    def get_cores(self):
        """Get cores value"""
        return self.cores

    def set_cores(self, newcores):
        """Set cores value"""
        self.cores = newcores

    def get_conda(self):
        """Get conda value"""
        return self.conda

    def set_conda(self, newconda):
        """Set conda value"""
        self.conda = newconda

    def get_cont(self):
        """Get cont value"""
        return self.cont

    def set_cont(self, newcont):
        """Set cont value"""
        self.cont = newcont

    def get_siesta(self):
        """Get siesta value"""
        return self.siesta

    def set_siesta(self, newsiesta):
        """Set siesta value"""
        self.siesta = newsiesta


settings = Settings()


def run_next(i, label):
    """Run SIESTA for given step"""
    logs = glob.glob(f"i{int(i) - 1}{os.sep}{settings.get_log()}")
    logs += glob.glob(f"i{int(i) - 1}{os.sep}{settings.get_cont()}*{os.sep}{settings.get_log()}")
    logs = sort_(logs, "i*", settings.get_cont())
    if logs and settings.get_cont() in logs[-1]:
        match = re.search(f"i{int(i) - 1}{os.sep}{settings.get_cont()}(_*[0-9]*)", logs[-1])
        if not os.path.isfile(f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{label}.fdf"):
            ani_to_fdf(
                f"i{int(i) - 1}{os.sep}{settings.get_cont()}{match[1]}{os.sep}{label}.ANI",
                f"i{int(i) - 1}{os.sep}{settings.get_cont()}{match[1]}{os.sep}{label}.fdf",
                f"i{i}{os.sep}{label}.fdf"
            )
        copy_files(
            ["ion" if check_userbasis(f"i{i}{os.sep}{label}.fdf") else "psf"],
            label,
            f"{settings.get_cwd()}{os.sep}i{int(i) - 1}{os.sep}{settings.get_cont()}{match[1]}",
            f"{settings.get_cwd()}{os.sep}i{i}"
        )
    elif int(i) > 1:
        if not os.path.isfile(f"{settings.get_cwd()}{os.sep}i{str(int(i) + 1)}{os.sep}{label}.fdf"):
            ani_to_fdf(
                f"i{int(i) - 1}{os.sep}{label}.ANI",
                f"i{int(i) - 1}{os.sep}{label}.fdf",
                f"i{i}{os.sep}{label}.fdf"
            )
        copy_files(
            ["ion" if check_userbasis(f"i{i}{os.sep}{label}.fdf") else "psf"],
            label,
            f"{settings.get_cwd()}{os.sep}i{int(i) - 1}",
            f"{settings.get_cwd()}{os.sep}i{i}"
        )

    os.chdir(f"{settings.get_cwd()}{os.sep}i{i}")
    print(f"Changed directory to {os.getcwd()}")
    print_run(f"i{i}", settings.get_cores(), settings.get_conda())
    _command(label=label)


def single_run(i, label):
    """Run SIESTA for given step without continuing next step"""
    os.chdir(f"{settings.get_cwd()}{os.sep}i{i}")
    print(f"Changed directory to {os.getcwd()}")
    with open(
        f"{settings.get_cwd()}{os.sep}i{int(i) - 1}{os.sep}{settings.get_log()}",
        "r",
        encoding="utf-8"
        ) as file:
        lines = file.readlines()
        if lines[-1] == "Job completed\n":
            print(f"i{i}{os.sep}{settings.get_log()}: Job completed")
        else:
            if int(i) > 1:
                if not os.path.isfile(f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{label}.fdf"):
                    ani_to_fdf(
                        f"{settings.get_cwd()}{os.sep}i{int(i) - 1}{os.sep}{label}.ANI",
                        f"{settings.get_cwd()}{os.sep}i{int(i) - 1}{os.sep}{label}.fdf",
                        f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{label}.fdf"
                    )
                copy_files(
                    ["ion" if check_userbasis(
                        f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{label}.fdf"
                        ) else "psf"],
                    label,
                    f"{settings.get_cwd()}{os.sep}i{int(i) - 1}",
                    f"{settings.get_cwd()}{os.sep}i{i}"
                )
            print_run(f"i{i}", settings.get_cores(), settings.get_conda())
            _command(label=label, issingle=True)


def ani_to_fdf(anipath, fdfpath, newfdfpath):
    """Convert last geometry of an ANI to FDF by using the previous FDF and ANI files"""
    print(f"Reading {anipath}")
    with open(anipath, "r", encoding="utf-8") as anifile:
        geo = anifile.read()
        number = geo.split("\n", 1)[0].strip()
        geo = geo.split(number + "\n \n")[-1]
        geo = geo.splitlines()
        fdf, geo = read_fdf(fdfpath, geo)
        create_fdf(fdf, geo, newfdfpath, number)
        anifile.close()


def xyz_to_fdf(xyzpath, fdfpath, newfdfpath):
    """Convert XYZ to FDF by using the previous FDF and XYZ files"""
    print(f"Reading {xyzpath}")
    with open(xyzpath, "r", encoding="utf-8") as xyzfile:
        geo = xyzfile.read()
        number = geo.split("\n", 1)[0].strip()
        geo = geo.splitlines()[2:]
        fdf, geo = read_fdf(fdfpath, geo)
        create_fdf(fdf, geo, newfdfpath, number)
        xyzfile.close()


def merge_ani(label=None, path=None):
    """Merge ANI files"""
    if path is None:
        path = "i*"
    if label is None:
        raise ValueError("ERROR: Please set a label")
    files = glob.glob(f"{settings.get_cwd()}{os.sep}{path}{os.sep}{label}.ANI")
    files += glob.glob(
        f"{settings.get_cwd()}{os.sep}{path}{os.sep}{settings.get_cont()}*{os.sep}{label}.ANI"
        )
    files = sort_(files, path, settings.get_cont())
    if files is not None:
        it = get_it(files)
        if [*set(it)] != list(range(min(it), max(it) + 1)):
            print("WARNING: There are missing ANI files!")
        with open(
            f"{settings.get_cwd()}{os.sep}{label}-merged.ANI",
            "w",
            encoding="utf-8"
            ) as outfile:
            print(f"{settings.get_cwd()}{os.sep}{label}-merged.ANI is opened")
            for f in files:
                with open(f, encoding="utf-8") as infile:
                    print(f"Writing {f}")
                    content = infile.read()
                    outfile.write(content)
                    infile.close()
            outfile.close()
        print("All ANI files are merged")
    else:
        print("No ANI files found")


def run(label):
    """Execute"""
    os.chdir(settings.get_cwd())
    folders = glob.glob(f"i*{os.sep}")
    logs = glob.glob(f"i*{os.sep}{settings.get_log()}")
    folders += glob.glob(f"i*{os.sep}{settings.get_cont()}*")
    logs += glob.glob(f"i*{os.sep}{settings.get_cont()}*{os.sep}{settings.get_log()}")
    folders = sort_(folders, "i*", settings.get_cont())
    logs = sort_(logs, "i*", settings.get_cont())
    if not logs:
        run_next("1", label)
    else:
        with open(logs[-1], "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(f"{logs[-1]}: Job completed")
                if len(folders) != len(logs) and not os.path.isfile(
                        f"{settings.get_cwd()}" +
                        f"{os.sep}i{str(int(logs[-1].split(os.sep)[0].strip('i')) + 1)}" +
                        f"{os.sep}{label}.fdf"
                ):
                    if settings.get_cont() in logs[-1]:
                        match = re.search(
                            f"i([0-9]+){os.sep}{settings.get_cont()}(_*[0-9]*)",
                            logs[-1]
                            )
                        ani_to_fdf(
                            f"i{match[1]}{os.sep}{settings.get_cont()}{match[2]}" +
                            f"{os.sep}{label}.ANI",
                            f"i{match[1]}{os.sep}{settings.get_cont()}{match[2]}" +
                            f"{os.sep}{label}.fdf",
                            f"i{int(match[1]) + 1}{os.sep}{label}.fdf"
                        )
                    else:
                        ani_to_fdf(
                            logs[-1].rsplit(os.sep)[0] + os.sep + label + ".ANI",
                            logs[-1].rsplit(os.sep)[0] + os.sep + label + ".fdf",
                            "i" +
                            str(int(logs[-1].split(os.sep)[0].strip("i")) + 1) +
                            os.sep +
                            label +
                            ".fdf"
                        )
                file.close()
                if len(folders) > len(logs):
                    run_next(str(int(logs[-1].split(os.sep)[0].strip("i")) + 1), label)
            elif not run_interrupted(str(int(logs[-1].split(os.sep)[0].strip("i"))), label):
                run_next(str(int(logs[-1].split(os.sep)[0].strip("i")) + 1), label)
    print("All iterations are completed")
    if settings.get_conda():
        sprun(
            [f"{os.sep}usr{os.sep}bin{os.sep}conda", "deactivate"] if os.name == "posix"
            else [f"C:{os.sep}{os.sep}Anaconda3{os.sep}Scripts{os.sep}deactivate"],
            check=True,
            shell=False
        )


def run_interrupted(i, label):
    """Continue to an interrupted calculation"""
    folders = glob.glob(f"i{i}{os.sep}{settings.get_cont()}*")
    folders = sort_(folders, "i*", settings.get_cont())
    if folders:
        with open(f"{folders[-1]}{os.sep}{settings.get_log()}", encoding="utf-8") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(
                    f"i{i}{os.sep}{settings.get_cont()}{os.sep}{settings.get_log()}: Job completed"
                    )
                return False
            match = re.search(f"i[0-9]+{os.sep}{settings.get_cont()}_*[0-9]*", folders[-1])
            if match[0].endswith(settings.get_cont()):
                _cont_step(f"{settings.get_cont()}_2", i, label)
                return True
            contnum = re.search(f"{os.sep}{settings.get_cont()}_([0-9]+)", match[0])[1]
            _cont_step(f"{settings.get_cont()}_{int(contnum) + 1}", i, label)
    _cont_step(settings.get_cont(), i, label)
    return True


def single_run_interrupted(i, label):
    """Continue to an interrupted calculation without continuing next step"""
    folders = glob.glob(f"i*{os.sep}{settings.get_cont()}*")
    folders = sort_(folders, "i*", settings.get_cont())
    if folders:
        with open(f"{folders[-1]}{os.sep}{settings.get_log()}", encoding="utf-8") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(
                    f"i{i}{os.sep}{settings.get_cont()}{os.sep}{settings.get_log()}: Job completed"
                    )
                return False
            match = re.search(f"i[0-9]+{os.sep}{settings.get_cont()}_*[0-9]*", folders[-1])
            if match[0].endswith(settings.get_cont()):
                _cont_step(f"{settings.get_cont()}_2", i, label, issingle=True)
                return True
            contnum = re.search(f"{os.sep}{settings.get_cont()}_([0-9]+)", match[0])[1]
            _cont_step(f"{settings.get_cont()}_{int(contnum) + 1}", i, label, issingle=True)
    _cont_step(settings.get_cont(), i, label, issingle=True)
    return True


def make_directories(n):
    """Create given number of i* folders"""
    for i in range(1, n + 1):
        if not os.path.exists(f"{settings.get_cwd()}{os.sep}i{i}"):
            print(f"Making directory i{i} under {settings.get_cwd().split(os.sep)[-1]}")
            os.mkdir(f"{settings.get_cwd()}{os.sep}i{i}")
        else:
            print(f"Directory i{i} exists")


def copy_files(extensions, label, source_, destination):
    """Copy and paste files"""
    if extensions is not None:
        for ext in extensions:
            if ext == "psf":
                files = glob.glob(f"{source_}{os.sep}*.psf")
                for f in files:
                    file = f.split(os.sep)[-1]
                    copy_file(f, f"{destination}{os.sep}{file}")
            elif ext == "ion":
                files = glob.glob(f"{source_}{os.sep}*.ion")
                for f in files:
                    file = f.split(os.sep)[-1]
                    copy_file(f, f"{destination}{os.sep}{file}")
            else:
                copy_file(
                    f"{source_}{os.sep}{label}.{ext}",
                    f"{destination}{os.sep}{label}.{ext}"
                )
    for cf in settings.contfiles:
        copy_file(f"{source_}{os.sep}{cf}", f"{destination}{os.sep}{cf}")


def analysis(path=None, plot_=True, print_=True):
    """Plot and return energies from log files"""
    if path is None:
        path = "i*"
    files = glob.glob(f"{settings.get_cwd()}{os.sep}{path}{os.sep}{settings.get_log()}")
    files += glob.glob(
        f"{settings.get_cwd()}{os.sep}{path}{os.sep}{settings.get_cont()}*" +
        f"{os.sep}{settings.get_log()}"
        )
    files = sort_(files, path, settings.get_cont())
    energies = []
    it = []
    remove_nones(files, path, settings.get_cwd(), settings.get_cont(), settings.get_log())
    read_energy(energies=energies, files=files, it=it, print_=print_)
    if sorted(it) != list(range(min(it), max(it) + 1)) or None in energies:
        print("WARNING: There are missing values!")
    if None in energies:
        print("WARNING: There are missing energy values!")
    if plot_:
        plt.scatter(it, energies)
        plt.xlabel("Step")
        plt.ylabel("Energy (eV)")
        plt.show()
    return list(zip_longest(it, energies))


def energy_diff(path=None):
    """Return energy differences between minima and maxima"""
    if path is None:
        path = "i*"
    data = analysis(path=path, plot_=False, print_=False)
    energies = np.array([_[1] for _ in data])
    it = np.array([_[0] for _ in data])
    min_idx = np.where(energies == np.amin(energies)) \
        if len(argrelmin(energies)) == 1 else argrelmin(energies)
    print(f"Minima: {energies[min_idx]}")
    max_idx = np.where(energies == np.amax(energies)) \
        if len(argrelmax(energies)) == 1 else argrelmax(energies)
    print(f"Maxima: {energies[max_idx]}")
    diff = np.absolute(energies[min_idx] - energies[max_idx])
    print(f"Energy difference: {diff}")
    return list(zip_longest(energies[min_idx], energies[max_idx], it[min_idx], it[max_idx], diff))


def _command(label=None, issingle=False):
    """SIESTA's run command"""
    if settings.get_conda():
        sprun(
            [f"{os.sep}usr{os.sep}bin{os.sep}conda", "activate", settings.get_conda()]
            if os.name == "posix"
            else
            [f"C:{os.sep}{os.sep}Anaconda3{os.sep}Scripts{os.sep}activate", settings.get_conda()],
            check=True,
            shell=False
        )
    with open(settings.get_log(), "w", encoding="utf-8") as logger:
        with Popen(
            shlex.split(
                f"mpirun -np {settings.get_cores()} " if settings.get_cores() is not None else "" +
                f"{settings.get_siesta()} {label}.fdf"
            ),
            shell=False,
            stdout=logger
        ) as job:
            print(f"PID is {job.pid}")
            for line in tail("-f", settings.get_log(), _iter=True):
                print(line)
                if line == "Job completed\n" and issingle is False:
                    run(label)


def _cont_step(contfolder, i, label, issingle=False):
    print(f"Making directory '{contfolder}' under i{i}")
    os.mkdir(f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}")
    contnummatch = re.search(f"{settings.get_cont()}_([0-9]+)", contfolder)
    contnum = contnummatch[1] if contnummatch is not None else "-1"
    if int(contnum) == 2:
        copy_files(
            settings.contextensions,
            label,
            f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{settings.get_cont()}",
            f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}"
        )
    elif int(contnum) > 2:
        copy_files(
            settings.contextensions,
            label,
            f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{settings.get_cont()}_{int(contnum) - 1}",
            f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}"
        )
    elif contnummatch is None:
        copy_files(
            settings.contextensions,
            label,
            f"{settings.get_cwd()}{os.sep}i{i}",
            f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}"
        )
    os.chdir(f"{settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}")
    print(f"Changed directory to {os.getcwd()}")
    print(f"Opening {settings.get_cwd()}{os.sep}i{i}{os.sep}{contfolder}{os.sep}{label}.fdf")
    with open(f"{label}.fdf", "r+", encoding="utf-8") as fdffile:
        check_restart(
            fdffile=fdffile,
            i=i,
            label=label,
            cwd=settings.get_cwd(),
            cont=contfolder,
            contextensions=settings.contextensions
        )
        fdffile.close()
    print_run(f"i{i}{os.sep}{contfolder}", settings.get_cores(), settings.get_conda())
    _command(label=label, issingle=issingle)
