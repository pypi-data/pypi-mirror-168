from typing import Any, Dict, List, Tuple

import numpy as np
from ase import Atoms
from ase.neighborlist import NeighborList
from pandas import DataFrame


def read_runfile(filename: str) -> Dict[str, Any]:
    """Returns the content of a configuration file (`run.in`) as a dictionary.

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
            if flds[0] == 'compute_hnemd':
                settings['dump_hnemd'] = int(flds[1])
                settings['Fe_x'] = float(flds[2])
                settings['Fe_y'] = float(flds[3])
                settings['Fe_z'] = float(flds[4])
            elif flds[0] == 'compute_hac':
                settings['sampling_interval'] = int(flds[1])
                settings['correlation_steps'] = int(flds[2])
                settings['output_interval'] = int(flds[3])
            elif flds[0] == 'ensemble':
                settings['ensemble'] = flds[1]
                if settings['ensemble'].startswith('nvt'):
                    settings['temperature'] = float(flds[2])
                    settings['temperature_final'] = float(flds[3])
                    settings['thermostat_coupling'] = float(flds[4])
                elif settings['ensemble'].startswith('npt'):
                    settings['temperature'] = float(flds[2])
                    settings['temperature_final'] = float(flds[3])
                    settings['thermostat_coupling'] = float(flds[4])
                    settings['pressure_x'] = float(flds[5])
                    settings['pressure_y'] = float(flds[6])
                    settings['pressure_z'] = float(flds[7])
                    settings['pressure_coupling'] = float(flds[8])
                elif settings['ensemble'].startswith('heat'):
                    settings['temperature'] = float(flds[2])
                    settings['thermostat_coupling'] = float(flds[3])
                    settings['delta_temperature'] = float(flds[4])
                    settings['label_source'] = flds[5]
                    settings['label_sink'] = flds[6]
                else:
                    raise ValueError(f'Run.in contains invalid ensemble {settings["ensemble"]}.'
                                     f' Expected nvt, npt or heat.')
            elif flds[0] == 'time_step':
                settings['time_step'] = float(flds[1])
            elif flds[0] == 'dump_thermo':
                settings['dump_thermo'] = int(flds[1])
            elif flds[0] == 'neighbor':
                settings['neighbor'] = int(flds[1])
            elif flds[0] == 'dump_position':
                settings['dump_position'] = int(flds[1])
            elif flds[0] == 'velocity':
                settings['velocity'] = float(flds[1])
            elif flds[0] == 'run':
                settings['run'] = int(flds[1])
            elif flds[0] == 'potential':
                settings[flds[0]] = ' '.join(flds[1:])
                potential_filename = flds[1]
                if 'fcp.txt' in potential_filename:
                    try:
                        with open(potential_filename, 'r') as f:
                            settings['fcp_order'] = int(f.readlines()[1].split()[0])
                    except IOError as e:
                        raise IOError(
                            f'Failed to read fcp potential in file {potential_filename}') from e
            else:
                settings[flds[0]] = ' '.join(flds[1:])
    return settings


def read_kappa(filename: str) -> DataFrame:
    """Parses a file in ``kappa.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found at
    https://gpumd.zheyongfan.org/index.php/The_kappa.out_output_file.

    Parameters
    ----------
    filename
        input file name

    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in kappa.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'kx_in kx_out ky_in ky_out kz_tot'.split()
    if len(data[0]) != len(tags):
        raise ValueError(f'Input file contains {len(data[0])} data columns.'
                         f' Expected {len(tags)} columns.')
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    return df


def read_hac(filename: str) -> DataFrame:
    """Parses a file in ``hac.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found at
    https://gpumd.zheyongfan.org/index.php/The_hac.out_output_file.

    Parameters
    ----------
    filename
        input file name

    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in hac.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'time'
    tags += ' jin_jtot_x jout_jtot_x jin_jtot_y jout_jtot_y jtot_jtot_z'
    tags += ' kx_in kx_out ky_in ky_out kz_tot'
    tags = tags.split()
    if len(data[0]) != len(tags):
        raise ValueError(f'Input file contains {len(data[0])} data columns.'
                         f' Expected {len(tags)} columns.')
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    # remove columns with less relevant data to save space
    for col in df:
        if 'jtot' in col or '_in' in col:
            del df[col]
    return df


def read_thermo(filename: str,
                natoms: int = 1) -> DataFrame:
    """Parses a file in ``thermo.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found at
    https://gpumd.zheyongfan.org/index.php/The_thermo.out_output_file.

    Parameters
    ----------
    filename
        input file name
    natoms
        number of atoms; used to normalize energies

    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in loss.out, append a dimension
        data = data.reshape(1, -1)
    if len(data[0]) == 9:
        # orthorhombic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 12:
        # orthorhombic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 15:
        # triclinic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
    elif len(data[0]) == 18:
        # triclinic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
    else:
        raise ValueError(f'Input file contains {len(data[0])} data columns.'
                         ' Expected 9, 12, 15 or 18 columns.')
    df = DataFrame(data=data, columns=tags.split())
    assert natoms > 0, 'natoms must be positive'
    df.kinetic_energy /= natoms
    df.potential_energy /= natoms
    return df


