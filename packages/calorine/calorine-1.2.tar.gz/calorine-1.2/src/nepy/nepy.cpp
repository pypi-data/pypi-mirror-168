#include <cmath>
#include <unistd.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>
#include "nepy.h"
#include "nep.cpp"
#include "nep.h"

namespace py = pybind11;

NEPY::NEPY(const std::string &potential_filename, int N_atoms, std::vector<double> cell, std::vector<std::string> atom_symbols, std::vector<double> positions) : nep(potential_filename), potential_filename(potential_filename)
{
  /**
   @brief Wrapper class for NEP3 in nep.cpp.
   @details This class wraps the setup functionality of the NEP3 class in nep.cpp.
   @param potential_filename   Path to the NEP model (/path/nep.txt).
   @param N_atoms              The number of atoms in the structure.
   @param cell                  The cell vectors for the structure.
   @param atom_symbols         The atomic symbol for each atom in the structure.
   @param positions            The position for each atom in the structure.
  */
  atom.N = N_atoms;
  atom.position = positions;
  atom.cell = cell;
  atom.type.resize(atom.N);

  std::vector<std::string>
      model_atom_symbols = _getAtomSymbols(potential_filename); // load atom symbols used in model
  _convertAtomTypeNEPIndex(atom.N, atom_symbols, model_atom_symbols, atom.type);
}

std::vector<double> NEPY::getDescriptors()
{
  std::vector<double> descriptor(atom.N * nep.annmb.dim);
  nep.find_descriptor(
      atom.type, atom.cell, atom.position, descriptor);
  return descriptor;
}

std::tuple<std::vector<double>, std::vector<double>, std::vector<double>> NEPY::getPotentialForcesAndVirials()
{
  std::vector<double> potential(atom.N);
  std::vector<double> force(atom.N * 3);
  std::vector<double> virial(atom.N * 9);
  nep.compute(
      atom.type, atom.cell, atom.position, potential, force, virial);
  return std::make_tuple(potential, force, virial);
}

std::vector<std::string> NEPY::_getAtomSymbols(std::string potential_filename)
/**
 @brief Fetches atomic symbols
 @details This function fetches the atomic symbols from the header of a NEP model. These are later used to ensure consistent indices for the atom types.
 @param potential_filename Path to the NEP model (/path/nep.txt).
 */
{
  std::ifstream input_potential(potential_filename);
  if (!input_potential.is_open())
  {
    std::cout << "Error: cannot open nep.txt.\n";
    exit(1);
  }
  std::string potential_name;
  input_potential >> potential_name;
  int number_of_types;
  input_potential >> number_of_types;
  std::vector<std::string> atom_symbols(number_of_types);
  for (int n = 0; n < number_of_types; ++n)
  {
    input_potential >> atom_symbols[n];
  }
  input_potential.close();
  return atom_symbols;
}

void NEPY::_convertAtomTypeNEPIndex(int N, std::vector<std::string> atom_symbols, std::vector<std::string> model_atom_symbols, std::vector<int> &type)
{
  for (int n = 0; n < N; n++)
  {
    // Convert atom type to index for consistency with nep.txt (potential_filename)
    std::string atom_symbol = atom_symbols[n];
    bool is_allowed_element = false;
    for (int t = 0; (unsigned)t < model_atom_symbols.size(); ++t)
    {
      if (atom_symbol == model_atom_symbols[t])
      {
        type[n] = t;
        is_allowed_element = true;
      }
    }
    if (!is_allowed_element)
    {
      std::cout << "Error: Atom type " << atom_symbols[n] << " not used in the given NEP potential.\n";
      exit(1);
    }
  }
}

void NEPY::setPositions(std::vector<double> positions)
{
  for (int i = 0; i < atom.N * 3; i++)
  {
    atom.position[i] = positions[i];
  }
}

void NEPY::setCell(std::vector<double> cell)
{
  for (int i = 0; i < 9; i++)
  {
    atom.cell[i] = cell[i];
  }
}

void NEPY::setSymbols(std::vector<std::string> atom_symbols)
{
  std::vector<std::string>
      model_atom_symbols = _getAtomSymbols(potential_filename); // load atom symbols used in model
  _convertAtomTypeNEPIndex(atom.N, atom_symbols, model_atom_symbols, atom.type);
}

PYBIND11_MODULE(_nepy, m)
{
  m.doc() = "Pybind11 interface for NEP";
  py::class_<NEPY>(m, "NEPY")
      .def(
          py::init<const std::string &, int, std::vector<double>, std::vector<std::string>, std::vector<double>>(),
          py::arg("potential_filename"),
          py::arg("N_atoms"),
          py::arg("cell"),
          py::arg("atom_symbols"),
          py::arg("positions"),
          py::call_guard<py::scoped_ostream_redirect, py::scoped_estream_redirect>())
      .def("set_positions",
           &NEPY::setPositions,
           "Set atom positions",
           py::arg("positions"))
      .def("set_cell",
           &NEPY::setCell,
           "Set cell",
           py::arg("cell"))
      .def("set_symbols",
           &NEPY::setSymbols,
           "Set atom symbols",
           py::arg("atom_symbols"))
      .def("get_descriptors",
           &NEPY::getDescriptors,
           "Get descriptors")
      .def("get_potential_forces_and_virials",
           &NEPY::getPotentialForcesAndVirials,
           "Get potential, forces and virials");
}