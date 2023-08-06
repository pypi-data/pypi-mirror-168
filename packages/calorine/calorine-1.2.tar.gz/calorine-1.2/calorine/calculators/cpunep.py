import os
import contextlib
from typing import List
import numpy as np
from tempfile import TemporaryFile
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
import _nepy


class CPUNEP(Calculator):
    """This class provides an ASE calculator for `nep_cpu`,
    the in-memory CPU implementation of GPUMD.

    Parameters
    ----------
    potential_filename : str
        Path to nep.txt potential
    atoms : Atoms
        Atoms to attach the calculator to
    label : str
        Label for this calculator
    debug : bool, optional
        Flag to toggle debug mode. Prints GPUMD output. Defaults to False.

    Raises
    ------
    FileNotFoundError
        Raises FileNotFoundError if `potential_filename` does not point to a valid file.
    ValueError
        Raises ValueError atoms are not defined when trying to get energies and forces.
    Example
    -------

    >>> calc = CPUNEP('nep.txt')
    >>> atoms.calc = calc
    >>> atoms.get_potential_energy()
    """

    implemented_properties = ['energy', 'energies', 'forces', 'stress']
    debug = False
    nepy = None

    def __init__(self,
                 potential_filename: str,
                 atoms: Atoms = None,
                 label: str = None,
                 debug: bool = False):

        self.debug = debug
        if not os.path.exists(potential_filename):
            raise FileNotFoundError(f'{potential_filename} does not exist.')
        self.potential_filename = potential_filename

        # Initialize atoms, results and nepy - note that this is also done in Calculator.__init__()
        self.set_atoms(atoms)
        Calculator.__init__(self, label=label, atoms=atoms)
        if atoms is not None:
            self._setup_nepy()

    def _setup_nepy(self):
        """
        Creates an instance of the NEPY class and attaches it to the calculator object.
        The output from `nep.cpp` is only written to STDOUT if debug == True
        """
        if self.atoms is None:
            raise ValueError('Atoms must be defined to get energies and forces.')
        if self.atoms.cell.rank == 0:
            raise ValueError('Atoms must have a defined cell.')

        N_atoms = len(self.atoms)
        self.N_atoms = N_atoms
        c = self.atoms.get_cell(complete=True).flatten()
        cell = [c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]]
        symbols = self.atoms.get_chemical_symbols()
        positions = list(
            self.atoms.get_positions().T.flatten())  # [x1, ..., xN, y1, ... yN,...]

        # Disable output from C++ code by default
        if self.debug:
            self.nepy = _nepy.NEPY(self.potential_filename, self.N_atoms,
                                   cell, symbols, positions)
        else:
            with TemporaryFile('w') as f:
                with contextlib.redirect_stdout(f):
                    self.nepy = _nepy.NEPY(self.potential_filename,
                                           self.N_atoms, cell, symbols, positions)

    def set_atoms(self, atoms: Atoms):
        """Updates the Atoms object.

        Parameters
        ----------
        atoms : Atoms
            Atoms to attach the calculator to
        """
        self.atoms = atoms
        self.results = {}
        self.nepy = None

    def _update_symbols(self):
        """Update atom symbols in NEPY.
        """
        symbols = self.atoms.get_chemical_symbols()
        self.nepy.set_symbols(symbols)

    def _update_cell(self):
        """Update cell parameters in NEPY.
        """
        c = self.atoms.get_cell(complete=True).flatten()
        cell = [c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]]
        self.nepy.set_cell(cell)

    def _update_positions(self):
        """Update atom positions in NEPY.
        """
        positions = list(
            self.atoms.get_positions().T.flatten())  # [x1, ..., xN, y1, ... yN,...]
        self.nepy.set_positions(positions)

    def calculate(self,
                  atoms: Atoms = None,
                  properties: List[str] = None,
                  system_changes: List[str] = all_changes):
        """Calculate energy, per atom energies and forces.

        Parameters
        ----------
        atoms : Atoms, optional
            System for which to calculate properties, by default None
        properties : List[str], optional
            Properties to calculate, by default None
        system_changes : List[str], optional
            Changes to the system since last call, by default all_changes
        """
        if properties is None:
            properties = self.implemented_properties

        Calculator.calculate(self, atoms, properties, system_changes)

        if self.nepy is None:
            # Create new NEPY interface
            self._setup_nepy()
        # Update existing NEPY interface
        for change in system_changes:
            if change == 'positions':
                self._update_positions()
            elif change == 'numbers':
                self._update_symbols()
            elif change == 'cell':
                self._update_cell()

        energies, forces, virials = self.nepy.get_potential_forces_and_virials()
        energies_per_atom = np.array(energies)
        energy = energies_per_atom.sum()
        forces_per_atom = np.array(forces).reshape(-1, self.N_atoms).T
        virials_per_atom = np.array(virials).reshape(-1, self.N_atoms).T
        stress = -(np.sum(virials_per_atom, axis=0) / atoms.get_volume()).reshape(3, 3)

        self.results['energy'] = energy
        self.results['energies'] = energies_per_atom
        self.results['forces'] = forces_per_atom
        self.results['stress'] = stress
