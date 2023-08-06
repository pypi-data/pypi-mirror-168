from os import makedirs
from os.path import exists, join as join_path
from typing import List, NamedTuple, Optional
import numpy as np
from ase import Atoms
from .io import write_nepfile, write_structures


def setup_training(parameters: NamedTuple,
                   structures: List[Atoms],
                   enforced_structures: List[int] = [],
                   rootdir: str = '.',
                   n_splits: int = None,
                   train_fraction: float = 0.9,
                   seed: int = 42,
                   overwrite: bool = False,
                   ) -> None:
    """Sets up the input files for training a NEP via the ``nep``
    executable of the GPUMD package.

    Parameters
    ----------
    parameters
        dictionary containing the parameters to be set in the nep.in file;
        see [here](https://gpumd.zheyongfan.org/index.php/The_nep.in_input_file)
        for an overview of these parameters
    structures
        list of structures to be included
    enforced_structures
        structures that _must_ be included in the training set, provided in the form
        of a list of indices that refer to the content of the ``structures`` parameter
    rootdir
        root directory in which to create the input files
    n_splits
        number of splits of the input structures in training and test sets that ought to be
        performed; by default no split will be done and all input structures will be used
        for training
    train_fraction
        fraction of structures to be used for training
    seed
        random number generator seed to be used; this ensures reproducability
    overwrite
        if True overwrite the content of ``rootdir`` if it exists
    """
    if exists(rootdir) and not overwrite:
        print('Output directory exists. Set overwrite=True in order to override this behavior.')
        return

    if n_splits is not None and (n_splits <= 0 or n_splits > 0.1 * len(structures)):
        raise ValueError(f'n_splits ({n_splits}) must be positive and'
                         f' must not exceed {0.1*len(structures)}.')

    if train_fraction <= 0 or train_fraction > 1:
        raise ValueError(f'train_fraction ({train_fraction}) must fall in the interval (0,1].')

    rs = np.random.RandomState(seed)
    _prepare_training(parameters, structures, enforced_structures,
                      rootdir, n_splits, train_fraction, rs)


def _prepare_training(parameters: NamedTuple,
                      structures: List[Atoms],
                      enforced_structures: List[int],
                      rootdir: str,
                      n_splits: Optional[int],
                      train_fraction: Optional[float],
                      rs: np.random.RandomState) -> None:
    """Prepares training and test sets and writes structural data as well as parameters files.

    See class-level docstring for documentation of parameters.
    """
    subdir = 'nepmodel_full'
    dirname = join_path(rootdir, subdir)
    makedirs(dirname, exist_ok=True)
    _write_structures(structures, dirname, list(set(range(len(structures)))), [0])
    write_nepfile(parameters, dirname)

    if n_splits is None:
        return

    for k in range(n_splits):
        # fill up training set while reserving space for enforced structures
        n_structures = len(structures)
        remaining_structures = list(set(range(n_structures)) - set(enforced_structures))
        train_selection = rs.choice(
            remaining_structures,
            size=int(train_fraction * n_structures) - len(enforced_structures),
            replace=False)

        # append enforced structures at the end of the training set
        train_selection = list(train_selection)
        train_selection.extend(enforced_structures)

        # add the remaining structures to the test set
        test_selection = list(set(range(n_structures)) - set(train_selection))

        subdir = f'nepmodel_split{k+1}'
        dirname = join_path(rootdir, subdir)
        makedirs(dirname, exist_ok=True)
        _write_structures(structures, dirname, train_selection, test_selection)
        write_nepfile(parameters, dirname)


def _write_structures(structures: List[Atoms],
                      dirname: str,
                      train_selection: List[int],
                      test_selection: List[int]):
    """Writes structures in format readable by nep executable.

    See class-level docstring for documentation of parameters.
    """
    write_structures(
        join_path(dirname, 'train.in'),
        [s for k, s in enumerate(structures) if k in train_selection])
    write_structures(
        join_path(dirname, 'test.in'),
        [s for k, s in enumerate(structures) if k in test_selection])
    with open(join_path(dirname, 'structures.txt'), 'w') as f:
        for k, structure in enumerate(structures):
            line = [f'{k:5}']
            line += [f'{len(structure):5}']
            line += [f' {structure.get_potential_energy():16.8f}']
            line += [f' {np.max(np.linalg.norm(structure.get_forces(), axis=1)):9.4f}']
            if k in train_selection:
                line += ['train']
            else:
                line += ['test']
            if hasattr(structure, 'name'):
                line += [structure.name]
            line += ['\n']
            f.write(' '.join(line))
