import numpy as np

atomtypes = [
    "N", "CA", "C", "CB", "O", "CG", "CG1", "CG2", "OG", "OG1", "SG", "CD", "CD1",
    "CD2", "ND1", "ND2", "OD1", "OD2", "SD", "CE", "CE1", "CE2", "CE3", "NE", "NE1",
    "NE2", "OE1", "OE2", "CH2", "NH1", "NH2", "OH", "CZ", "CZ2", "CZ3", "NZ", "OXT",
]

# atomtypes = [
#     "N", "CA", "C", "O", "CB", "CG", "CG1", "CG2", "OG", "OG1", "SG", "CD", "CD1",
#     "CD2", "ND1", "ND2", "OD1", "OD2", "OE1", "OE2", "SD", "CE", "CE1", "CE2", "CE3", "NE", "NE1",
#     "NE2", "CH2", "NH1", "NH2", "OH", "CZ", "CZ2", "CZ3", "NZ", "OXT",
# ]

atomtypeid_to_atomtype = {i: j for i, j in enumerate(atomtypes)}
atomtype_to_atomtypeid = {j: i for i, j in enumerate(atomtypes)}

restype1s = [
    "A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "X"
]
restypeid_to_restype1 = {i: j for i, j in enumerate(restype1s)}
restype1_to_restypeid = {j: i for i, j in enumerate(restype1s)}

restype1_to_restype3 = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS", "Q": "GLN", "E": "GLU", "G": "GLY",
    "H": "HIS", "I": "ILE", "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO", "S": "SER",
    "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL", "X": "UNK"
}
restype3s = [restype1_to_restype3[restype1] for restype1 in restype1s]
restype3_to_retype1 = {v: k for k, v in restype1_to_restype3.items()}
restype3_to_restypeid = {restype1_to_restype3[i]: j for i, j in restype1_to_restypeid.items()}
restypeid_to_restype3 = {i: restype1_to_restype3[restype1] for i, restype1 in enumerate(restype1s)}

restype3_to_chi_atomtypes = {
    "ALA": [],
    "ARG": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD"], ["CB", "CG", "CD", "NE"], ["CG", "CD", "NE", "CZ"]],
    "ASN": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "OD1"]],
    "ASP": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "OD1"]],
    "CYS": [["N", "CA", "CB", "SG"]],
    "GLN": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD"], ["CB", "CG", "CD", "OE1"]],
    "GLU": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD"], ["CB", "CG", "CD", "OE1"]],
    "GLY": [],
    "HIS": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "ND1"]],
    "ILE": [["N", "CA", "CB", "CG1"], ["CA", "CB", "CG1", "CD1"]],
    "LEU": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD1"]],
    "LYS": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD"], ["CB", "CG", "CD", "CE"], ["CG", "CD", "CE", "NZ"]],
    "MET": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "SD"], ["CB", "CG", "SD", "CE"]],
    "PHE": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD1"]],
    "PRO": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD"]],
    "SER": [["N", "CA", "CB", "OG"]],
    "THR": [["N", "CA", "CB", "OG1"]],
    "TRP": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD1"]],
    "TYR": [["N", "CA", "CB", "CG"], ["CA", "CB", "CG", "CD1"]],
    "VAL": [["N", "CA", "CB", "CG1"]],
    "UNK": []
}

restype3_to_residue_atom_renaming_swaps = {
    "ASP": {"OD1": "OD2"},
    "GLU": {"OE1": "OE2"},
    "PHE": {"CD1": "CD2", "CE1": "CE2"},
    "TYR": {"CD1": "CD2", "CE1": "CE2"}
}

