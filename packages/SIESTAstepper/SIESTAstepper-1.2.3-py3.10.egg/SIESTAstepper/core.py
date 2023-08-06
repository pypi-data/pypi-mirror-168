import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelmin, argrelmax
from sh import tail
from subprocess import Popen
from subprocess import run as sprun
import shlex
from itertools import zip_longest
import re
from .helpers import create_fdf, read_fdf, read_energy, get_it, print_run, check_restart, check_userbasis, copy_file, \
    sort_, remove_nones

cwd: str = os.getcwd()
log: str = "log"
cores = None
conda = None
cont: str = "continue"
contfiles: list = []
contextensions: list = ["psf", "fdf"]
siesta: str = "siesta"


def run_next(i, label):
    """Run SIESTA for given step"""
    logs = glob.glob(f"i{int(i) - 1}{os.sep}{log}")
    logs += glob.glob(f"i{int(i) - 1}{os.sep}{cont}*{os.sep}{log}")
    logs = sort_(logs, "i*", cont)
    if len(logs) != 0 and cont in logs[-1]:
        match = re.search(f"i{int(i) - 1}{os.sep}{cont}(_*[0-9]*)", logs[-1])
        if not os.path.isfile(f"{cwd}{os.sep}i{i}{os.sep}{label}.fdf"):
            ani_to_fdf(
                f"i{int(i) - 1}{os.sep}{cont}{match[1]}{os.sep}{label}.ANI",
                f"i{int(i) - 1}{os.sep}{cont}{match[1]}{os.sep}{label}.fdf",
                f"i{i}{os.sep}{label}.fdf"
            )
        copy_files(
            ["ion" if check_userbasis(f"i{i}{os.sep}{label}.fdf") else "psf"],
            label,
            f"{cwd}{os.sep}i{int(i) - 1}{os.sep}{cont}{match[1]}",
            f"{cwd}{os.sep}i{i}"
        )
    elif int(i) > 1:
        if not os.path.isfile(f"{cwd}{os.sep}i{str(int(i) + 1)}{os.sep}{label}.fdf"):
            ani_to_fdf(
                f"i{int(i) - 1}{os.sep}{label}.ANI",
                f"i{int(i) - 1}{os.sep}{label}.fdf",
                f"i{i}{os.sep}{label}.fdf"
            )
        copy_files(
            ["ion" if check_userbasis(f"i{i}{os.sep}{label}.fdf") else "psf"],
            label,
            f"{cwd}{os.sep}i{int(i) - 1}",
            f"{cwd}{os.sep}i{i}"
        )

    os.chdir(f"{cwd}{os.sep}i{i}")
    print(f"Changed directory to {os.getcwd()}")
    print_run(f"i{i}", cores, conda)
    _command(label=label)


def single_run(i, label):
    """Run SIESTA for given step without continuing next step"""
    os.chdir(f"{cwd}{os.sep}i{i}")
    print(f"Changed directory to {os.getcwd()}")
    with open(f"{cwd}{os.sep}i{i}{os.sep}{log}", "r") as file:
        lines = file.readlines()
        if lines[-1] == "Job completed\n":
            print(f"i{i}{os.sep}{log}: Job completed")
        else:
            if int(i) > 1:
                if not os.path.isfile(f"{cwd}{os.sep}i{str(int(i) + 1)}{os.sep}{label}.fdf"):
                    ani_to_fdf(
                        f"{cwd}{os.sep}i{int(i) - 1}{os.sep}{label}.ANI",
                        f"{cwd}{os.sep}i{int(i) - 1}{os.sep}{label}.fdf",
                        f"{cwd}{os.sep}i{i}{os.sep}{label}.fdf"
                    )
                copy_files(
                    ["ion" if check_userbasis(f"{cwd}{os.sep}i{i}{os.sep}{label}.fdf") else "psf"],
                    label,
                    f"{cwd}{os.sep}i{int(i) - 1}",
                    f"{cwd}{os.sep}i{i}"
                )
            print_run(f"i{i}", cores, conda)
            _command(label=label, issingle=True)


