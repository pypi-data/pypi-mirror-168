"""This file contains metadata to help describe the results of DFTB+
calculations, etc.
"""
"""Properties that DFTB+ produces, depending on the type of calculation.
"""
properties = {
    "total_energy": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The total energy",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "energy_per_formula_unit": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The energy per empirical formula unit",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "energy of formation": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The energy of formation",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "kJ/mol",
    },
    "fermi_level": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The Fermi level",
        "dimensionality": [2],
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "number_of_electrons": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The number of electrons",
        "dimensionality": [2],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "mermin_energy": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The Mermin energy",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "extrapolated0_energy": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The energy extrapolated to no smearing",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "forcerelated_energy": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The force-related energy",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "dipole_moments": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The dipole moments of the system",
        "dimensionality": [3, "nspins"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "eigenvalues": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The eigenvalues",
        "dimensionality": ["norbitals"],
        "methods": [],
        "type": "float",
        "units": "hartree",
    },
    "filling": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The orbital occupancy",
        "dimensionality": ["norbitals"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "orbital_charges": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The orbital charges",
        "dimensionality": ["natoms", "natoms"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "gross_atomic_charges": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The charges on the atoms",
        "dimensionality": ["natoms"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "gross_atomic_spins": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The spins on the atoms",
        "dimensionality": ["natoms"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "atomic_dipole_moment": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The dipole moments of the atoms",
        "dimensionality": [3, "natoms"],
        "methods": [],
        "type": "float",
        "units": "",
    },
    "forces": {
        "calculation": ["optimization"],
        "description": "The forces on the atoms",
        "dimensionality": [3, "natoms"],
        "methods": [],
        "type": "float",
        "units": "hartree/bohr",
    },
    "stress": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The stress",
        "dimensionality": [3, 3],
        "methods": [],
        "type": "float",
        "units": "Å^3",
    },
    "#_primitive_cells": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The number of primitive cells in the unit cell",
        "dimensionality": "scalar",
        "methods": [],
        "type": "integer",
        "units": "",
    },
    "Z": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The number of empirical formula u its in the system",
        "dimensionality": "scalar",
        "methods": [],
        "type": "integer",
        "units": "",
    },
    "formula": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The chemical formula of the system",
        "dimensionality": "scalar",
        "methods": [],
        "type": "string",
        "units": "",
    },
    "empirical_formula": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The empirical formula of the system",
        "dimensionality": "scalar",
        "methods": [],
        "type": "string",
        "units": "",
    },
    "cell_volume": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "The volume of the unit cell",
        "dimensionality": "scalar",
        "methods": [],
        "type": "float",
        "units": "Å^3",
    },
}