restype3_to_atoms = {
    "ALA": [["N", 0, [-0.525, 1.363, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, -0.0, -0.0]],
            ["O", 3, [0.627, 1.062, 0.0]], ["CB", 0, [-0.529, -0.774, -1.205]]],
    "ARG": [["N", 0, [-0.524, 1.362, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, -0.0, -0.0]],
            ["O", 3, [0.626, 1.062, 0.0]], ["CB", 0, [-0.524, -0.778, -1.209]], ["CG", 4, [0.616, 1.39, -0.0]],
            ["CD", 5, [0.564, 1.414, 0.0]], ["NE", 6, [0.539, 1.357, -0.0]], ["CZ", 7, [0.758, 1.093, -0.0]],
            ["NH1", 7, [0.206, 2.301, 0.0]], ["NH2", 7, [2.078, 0.978, -0.0]]],
    "ASN": [["N", 0, [-0.536, 1.357, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, -0.0, -0.0]],
            ["O", 3, [0.625, 1.062, 0.0]], ["CB", 0, [-0.531, -0.787, -1.2]], ["CG", 4, [0.584, 1.399, 0.0]],
            ["OD1", 5, [0.633, 1.059, 0.0]], ["ND2", 5, [0.593, -1.188, 0.001]]],
    "ASP": [["N", 0, [-0.525, 1.362, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.527, 0.0, -0.0]],
            ["O", 3, [0.626, 1.062, -0.0]], ["CB", 0, [-0.526, -0.778, -1.208]], ["CG", 4, [0.593, 1.398, -0.0]],
            ["OD1", 5, [0.61, 1.091, 0.0]], ["OD2", 5, [0.592, -1.101, -0.003]]],
    "CYS": [["N", 0, [-0.522, 1.362, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.524, 0.0, 0.0]],
            ["O", 3, [0.625, 1.062, -0.0]], ["CB", 0, [-0.519, -0.773, -1.212]], ["SG", 4, [0.728, 1.653, 0.0]]],
    "GLN": [["N", 0, [-0.526, 1.361, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, 0.0, 0.0]],
            ["O", 3, [0.626, 1.062, -0.0]], ["CB", 0, [-0.525, -0.779, -1.207]], ["CG", 4, [0.615, 1.393, 0.0]],
            ["CD", 5, [0.587, 1.399, -0.0]], ["OE1", 6, [0.634, 1.06, 0.0]], ["NE2", 6, [0.593, -1.189, -0.001]]],
    "GLU": [["N", 0, [-0.528, 1.361, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, -0.0, -0.0]],
            ["O", 3, [0.626, 1.062, 0.0]], ["CB", 0, [-0.526, -0.781, -1.207]], ["CG", 4, [0.615, 1.392, 0.0]],
            ["CD", 5, [0.6, 1.397, 0.0]], ["OE1", 6, [0.607, 1.095, -0.0]], ["OE2", 6, [0.589, -1.104, -0.001]]],
    "GLY": [["N", 0, [-0.572, 1.337, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.517, -0.0, -0.0]],
            ["O", 3, [0.626, 1.062, -0.0]]],
    "HIS": [["N", 0, [-0.527, 1.36, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, 0.0, 0.0]],
            ["O", 3, [0.625, 1.063, 0.0]], ["CB", 0, [-0.525, -0.778, -1.208]], ["CG", 4, [0.6, 1.37, -0.0]],
            ["ND1", 5, [0.744, 1.16, -0.0]], ["CD2", 5, [0.889, -1.021, 0.003]], ["CE1", 5, [2.03, 0.851, 0.002]],
            ["NE2", 5, [2.145, -0.466, 0.004]]],
    "ILE": [["N", 0, [-0.493, 1.373, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.527, -0.0, -0.0]],
            ["O", 3, [0.627, 1.062, -0.0]], ["CB", 0, [-0.536, -0.793, -1.213]], ["CG1", 4, [0.534, 1.437, -0.0]],
            ["CG2", 4, [0.54, -0.785, -1.199]], ["CD1", 5, [0.619, 1.391, 0.0]]],
    "LEU": [["N", 0, [-0.52, 1.363, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, -0.0, -0.0]],
            ["O", 3, [0.625, 1.063, -0.0]], ["CB", 0, [-0.522, -0.773, -1.214]], ["CG", 4, [0.678, 1.371, 0.0]],
            ["CD1", 5, [0.53, 1.43, -0.0]], ["CD2", 5, [0.535, -0.774, 1.2]]],
    "LYS": [["N", 0, [-0.526, 1.362, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, 0.0, 0.0]],
            ["O", 3, [0.626, 1.062, -0.0]], ["CB", 0, [-0.524, -0.778, -1.208]], ["CG", 4, [0.619, 1.39, 0.0]],
            ["CD", 5, [0.559, 1.417, 0.0]], ["CE", 6, [0.56, 1.416, 0.0]], ["NZ", 7, [0.554, 1.387, 0.0]]],
    "MET": [["N", 0, [-0.521, 1.364, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, 0.0, 0.0]],
            ["O", 3, [0.625, 1.062, -0.0]], ["CB", 0, [-0.523, -0.776, -1.21]], ["CG", 4, [0.613, 1.391, -0.0]],
            ["SD", 5, [0.703, 1.695, 0.0]], ["CE", 6, [0.32, 1.786, -0.0]]],
    "PHE": [["N", 0, [-0.518, 1.363, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.524, 0.0, -0.0]],
            ["O", 3, [0.626, 1.062, -0.0]], ["CB", 0, [-0.525, -0.776, -1.212]], ["CG", 4, [0.607, 1.377, 0.0]],
            ["CD1", 5, [0.709, 1.195, -0.0]], ["CD2", 5, [0.706, -1.196, 0.0]], ["CE1", 5, [2.102, 1.198, -0.0]],
            ["CE2", 5, [2.098, -1.201, -0.0]], ["CZ", 5, [2.794, -0.003, -0.001]]],
    "PRO": [["N", 0, [-0.566, 1.351, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.527, -0.0, 0.0]],
            ["O", 3, [0.621, 1.066, 0.0]], ["CB", 0, [-0.546, -0.611, -1.293]], ["CG", 4, [0.382, 1.445, 0.0]],
            ["CD", 5, [0.477, 1.424, 0.0]]],
    "SER": [["N", 0, [-0.529, 1.36, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, -0.0, -0.0]],
            ["O", 3, [0.626, 1.062, -0.0]], ["CB", 0, [-0.518, -0.777, -1.211]], ["OG", 4, [0.503, 1.325, 0.0]]],
    "THR": [["N", 0, [-0.517, 1.364, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.526, 0.0, -0.0]],
            ["O", 3, [0.626, 1.062, 0.0]], ["CB", 0, [-0.516, -0.793, -1.215]], ["OG1", 4, [0.472, 1.353, 0.0]],
            ["CG2", 4, [0.55, -0.718, -1.228]]],
    "TRP": [["N", 0, [-0.521, 1.363, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.525, -0.0, 0.0]],
            ["O", 3, [0.627, 1.062, 0.0]], ["CB", 0, [-0.523, -0.776, -1.212]], ["CG", 4, [0.609, 1.37, -0.0]],
            ["CD1", 5, [0.824, 1.091, 0.0]], ["CD2", 5, [0.854, -1.148, -0.005]], ["NE1", 5, [2.14, 0.69, -0.004]],
            ["CE2", 5, [2.186, -0.678, -0.007]], ["CE3", 5, [0.622, -2.53, -0.007]],
            ["CZ2", 5, [3.283, -1.543, -0.011]],
            ["CZ3", 5, [1.715, -3.389, -0.011]], ["CH2", 5, [3.028, -2.89, -0.013]]],
    "TYR": [["N", 0, [-0.522, 1.362, 0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.524, -0.0, -0.0]],
            ["O", 3, [0.627, 1.062, -0.0]], ["CB", 0, [-0.522, -0.776, -1.213]], ["CG", 4, [0.607, 1.382, -0.0]],
            ["CD1", 5, [0.716, 1.195, -0.0]], ["CD2", 5, [0.713, -1.194, -0.001]], ["CE1", 5, [2.107, 1.2, -0.002]],
            ["CE2", 5, [2.104, -1.201, -0.003]], ["CZ", 5, [2.791, -0.001, -0.003]],
            ["OH", 5, [4.168, -0.002, -0.005]]],
    "VAL": [["N", 0, [-0.494, 1.373, -0.0]], ["CA", 0, [0.0, 0.0, 0.0]], ["C", 0, [1.527, -0.0, -0.0]],
            ["O", 3, [0.627, 1.062, -0.0]], ["CB", 0, [-0.533, -0.795, -1.213]], ["CG1", 4, [0.54, 1.429, -0.0]],
            ["CG2", 4, [0.533, -0.776, 1.203]]],
    "UNK": []
}