def ani_to_fdf(anipath, fdfpath, newfdfpath):
    """Convert last geometry of an ANI to FDF by using the previous FDF and ANI files"""
    print(f"Reading {anipath}")
    with open(anipath, "r") as anifile:
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
    with open(xyzpath, "r") as xyzfile:
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
    files = glob.glob(f"{cwd}{os.sep}{path}{os.sep}{label}.ANI")
    files += glob.glob(f"{cwd}{os.sep}{path}{os.sep}{cont}*{os.sep}{label}.ANI")
    files = sort_(files, path, cont)
    if files is not None:
        it = get_it(files)
        if [*set(it)] != list(range(min(it), max(it) + 1)):
            print("WARNING: There are missing ANI files!")
        with open(f"{cwd}{os.sep}{label}-merged.ANI", "w") as outfile:
            print(f"{cwd}{os.sep}{label}-merged.ANI is opened")
            for f in files:
                with open(f) as infile:
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
    os.chdir(cwd)
    folders = glob.glob(f"i*{os.sep}")
    logs = glob.glob(f"i*{os.sep}{log}")
    folders += glob.glob(f"i*{os.sep}{cont}*")
    logs += glob.glob(f"i*{os.sep}{cont}*{os.sep}{log}")
    folders = sort_(folders, "i*", cont)
    logs = sort_(logs, "i*", cont)
    if len(logs) == 0:
        run_next("1", label)
    else:
        with open(logs[-1], "r") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(f"{logs[-1]}: Job completed")
                if len(folders) != len(logs) and not os.path.isfile(
                        f"{cwd}{os.sep}i{str(int(logs[-1].split(os.sep)[0].strip('i')) + 1)}{os.sep}{label}.fdf"
                ):
                    if cont in logs[-1]:
                        match = re.search(f"i([0-9]+){os.sep}{cont}(_*[0-9]*)", logs[-1])
                        ani_to_fdf(
                            f"i{match[1]}{os.sep}{cont}{match[2]}{os.sep}{label}.ANI",
                            f"i{match[1]}{os.sep}{cont}{match[2]}{os.sep}{label}.fdf",
                            f"i{int(match[1]) + 1}{os.sep}{label}.fdf"
                        )
                    else:
                        ani_to_fdf(
                            logs[-1].rsplit(os.sep)[0] + os.sep + label + ".ANI",
                            logs[-1].rsplit(os.sep)[0] + os.sep + label + ".fdf",
                            "i" + str(int(logs[-1].split(os.sep)[0].strip("i")) + 1) + os.sep + label + ".fdf"
                        )
                file.close()
                if len(folders) > len(logs):
                    run_next(str(int(logs[-1].split(os.sep)[0].strip("i")) + 1), label)
            elif not run_interrupted(str(int(logs[-1].split(os.sep)[0].strip("i"))), label):
                run_next(str(int(logs[-1].split(os.sep)[0].strip("i")) + 1), label)
    print("All iterations are completed")
    if conda:
        sprun(
            [f"{os.sep}usr{os.sep}bin{os.sep}conda", "deactivate"] if os.name == "posix"
            else [f"C:{os.sep}{os.sep}Anaconda3{os.sep}Scripts{os.sep}deactivate"]
        )


def run_interrupted(i, label):
    """Continue to an interrupted calculation"""
    folders = glob.glob(f"i{i}{os.sep}{cont}*")
    folders = sort_(folders, "i*", cont)
    if len(folders) != 0:
        with open(f"{folders[-1]}{os.sep}{log}") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(f"i{i}{os.sep}{cont}{os.sep}{log}: Job completed")
                return False
            match = re.search(f"i[0-9]+{os.sep}{cont}_*[0-9]*", folders[-1])
            if match[0].endswith(cont):
                _cont_step(f"{cont}_2", i, label)
                return True
            contnum = re.search(f"{os.sep}{cont}_([0-9]+)", match[0])[1]
            _cont_step(f"{cont}_{int(contnum) + 1}", i, label)
    _cont_step(cont, i, label)
    return True


def single_run_interrupted(i, label):
    """Continue to an interrupted calculation without continuing next step"""
    folders = glob.glob(f"i*{os.sep}{cont}*")
    folders = sort_(folders, "i*", cont)
    if len(folders) != 0:
        with open(f"{folders[-1]}{os.sep}{log}") as file:
            lines = file.readlines()
            if lines[-1] == "Job completed\n":
                print(f"i{i}{os.sep}{cont}{os.sep}{log}: Job completed")
                return False
            match = re.search(f"i[0-9]+{os.sep}{cont}_*[0-9]*", folders[-1])
            if match[0].endswith(cont):
                _cont_step(f"{cont}_2", i, label, issingle=True)
                return True
            contnum = re.search(f"{os.sep}{cont}_([0-9]+)", match[0])[1]
            _cont_step(f"{cont}_{int(contnum) + 1}", i, label, issingle=True)
    _cont_step(cont, i, label, issingle=True)
    return True


