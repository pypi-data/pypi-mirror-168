"""
SIESTAstepper terminal client
"""
from __future__ import absolute_import
import sys
from .core import (
    run,
    single_run,
    run_next,
    run_interrupted,
    single_run_interrupted,
    make_directories,
    copy_files,
    ani_to_fdf,
    xyz_to_fdf,
    merge_ani,
    analysis,
    energy_diff,
    settings
)


def main(*, args):
    """Main function"""
    function = args[1]
    for arg in args:
        independents(arg)
    if function not in ["run", "single_run", "run_next", "run_interrupted",
                        "single_run_interrupted", "make_directories",
                        "copy_files", "ani_to_fdf", "xyz_to_fdf", "merge_ani",
                        "analysis", "energy_diff"]:
        raise AttributeError(
            """Command not found. Please use 'run', 'single_run', 'run_next', 'run_interrupted',
            'single_run_interrupted', 'make_directories', 'copy_files', 'ani_to_fdf', 'xyz_to_fdf',
            'merge_ani', 'analysis', 'energy_diff'""".replace("\n", " ")
        )
    if function == "run":
        settings.set_log(args[2])
        run(args[3])
    elif function == "single_run":
        settings.set_log(args[2])
        single_run(args[3], args[4])
    elif function == "run_next":
        settings.set_log(args[2])
        run_next(args[3], args[4])
    elif function == "run_interrupted":
        settings.set_log(args[2])
        run_interrupted(args[3], args[4])
    elif function == "single_run_interrupted":
        settings.set_log(args[2])
        single_run_interrupted(args[3], args[4])
    elif function == "make_directories":
        make_directories(int(args[2]))
    elif function == "copy_files":
        copy_files(
            [_ for _ in args[5:] if not _.startswith("contfiles=")],
            args[2],
            args[3],
            args[4]
        )
    elif function == "ani_to_fdf":
        ani_to_fdf(args[2], args[3], args[4])
    elif function == "xyz_to_fdf":
        xyz_to_fdf(args[2], args[3], args[4])
    elif function == "merge_ani":
        path = "i*"
        if len(args) == 3:
            merge_ani(label=args[2])
        elif len(args) > 3:
            for arg in args[3:]:
                if arg.startswith("path="):
                    path = arg.split("=")[1]
            merge_ani(label=args[2], path=path)
    elif function == "analysis":
        settings.set_log(args[2])
        plot_ = True
        path = "i*"
        if len(args) > 4:
            for arg in args[3:]:
                if arg.startswith("path="):
                    path = arg.split("=")[1]
                if arg == "noplot":
                    plot_ = False
            analysis(path=path, plot_=plot_)
        else:
            analysis()
    elif function == "energy_diff":
        settings.set_log(args[2])
        path = "i*"
        if len(args) > 4:
            for arg in args[3:]:
                if arg.startswith("path="):
                    path = arg.split("=")[1]
            energy_diff(path=path)
        else:
            energy_diff()


def independents(arg):
    """Sets independent variables"""
    if arg.startswith("mpirun="):
        settings.set_cores(int(arg.split("=")[1]))
    if arg.startswith("conda="):
        settings.set_conda(arg.split("=")[1])
    if arg.startswith("cont="):
        settings.set_cont(arg.split("=")[1])
    if arg.startswith("contfiles="):
        settings.contfiles.extend(arg.split("=")[1].split(","))
    if arg.startswith("contextensions="):
        settings.contextensions.extend(arg.split("=")[1].split(","))
    if arg.startswith("siesta="):
        settings.set_siesta(arg.split("=")[1])


main(args=sys.argv)