restype3_to_atomtypes = {restype3: list(zip(*atomtypes14))[0] if restype3 != "UNK" else ()
                         for restype3, atomtypes14 in restype3_to_atoms.items()}

restypeid_to_chi_atomids = [[[restype3_to_atomtypes[restype3].index(atomtype) for atomtype in chiatomstypes]
                             for chiatomstypes in restype3_to_chi_atomtypes[restype3]]
                            for restype3 in restype3s]

CA1_CA2_dis = 3.80209737096
van_der_waals_radius = {"C": 1.7, "N": 1.55, "O": 1.52, "S": 1.8}
C1_N2_bond = [1.329, 1.341]
C1_N2_bond_stddev = [0.014, 0.016]
C1_N2_CA2_angle = -0.5203
C1_N2_CA2_angle_stddev = 0.0353
CA1_C1_N2_angle = -0.4473
CA1_C1_N2_angle_stddev = 0.0311

restype3_to_within_residue_bonds = {
    "ALA": [["CA", "CB", 1.52, 0.021], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "ARG": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.521, 0.027], ["CG", "CD", 1.515, 0.025],
            ["CD", "NE", 1.46, 0.017], ["NE", "CZ", 1.326, 0.013], ["CZ", "NH1", 1.326, 0.013],
            ["CZ", "NH2", 1.326, 0.013], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "ASN": [["CA", "CB", 1.527, 0.026], ["CB", "CG", 1.506, 0.023], ["CG", "OD1", 1.235, 0.022],
            ["CG", "ND2", 1.324, 0.025], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "ASP": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.513, 0.021], ["CG", "OD1", 1.249, 0.023],
            ["CG", "OD2", 1.249, 0.023], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "CYS": [["CA", "CB", 1.526, 0.013], ["CB", "SG", 1.812, 0.016], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "GLU": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.517, 0.019], ["CG", "CD", 1.515, 0.015],
            ["CD", "OE1", 1.252, 0.011], ["CD", "OE2", 1.252, 0.011], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "GLN": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.521, 0.027], ["CG", "CD", 1.506, 0.023],
            ["CD", "OE1", 1.235, 0.022], ["CD", "NE2", 1.324, 0.025], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "GLY": [["N", "CA", 1.456, 0.015], ["CA", "C", 1.514, 0.016], ["C", "O", 1.232, 0.016]],
    "HIS": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.492, 0.016], ["CG", "ND1", 1.369, 0.015],
            ["CG", "CD2", 1.353, 0.017], ["ND1", "CE1", 1.343, 0.025], ["CD2", "NE2", 1.415, 0.021],
            ["CE1", "NE2", 1.322, 0.023], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "ILE": [["CA", "CB", 1.544, 0.023], ["CB", "CG1", 1.536, 0.028], ["CB", "CG2", 1.524, 0.031],
            ["CG1", "CD1", 1.5, 0.069], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "LEU": [["CA", "CB", 1.533, 0.023], ["CB", "CG", 1.521, 0.029], ["CG", "CD1", 1.514, 0.037],
            ["CG", "CD2", 1.514, 0.037], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "LYS": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.521, 0.027], ["CG", "CD", 1.52, 0.034],
            ["CD", "CE", 1.508, 0.025], ["CE", "NZ", 1.486, 0.025], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "MET": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.509, 0.032], ["CG", "SD", 1.807, 0.026],
            ["SD", "CE", 1.774, 0.056], ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026],
            ["C", "O", 1.229, 0.019]],
    "PHE": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.509, 0.017], ["CG", "CD1", 1.383, 0.015],
            ["CG", "CD2", 1.383, 0.015], ["CD1", "CE1", 1.388, 0.02], ["CD2", "CE2", 1.388, 0.02],
            ["CE1", "CZ", 1.369, 0.019], ["CE2", "CZ", 1.369, 0.019], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "PRO": [["CA", "CB", 1.531, 0.02], ["CB", "CG", 1.495, 0.05], ["CG", "CD", 1.502, 0.033],
            ["CD", "N", 1.474, 0.014], ["N", "CA", 1.468, 0.017], ["CA", "C", 1.524, 0.02],
            ["C", "O", 1.228, 0.02]],
    "SER": [["CA", "CB", 1.525, 0.015], ["CB", "OG", 1.418, 0.013], ["N", "CA", 1.459, 0.02],
            ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "THR": [["CA", "CB", 1.529, 0.026], ["CB", "OG1", 1.428, 0.02], ["CB", "CG2", 1.519, 0.033],
            ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "TRP": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.498, 0.018], ["CG", "CD1", 1.363, 0.014],
            ["CG", "CD2", 1.432, 0.017], ["CD1", "NE1", 1.375, 0.017], ["NE1", "CE2", 1.371, 0.013],
            ["CD2", "CE2", 1.409, 0.012], ["CD2", "CE3", 1.399, 0.015], ["CE2", "CZ2", 1.393, 0.017],
            ["CE3", "CZ3", 1.38, 0.017], ["CZ2", "CH2", 1.369, 0.019], ["CZ3", "CH2", 1.396, 0.016],
            ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "TYR": [["CA", "CB", 1.535, 0.022], ["CB", "CG", 1.512, 0.015], ["CG", "CD1", 1.387, 0.013],
            ["CG", "CD2", 1.387, 0.013], ["CD1", "CE1", 1.389, 0.015], ["CD2", "CE2", 1.389, 0.015],
            ["CE1", "CZ", 1.381, 0.013], ["CE2", "CZ", 1.381, 0.013], ["CZ", "OH", 1.374, 0.017],
            ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "VAL": [["CA", "CB", 1.543, 0.021], ["CB", "CG1", 1.524, 0.021], ["CB", "CG2", 1.524, 0.021],
            ["N", "CA", 1.459, 0.02], ["CA", "C", 1.525, 0.026], ["C", "O", 1.229, 0.019]],
    "UNK": []
}

restype3_to_within_residue_angles = {
    "ALA": [["N", "CA", "CB", 110.1, 1.4], ["CB", "CA", "C", 110.1, 1.5], ["N", "CA", "C", 111.0, 2.7],
            ["CA", "C", "O", 120.1, 2.1]],
    "ARG": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "CD", 111.6, 2.6], ["CG", "CD", "NE", 111.8, 2.1], ["CD", "NE", "CZ", 123.6, 1.4],
            ["NE", "CZ", "NH1", 120.3, 0.5], ["NE", "CZ", "NH2", 120.3, 0.5], ["NH1", "CZ", "NH2", 119.4, 1.1],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "ASN": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "ND2", 116.7, 2.4], ["CB", "CG", "OD1", 121.6, 2.0], ["ND2", "CG", "OD1", 121.9, 2.3],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "ASP": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "OD1", 118.3, 0.9], ["CB", "CG", "OD2", 118.3, 0.9], ["OD1", "CG", "OD2", 123.3, 1.9],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "CYS": [["N", "CA", "CB", 110.8, 1.5], ["CB", "CA", "C", 111.5, 1.2], ["CA", "CB", "SG", 114.2, 1.1],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "GLU": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "CD", 114.2, 2.7], ["CG", "CD", "OE1", 118.3, 2.0], ["CG", "CD", "OE2", 118.3, 2.0],
            ["OE1", "CD", "OE2", 123.3, 1.2], ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "GLN": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "CD", 111.6, 2.6], ["CG", "CD", "OE1", 121.6, 2.0], ["CG", "CD", "NE2", 116.7, 2.4],
            ["OE1", "CD", "NE2", 121.9, 2.3], ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "GLY": [["N", "CA", "C", 113.1, 2.5], ["CA", "C", "O", 120.6, 1.8]],
    "HIS": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.6, 1.7],
            ["CB", "CG", "ND1", 123.2, 2.5], ["CB", "CG", "CD2", 130.8, 3.1], ["CG", "ND1", "CE1", 108.2, 1.4],
            ["ND1", "CE1", "NE2", 109.9, 2.2], ["CE1", "NE2", "CD2", 106.6, 2.5], ["NE2", "CD2", "CG", 109.2, 1.9],
            ["CD2", "CG", "ND1", 106.0, 1.4], ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "ILE": [["N", "CA", "CB", 110.8, 2.3], ["CB", "CA", "C", 111.6, 2.0], ["CA", "CB", "CG1", 111.0, 1.9],
            ["CB", "CG1", "CD1", 113.9, 2.8], ["CA", "CB", "CG2", 110.9, 2.0], ["CG1", "CB", "CG2", 111.4, 2.2],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "LEU": [["N", "CA", "CB", 110.4, 2.0], ["CB", "CA", "C", 110.2, 1.9], ["CA", "CB", "CG", 115.3, 2.3],
            ["CB", "CG", "CD1", 111.0, 1.7], ["CB", "CG", "CD2", 111.0, 1.7], ["CD1", "CG", "CD2", 110.5, 3.0],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "LYS": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 2.2],
            ["CB", "CG", "CD", 111.6, 2.6], ["CG", "CD", "CE", 111.9, 3.0], ["CD", "CE", "NZ", 111.7, 2.3],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "MET": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.3, 1.7],
            ["CB", "CG", "SD", 112.4, 3.0], ["CG", "SD", "CE", 100.2, 1.6], ["N", "CA", "C", 111.0, 2.7],
            ["CA", "C", "O", 120.1, 2.1]],
    "PHE": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.9, 2.4],
            ["CB", "CG", "CD1", 120.8, 0.7], ["CB", "CG", "CD2", 120.8, 0.7], ["CD1", "CG", "CD2", 118.3, 1.3],
            ["CG", "CD1", "CE1", 120.8, 1.1], ["CG", "CD2", "CE2", 120.8, 1.1], ["CD1", "CE1", "CZ", 120.1, 1.2],
            ["CD2", "CE2", "CZ", 120.1, 1.2], ["CE1", "CZ", "CE2", 120.0, 1.8], ["N", "CA", "C", 111.0, 2.7],
            ["CA", "C", "O", 120.1, 2.1]],
    "PRO": [["N", "CA", "CB", 103.3, 1.2], ["CB", "CA", "C", 111.7, 2.1], ["CA", "CB", "CG", 104.8, 1.9],
            ["CB", "CG", "CD", 106.5, 3.9], ["CG", "CD", "N", 103.2, 1.5], ["CA", "N", "CD", 111.7, 1.4],
            ["N", "CA", "C", 112.1, 2.6], ["CA", "C", "O", 120.2, 2.4]],
    "SER": [["N", "CA", "CB", 110.5, 1.5], ["CB", "CA", "C", 110.1, 1.9], ["CA", "CB", "OG", 111.2, 2.7],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "THR": [["N", "CA", "CB", 110.3, 1.9], ["CB", "CA", "C", 111.6, 2.7], ["CA", "CB", "OG1", 109.0, 2.1],
            ["CA", "CB", "CG2", 112.4, 1.4], ["OG1", "CB", "CG2", 110.0, 2.3], ["N", "CA", "C", 111.0, 2.7],
            ["CA", "C", "O", 120.1, 2.1]],
    "TRP": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.7, 1.9],
            ["CB", "CG", "CD1", 127.0, 1.3], ["CB", "CG", "CD2", 126.6, 1.3], ["CD1", "CG", "CD2", 106.3, 0.8],
            ["CG", "CD1", "NE1", 110.1, 1.0], ["CD1", "NE1", "CE2", 109.0, 0.9], ["NE1", "CE2", "CD2", 107.3, 1.0],
            ["CE2", "CD2", "CG", 107.3, 0.8], ["CG", "CD2", "CE3", 133.9, 0.9], ["NE1", "CE2", "CZ2", 130.4, 1.1],
            ["CE3", "CD2", "CE2", 118.7, 1.2], ["CD2", "CE2", "CZ2", 122.3, 1.2], ["CE2", "CZ2", "CH2", 117.4, 1.0],
            ["CZ2", "CH2", "CZ3", 121.6, 1.2], ["CH2", "CZ3", "CE3", 121.2, 1.1], ["CZ3", "CE3", "CD2", 118.8, 1.3],
            ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "TYR": [["N", "CA", "CB", 110.6, 1.8], ["CB", "CA", "C", 110.4, 2.0], ["CA", "CB", "CG", 113.4, 1.9],
            ["CB", "CG", "CD1", 121.0, 0.6], ["CB", "CG", "CD2", 121.0, 0.6], ["CD1", "CG", "CD2", 117.9, 1.1],
            ["CG", "CD1", "CE1", 121.3, 0.8], ["CG", "CD2", "CE2", 121.3, 0.8], ["CD1", "CE1", "CZ", 119.8, 0.9],
            ["CD2", "CE2", "CZ", 119.8, 0.9], ["CE1", "CZ", "CE2", 119.8, 1.6], ["CE1", "CZ", "OH", 120.1, 2.7],
            ["CE2", "CZ", "OH", 120.1, 2.7], ["N", "CA", "C", 111.0, 2.7], ["CA", "C", "O", 120.1, 2.1]],
    "VAL": [["N", "CA", "CB", 111.5, 2.2], ["CB", "CA", "C", 111.4, 1.9], ["CA", "CB", "CG1", 110.9, 1.5],
            ["CA", "CB", "CG2", 110.9, 1.5], ["CG1", "CB", "CG2", 110.9, 1.6], ["N", "CA", "C", 111.0, 2.7],
            ["CA", "C", "O", 120.1, 2.1]],
    "UNK": []
}