def read_xyz(filename: str) -> Tuple[Atoms, Dict[str, int]]:
    """
    Read the structure input file (`xyz.in`) for GPUMD and return the
    structure along with run input parameters from the file.

    Parameters
    ----------
    filename
        Name of file from which to read the structure

    Returns
    -------
    tuple comprising the structure and the parameters from the first row of the file
    """

    with open(filename, 'r') as fd:

        # Parse first line
        first_line = next(fd)
        input_parameters = {}
        keys = ['number_of_atoms', 'maximum_neighbors', 'cutoff',
                'use_triclinic', 'has_velocity', 'number_of_groups']
        types = [float if key == 'cutoff' else int for key in keys]
        for k, (key, typ) in enumerate(zip(keys, types)):
            input_parameters[key] = typ(first_line.split()[k])

        # Parse second line
        second_line = next(fd)
        second_arr = np.array(second_line.split())
        pbc = second_arr[:3].astype(bool)
        if input_parameters['use_triclinic']:
            cell = second_arr[3:].astype(float).reshape((3, 3))
        else:
            cell = np.diag(second_arr[3:].astype(float))

        # Parse all remaining rows
        n_rows = input_parameters['number_of_atoms']
        n_columns = 5 + input_parameters['has_velocity'] * 3
        n_columns += input_parameters['number_of_groups']
        rest_lines = [next(fd) for _ in range(n_rows)]
        rest_arr = np.array([line.split() for line in rest_lines])
        assert rest_arr.shape == (n_rows, n_columns)

    # Extract atom types, positions and masses
    symbols = rest_arr[:, 0].astype('str')
    positions = rest_arr[:, 1:4].astype(float)

    # Create the Atoms object
    structure = Atoms(symbols=symbols, positions=positions, pbc=pbc, cell=cell)
    if input_parameters['has_velocity']:
        velocities = rest_arr[:, 5:8].astype(float)
        structure.set_velocities(velocities)
    if input_parameters['number_of_groups']:
        start_col = 5 + 3 * input_parameters['has_velocity']
        groups = rest_arr[:, start_col:].astype(int)
        structure.info = {i: {'groups': groups[i, :]} for i in range(n_rows)}

    return structure, input_parameters


def write_xyz(filename: str,
              structure: Atoms,
              maximum_neighbors: int = None,
              cutoff: float = None,
              groupings: List[List[List[int]]] = None,
              use_triclinic: bool = False):
    """
    Writes a structure into GPUMD input format (`xyz.in`).

    Parameters
    ----------
    filename
        Name of file to which the structure should be written
    structure
        Input structure
    maximum_neighbors
        Maximum number of neighbors any atom can ever have (not relevant when
        using force constant potentials)
    cutoff
        Initial cutoff distance used for building the neighbor list (not
        relevant when using force constant potentials)
    groupings
        Groups into which the individual atoms should be divided in the form of
        a list of list of lists. Specifically, the outer list corresponds to
        the grouping methods, of which there can be three at the most, which
        contains a list of groups in the form of lists of site indices. The
        sum of the lengths of the latter must be the same as the total number
        of atoms.
    use_triclinic
        Use format for triclinic cells

    Raises
    ------
    ValueError
        Raised if parameters are incompatible
    """

    # Check velocties parameter
    velocities = structure.get_velocities()
    if velocities is None or np.max(np.abs(velocities)) < 1e-6:
        has_velocity = 0
    else:
        has_velocity = 1

    # Check groupings parameter
    if groupings is None:
        number_of_grouping_methods = 0
    else:
        number_of_grouping_methods = len(groupings)
        if number_of_grouping_methods > 3:
            raise ValueError('There can be no more than 3 grouping methods!')
        for g, grouping in enumerate(groupings):
            all_indices = [i for group in grouping for i in group]
            if len(all_indices) != len(structure) or \
                    set(all_indices) != set(range(len(structure))):
                raise ValueError(f'The indices listed in grouping method {g} are'
                                 ' not compatible with the input'
                                 ' structure!')

    # If not specified, estimate the maximum_neighbors
    if maximum_neighbors is None:
        if cutoff is None:
            cutoff = 0.1
            maximum_neighbors = 1
        else:
            nl = NeighborList([cutoff / 2] * len(structure), skin=2, bothways=True)
            nl.update(structure)
            maximum_neighbors = 0
            for atom in structure:
                maximum_neighbors = max(maximum_neighbors,
                                        len(nl.get_neighbors(atom.index)[0]))
            maximum_neighbors *= 2
            maximum_neighbors = min(maximum_neighbors, 1024)

    # Add header and cell parameters
    lines = []
    if structure.cell.orthorhombic and not use_triclinic:
        triclinic = 0
    else:
        triclinic = 1
    lines.append('{} {} {} {} {} {}'.format(len(structure), maximum_neighbors,
                                            cutoff, triclinic, has_velocity,
                                            number_of_grouping_methods))
    if triclinic:
        lines.append((' {}' * 12)[1:].format(*structure.pbc.astype(int),
                                             *structure.cell[:].flatten()))
    else:
        lines.append((' {}' * 6)[1:].format(*structure.pbc.astype(int),
                                            *structure.cell.lengths()))

    # Add lines for all atoms
    for a, atm in enumerate(structure):
        line = (' {}' * 5)[1:].format(atm.symbol, *atm.position, atm.mass)
        if has_velocity:
            line += (' {}' * 3).format(*velocities[a])
        if groupings is not None:
            for grouping in groupings:
                for i, group in enumerate(grouping):
                    if a in group:
                        line += ' {}'.format(i)
        lines.append(line)

    # Write file
    with open(filename, 'w') as fd:
        fd.write('\n'.join(lines))