def make_directories(n):
    for i in range(1, n + 1):
        if not os.path.exists(f"{cwd}{os.sep}i{i}"):
            print(f"Making directory i{i} under {cwd.split(os.sep)[-1]}")
            os.mkdir(f"{cwd}{os.sep}i{i}")
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
                copy_file(f"{source_}{os.sep}{label}.{ext}", f"{destination}{os.sep}{label}.{ext}")
    for cf in contfiles:
        copy_file(f"{source_}{os.sep}{cf}", f"{destination}{os.sep}{cf}")


def analysis(path=None, plot_=True, print_=True):
    """Plot and return energies from log files"""
    if path is None:
        path = "i*"
    files = glob.glob(f"{cwd}{os.sep}{path}{os.sep}{log}")
    files += glob.glob(f"{cwd}{os.sep}{path}{os.sep}{cont}*{os.sep}{log}")
    files = sort_(files, path, cont)
    energies = []
    it = []
    remove_nones(files, path, cwd, cont, log)
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
    if path is None:
        path = "i*"
    data = analysis(path=path, plot_=False, print_=False)
    energies = np.array([_[1] for _ in data])
    it = np.array([_[0] for _ in data])
    min_idx = np.where(energies == np.amin(energies)) if len(argrelmin(energies)) == 1 else argrelmin(energies)
    print(f"Minima: {energies[min_idx]}")
    max_idx = np.where(energies == np.amax(energies)) if len(argrelmax(energies)) == 1 else argrelmax(energies)
    print(f"Maxima: {energies[max_idx]}")
    diff = np.absolute(energies[min_idx] - energies[max_idx])
    print(f"Energy difference: {diff}")
    return list(zip_longest(energies[min_idx], energies[max_idx], it[min_idx], it[max_idx], diff))


def _command(label=None, issingle=False):
    """SIESTA's run command"""
    if conda:
        sprun([f"{os.sep}usr{os.sep}bin{os.sep}conda", "activate", conda] if os.name == "posix"
              else [f"C:{os.sep}{os.sep}Anaconda3{os.sep}Scripts{os.sep}activate", conda])
    with open(log, "w") as logger:
        job = Popen(
            shlex.split(f"{f'mpirun -np {cores} ' if cores is not None else ''}{siesta} {label}.fdf"),
            stdout=logger
        )
        print(f"PID is {job.pid}")
        for line in tail("-f", log, _iter=True):
            print(line)
            if line == "Job completed\n" and issingle is False:
                run(label)


def _cont_step(contfolder, i, label, issingle=False):
    print(f"Making directory '{contfolder}' under i{i}")
    os.mkdir(f"{cwd}{os.sep}i{i}{os.sep}{contfolder}")
    contnummatch = re.search(f"{cont}_([0-9]+)", contfolder)
    contnum = contnummatch[1] if contnummatch is not None else "-1"
    if int(contnum) == 2:
        copy_files(contextensions, label, f"{cwd}{os.sep}i{i}{os.sep}{cont}", f"{cwd}{os.sep}i{i}{os.sep}{contfolder}")
    elif int(contnum) > 2:
        copy_files(
            contextensions,
            label,
            f"{cwd}{os.sep}i{i}{os.sep}{cont}_{int(contnum) - 1}",
            f"{cwd}{os.sep}i{i}{os.sep}{contfolder}"
        )
    elif contnummatch is None:
        copy_files(contextensions, label, f"{cwd}{os.sep}i{i}", f"{cwd}{os.sep}i{i}{os.sep}{contfolder}")
    os.chdir(f"{cwd}{os.sep}i{i}{os.sep}{contfolder}")
    print(f"Changed directory to {os.getcwd()}")
    print(f"Opening {cwd}{os.sep}i{i}{os.sep}{contfolder}{os.sep}{label}.fdf")
    with open(f"{label}.fdf", "r+") as fdffile:
        check_restart(fdffile, i, label, cwd, contfolder, contextensions)
        fdffile.close()
    print_run(f"i{i}{os.sep}{contfolder}", cores, conda)
    _command(label=label, issingle=issingle)


def update_cwd(newcwd):
    global cwd
    cwd = newcwd


def update_log(newlog):
    global log
    log = newlog


def update_cores(newcores):
    global cores
    cores = newcores


def update_conda(newconda):
    global conda
    conda = newconda


def update_cont(newcont):
    global cont
    cont = newcont


def update_siesta(newsiesta):
    global siesta
    siesta = newsiesta