# Virtual Bond include bond/angle
restype3_to_within_residue_virtural_bonds = {restype3: dict() for restype3 in restype3s}
for restype3 in restype3s:
    for bond_info in restype3_to_within_residue_bonds[restype3]:
        restype3_to_within_residue_virtural_bonds[restype3][f"{bond_info[0]}-{bond_info[1]}"] = \
            [bond_info[2], bond_info[3]]
        restype3_to_within_residue_virtural_bonds[restype3][f"{bond_info[1]}-{bond_info[0]}"] = \
            [bond_info[2], bond_info[3]]
    for angle_info in restype3_to_within_residue_angles[restype3]:
        b1 = restype3_to_within_residue_virtural_bonds[restype3][f"{angle_info[0]}-{angle_info[1]}"][0]
        b2 = restype3_to_within_residue_virtural_bonds[restype3][f"{angle_info[1]}-{angle_info[2]}"][0]
        b1stddev = restype3_to_within_residue_virtural_bonds[restype3][f"{angle_info[0]}-{angle_info[1]}"][1]
        b2stddev = restype3_to_within_residue_virtural_bonds[restype3][f"{angle_info[1]}-{angle_info[2]}"][1]
        arg = angle_info[3] / 180 * np.pi
        length = np.sqrt(b1 ** 2 + b2 ** 2 - 2 * b1 * b2 * np.cos(arg))
        dl_dgamma = (b1 * b2 * np.sin(arg)) / length
        dl_db1 = (b1 - b2 * np.cos(arg)) / length
        dl_db2 = (b2 - b1 * np.cos(arg)) / length
        stddev = np.sqrt(
            (dl_dgamma * angle_info[4] / 180 * np.pi) ** 2 + (dl_db1 * b1stddev) ** 2 + (dl_db2 * b2stddev) ** 2)
        restype3_to_within_residue_virtural_bonds[restype3]["-".join([angle_info[0], angle_info[2]])] = \
            [length, stddev]
        restype3_to_within_residue_virtural_bonds[restype3]["-".join([angle_info[2], angle_info[0]])] = \
            [length, stddev]
