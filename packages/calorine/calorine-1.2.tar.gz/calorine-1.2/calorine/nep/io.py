from typing import Any, Dict, Iterable, List, NamedTuple, TextIO, Tuple
from os.path import exists, join as join_path
import numpy as np
from ase import Atoms
from pandas import DataFrame


def read_loss(filename: str) -> DataFrame:
    """Parses a file in ``loss.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found at
    https://gpumd.zheyongfan.org/index.php/The_output_files_for_the_nep_executable#The_loss.out_file.

    Parameters
    ----------
    filename
        input file name

    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in loss.out, append a dimension
        data = data.reshape(1, -1)
    if len(data[0]) != 10:
        raise ValueError(f'Input file contains {len(data[0])} data columns.'
                         f' Expected 10 columns.')
    tags = 'total_loss L1 L2'
    tags += ' RMSE_E_train RMSE_F_train RMSE_V_train'
    tags += ' RMSE_E_test RMSE_F_test RMSE_V_test'
    generations = range(100, len(data) * 100 + 1, 100)
    df = DataFrame(data=data[:, 1:], columns=tags.split(), index=generations)
    return df


def read_potential(filename: str) -> Tuple[Dict[str, tuple], List[float]]:
    """Parses a file in ``nep.txt`` format from GPUMD and returns the
    content as a tuple of a dict and a list. The dict contains the
    information contained in the header, whereas the list contains the
    weights and rescaling factors.

    Parameters
    ----------
    filename
        input file name

    """
    header = []
    parameters = []
    nheader = 6
    with open(filename) as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            if len(flds) == 0:
                continue
            if k == 0 and 'zbl' in flds[0]:
                nheader += 1
            if k <= nheader:
                header.append(tuple(flds))
            elif len(flds) == 1:
                parameters.append(float(flds[0]))
            else:
                raise IOError(f'Failed to parse line {k} from {filename}')
    settings = {}
    for flds in header:
        if flds[0] in ['cutoff']:
            settings[flds[0]] = tuple(map(float, flds[1:]))
        elif flds[0] in ['zbl', 'n_max', 'l_max', 'ANN', 'basis_size']:
            settings[flds[0]] = tuple(map(int, flds[1:]))
        else:
            settings[flds[0]] = flds[1:]
    return settings, parameters


def _write_structure_in_nep_format(structure: Atoms,
                                   f: TextIO) -> None:
    """Write structure block into a file-like object in format readable by nep executable.

    Parameters
    ----------
    structure
        input structure; must hold information regarding energy and forces
    f
        file-like object to which to write
    """

    try:
        energy = structure.get_potential_energy()
        forces = structure.get_forces()
    except RuntimeError:
        raise Exception('Failed to retrieve energy and/or forces for structure')
    try:
        stress = structure.get_stress()
        virials = -stress * structure.get_volume()  # --> eV
    except RuntimeError:
        print('Warning: Failed to retrieve stresses for structure')
        virials = None

    f.write(f'{energy} ')
    if virials is not None:
        f.write(' '.join([f'{virials[i]:.8f}' for i in [0, 1, 2, 3, 4, 5]]))
    f.write('\n')
    for row in structure.cell:
        for val in row:
            f.write(f'  {val:.8f}')
    f.write('\n')
    for symbol, position, force in zip(structure.symbols, structure.positions, forces):
        f.write(f'{symbol:2}  ')
        f.write(' '.join([f'{pi:14.8f}' for pi in position]))
        f.write('  ')
        f.write(' '.join([f'{fi:14.8f}' for fi in force]))
        f.write('\n')


def write_structures(outfile: str,
                     structures: List[Atoms]) -> None:
    """Writes structures for training/testing in format readable by nep executable.

    Parameters
    ----------
    outfile
        output filename
    structures
        list of structures with energy, forces, and stresses
    """
    with open(outfile, 'w') as f:
        f.write(f'{len(structures)}\n')
        for structure in structures:
            try:
                _ = structure.get_stress()
                has_virial = 1
            except RuntimeError:
                has_virial = 0
            f.write(f'{len(structure)} {has_virial}\n')
        for structure in structures:
            _write_structure_in_nep_format(structure, f)


def write_nepfile(parameters: NamedTuple,
                  dirname: str) -> None:
    """Writes parameters file for NEP construction.

    Parameters
    ----------
    parameters
        input parameters; see https://gpumd.zheyongfan.org/index.php/The_nep.in_input_file
    dirname
        directory in which to place input file and links
    """
    with open(join_path(dirname, 'nep.in'), 'w') as f:
        for key, val in parameters.items():
            f.write(f'{key}  ')
            if isinstance(val, Iterable):
                f.write(' '.join([f'{v}' for v in val]))
            else:
                f.write(f'{val}')
            f.write('\n')


def read_nepfile(filename: str) -> Dict[str, Any]:
    """Returns the content of a configuration file (`nep.in`) as a dictionary.

    Parameters
    ----------
    filename
        input file name
    """
    settings = {}
    with open(filename) as f:
        for line in f.readlines():
            flds = line.split()
            if len(flds) == 0:
                continue
            if flds[0].startswith('#'):
                continue
            settings[flds[0]] = ' '.join(flds[1:])
    return settings


def read_structures(dirname: str) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    """Parses the energy_*.out, force_*.out, and virial_*.out files from a
    nep run and returns their content as dictionaries.  The first and
    second dictionary contain the structures from the training and
    test sets, respectively.  Each dictionary entry correspond
    corresponds to a structure and contains itself a dict that holds
    the structure specific information, such as target and predicted
    energies, forces, and virials.

    Parameters
    ----------
    dirname
        directory from which to read output files
    """
    path = join_path(dirname)
    if not exists(path):
        raise ValueError(f'Directory {path} does not exist')

    structures = _read_structures_file(path)

    for stype in ['train', 'test']:
        n_atoms = _read_natoms_from_input_file(path, f'{stype}.in')
        n_structures = len(n_atoms)
        if len(structures[stype]) > 0:
            assert len(structures[stype]) == n_structures, \
                f'Number of structures in structures.txt ({len(structures[stype])})' \
                f' and {stype}.in ({n_structures}) inconsistent'
        if len(structures[stype]) == 0:
            structures[stype] = {k: dict() for k in range(n_structures)}
        for k, nat in zip(structures[stype], n_atoms):
            structures[stype][k]['natoms'] = nat

        ts, ps = _read_data_file(path, f'energy_{stype}.out')
        assert len(ts) == n_structures, \
            f'Number of structures in energy_{stype}.out ({len(ts)})' \
            f' and {stype}.in ({n_structures}) inconsistent'
        for k, (t, p) in enumerate(zip(ts, ps)):
            structures[stype][k]['energy_target'] = t
            structures[stype][k]['energy_predicted'] = p

        ts, ps = _read_data_file(path, f'force_{stype}.out')
        assert len(ts) == sum(n_atoms), \
            f'Number of structures in force_{stype}.out ({len(ts)})' \
            f' and {stype}.in ({n_structures}) inconsistent'
        n = 0
        for k, nat in enumerate(n_atoms):
            structures[stype][k]['force_target'] = np.array(ts[n:n+nat]).reshape(nat, 3)
            structures[stype][k]['force_predicted'] = np.array(ps[n:n+nat]).reshape(nat, 3)
            n += nat

        ts, ps = _read_data_file(path, f'virial_{stype}.out')
        assert len(ts) == 6 * n_structures, \
            f'Number of structures in virial_{stype}.out ({len(ts)})' \
            f' and {stype}.in ({n_structures}) inconsistent'
        ts = np.array(ts).reshape((6, n_structures)).T
        ps = np.array(ps).reshape((6, n_structures)).T
        for k, (t, p) in enumerate(zip(ts, ps)):
            assert np.shape(t) == (6,)
            structures[stype][k]['virial_target'] = t
            structures[stype][k]['virial_predicted'] = p

    return structures['train'], structures['test']


def _read_natoms_from_input_file(dirname: str,
                                 fname: str):
    """Private function that parses a train.in/test.in file and returns
    the number of atoms for each structure.
    """
    path = join_path(dirname, fname)
    if not exists(path):
        raise ValueError(f'Directory {path} does not exist')
    with open(path, 'r') as f:
        lines = f.readlines()
    n_structures = int(lines[0])
    n_atoms = [int(s.split()[0]) for s in lines[1:n_structures + 1]]
    return n_atoms


def _read_data_file(dirname: str,
                    fname: str):
    """Private function that parses energy/force/virial_*.out files and
    returns their content for further processing.
    """
    path = join_path(dirname, fname)
    if not exists(path):
        raise ValueError(f'Directory {path} does not exist')
    with open(path, 'r') as f:
        lines = f.readlines()
    target, predicted = [], []
    for line in lines:
        flds = line.split()
        if len(flds) == 6:
            predicted.append([float(s) for s in flds[0:3]])
            target.append([float(s) for s in flds[3:6]])
        elif len(flds) == 2:
            predicted.append(float(flds[0]))
            target.append(float(flds[1]))
    return target, predicted


def _read_structures_file(dirname: str):
    """Private function that parses a structures.txt file and returns the
    content for further processing.
    """
    structures = {}
    structures['train'] = {}
    structures['test'] = {}
    path = join_path(dirname, 'structures.txt')
    if exists(path):
        with open(path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            flds = line.split()
            index = int(flds[0])
            stype = flds[4]
            if index in structures[stype]:
                print(f'Warning: Structure {index} appears multiple times ({stype});'
                      ' keeping only first occurence')
                continue
            record = dict()
            if len(flds) > 5:
                record['name'] = flds[5]
            structures[stype][index] = record
    return structures