# print(restype3_to_within_residue_virtural_bonds["ALA"])

restype3_to_within_residue_vdW_pair = {restype3: dict() for restype3 in restype3s}
for restype3 in restype3s:
    for atomtype1 in restype3_to_atomtypes[restype3]:
        for atomtype2 in restype3_to_atomtypes[restype3]:
            dis = van_der_waals_radius[atomtype1[0]] + van_der_waals_radius[atomtype2[0]]
            restype3_to_within_residue_vdW_pair[restype3][f"{atomtype1}-{atomtype2}"] = dis
            restype3_to_within_residue_vdW_pair[restype3][f"{atomtype2}-{atomtype1}"] = dis

# print(restype3_to_within_residue_vdW_pair["ALA"])

# atommask14=np.array([[True]*len(restype3_to_atomtypes[restype3])+
#                                          [False]*(14-len(restype3_to_atomtypes[restype3])) for restype3 in restype3s])
#
# atomtype14=np.array([[atomtype_to_atomtypeid[atomtype] for atomtype in restype3_to_atomtypes[restype3]]+
#                                          [len(atomtypes)-1]*(14-len(restype3_to_atomtypes[restype3])) for restype3 in restype3s])

atomtypes_num = len(atomtypes)
restypes_num = len(restype1s)

# pseudo_beta=[]
# for restype3 in restype3s[:-1]:
#     atomtypes=restype3_to_atomtypes[restype3]
#     print(atomtypes)
#     if "CB" in atomtypes:
#         pseudo_beta.append(atomtypes.index("CB"))
#     else:
#         pseudo_beta.append(atomtypes.index("CA"))
#
#
# print(pseudo_beta)

def ATOM_RECORD_LINE(record: str = "ATOM",
                     atom_ind: int = 1,
                     atom_name: str = "C",
                     alt_location: str = "",
                     res_name: str = "GRO",
                     chain_id: str = "A",
                     res_ind:int=1,
                     insertion:str="",
                     x:float=0.,
                     y:float=0.,
                     z:float=0.,
                     occupancy:float=1.,
                     bfactor:float=1.,
                     seg_id:str="",
                     element:str="C",
                     charge:str=""):
    return (f"{record:<6}"
            f"{atom_ind:>5d}"
            f" "
            f"{atom_name if len(atom_name)>=4 else ' '+atom_name:<4}"
            f"{alt_location:>1}"
            f"{res_name:>3}"
            f" "
            f"{chain_id:>1}"
            f"{res_ind:>4d}"
            f"{insertion:>1}"
            f"   "
            f"{x:>8.3f}"
            f"{y:>8.3f}"
            f"{z:>8.3f}"
            f"{occupancy:>6.2f}"
            f"{bfactor:>6.2f}"
            f"      "
            f"{seg_id:<4}"
            f"{element:>2}"
            f"{charge:>2}")


def makepdb(aatype,poses,plddt,chain_id: str = "", alt_loc: str = "", insertion_code: str = "", occupancy: float = 1.0,
                   charge: str = ""):
    pdblines=[]
    atom_index = -1
    res_index = -1
    for restypeid in aatype:
        res_index += 1
        restype3 = restypeid_to_restype3[restypeid]
        atomtypes = restype3_to_atomtypes[restype3]
        atom_residue_index = -1
        for atomid,atomtype in enumerate(atomtypes):
            x,y,z=poses[res_index][atomid]
            atom_residue_index += 1
            atom_index += 1
            atom_line = ATOM_RECORD_LINE(
                atom_ind=atom_index + 1, atom_name=atomtype, alt_location=alt_loc, res_name=restype3,
                chain_id=chain_id, res_ind=res_index + 1, insertion=insertion_code,
                x=x,
                y=y,
                z=z,
                occupancy=occupancy, bfactor=plddt[res_index],
                element=atomtype[0], charge=charge)
            pdblines.append(atom_line)
    return "\n".join(pdblines)