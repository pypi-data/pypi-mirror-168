import torch
from Ginobifold import residue_constants
import copy

atomtypeid_to_van_der_waals_radius = torch.tensor(
    [residue_constants.van_der_waals_radius[name[0]] for name in residue_constants.atomtypes])

restypeid_to_atommasks = torch.tensor([[True] * len(residue_constants.restype3_to_atomtypes[restype3])
                                       + [False] * (14 - len(residue_constants.restype3_to_atomtypes[restype3]))
                                       for restype3 in residue_constants.restype3s])
restypeid_to_atomtypeids = torch.tensor([[residue_constants.atomtype_to_atomtypeid[atomtype]
                                          for atomtype in residue_constants.restype3_to_atomtypes[restype3]]
                                         + [0] * (14 - len(residue_constants.restype3_to_atomtypes[restype3]))
                                         for restype3 in residue_constants.restype3s])


def within_residue_bounds(overlap_tolerance=1.5, bond_length_tolerance_factor=15):
    lower_bound = torch.zeros([residue_constants.restypes_num, 14, 14])
    upper_bound = torch.zeros([residue_constants.restypes_num, 14, 14])
    for restypeid, restype3 in enumerate(residue_constants.restype3s):
        for atomtypeid1, atomtype1 in enumerate(residue_constants.restype3_to_atomtypes[restype3]):
            for atomtypeid2, atomtype2 in enumerate(residue_constants.restype3_to_atomtypes[restype3]):
                virtual_bonds = residue_constants.restype3_to_within_residue_virtural_bonds[restype3]
                vdw_pairs = residue_constants.restype3_to_within_residue_vdW_pair[restype3]
                atomtype12 = f"{atomtype1}-{atomtype2}"
                if atomtype12 in virtual_bonds:
                    lower_bound[restypeid, atomtypeid1, atomtypeid2] = virtual_bonds[atomtype12][
                                                                           0] - bond_length_tolerance_factor * \
                                                                       virtual_bonds[atomtype12][1]
                    upper_bound[restypeid, atomtypeid1, atomtypeid2] = virtual_bonds[atomtype12][
                                                                           0] + bond_length_tolerance_factor * \
                                                                       virtual_bonds[atomtype12][1]
                else:
                    lower_bound[restypeid, atomtypeid1, atomtypeid2] = vdw_pairs[atomtype12] - overlap_tolerance
                    upper_bound[restypeid, atomtypeid1, atomtypeid2] = 1E10
    return lower_bound, upper_bound


default_within_residue_lower_bounds, default_within_residue_upper_bounds = within_residue_bounds()

restypeid_to_torsion_masks = torch.tensor(
    [[True] * (len(l) + 3) + [False] * (4 - len(l)) for l in residue_constants.restypeid_to_chi_atomids])
restypeid_to_torsion_atom_index = torch.tensor([[[1, 2, 0, 1],  # pre_omega
                                                 [2, 0, 1, 2],  # phi
                                                 [0, 1, 2,
                                                  3]] +  # psi Because the angle need mirror so as to turn O into C
                                                l + [[0, 0, 0, 0]] * (4 - len(l)) for l in
                                                residue_constants.restypeid_to_chi_atomids], dtype=torch.long)

torsion_atom_use_pre = torch.tensor([[-1, -1, 0, 0], [-1, 0, 0, 0]] + [[0, 0, 0, 0]] * 5, dtype=torch.long)

chi_pi_periodic = [[1 if restype3 in residue_constants.restype3_to_residue_atom_renaming_swaps and
                         len(set(chiatoms) & set(
                             residue_constants.restype3_to_residue_atom_renaming_swaps[restype3])) > 0 else 0
                    for chiatoms in residue_constants.restype3_to_chi_atomtypes[restype3]] for restype3 in
                   residue_constants.restype3s]

restypeid_to_alt_torsion_factor = 1 - 2 * torch.tensor([[0, 0, 0] + i + [0] * (4 - len(i)) for i in chi_pi_periodic],
                                                       dtype=torch.long)

restypeid_to_alt_pos_factor = torch.eye(14)[None].repeat([21, 1, 1])
restypeid_to_swap_atom_masks = torch.zeros([residue_constants.restypes_num, 14], dtype=torch.bool)
for restype3 in residue_constants.restype3_to_residue_atom_renaming_swaps:
    restype3id = residue_constants.restype3_to_restypeid[restype3]
    for k, v in residue_constants.restype3_to_residue_atom_renaming_swaps[restype3].items():
        id1 = residue_constants.restype3_to_atomtypes[restype3].index(k)
        id2 = residue_constants.restype3_to_atomtypes[restype3].index(v)
        restypeid_to_swap_atom_masks[restype3id, id1] = True
        restypeid_to_swap_atom_masks[restype3id, id2] = True
        restypeid_to_alt_pos_factor[restype3id, id1, id1] = 0
        restypeid_to_alt_pos_factor[restype3id, id2, id2] = 0
        restypeid_to_alt_pos_factor[restype3id, id1, id2] = 1
        restypeid_to_alt_pos_factor[restype3id, id2, id1] = 1


def make_frame_rt4(ex, ey, trans):
    ex_n = ex / ex.norm()
    ey_l = ey - torch.dot(ey, ex_n) * ex_n
    ey_n = ey_l / ey_l.norm()
    ez_n = torch.cross(ex_n, ey_n)
    b = torch.eye(4)
    b[:3] = torch.stack([ex_n, ey_n, ez_n, trans], dim=1)
    # print(b)
    return b


# default_frame_rots = torch.zeros([21, 8, 3, 3])
# default_frame_trans = torch.zeros([21, 8, 3, 1])
default_frame_rt4 = torch.eye(4)[None, None].repeat([21, 8, 1, 1])
# print(default_frame_rt4.shape)


default_black_hole_position = torch.zeros([21, 14, 3], dtype=torch.float)

for restypeid, restype3 in enumerate(residue_constants.restype3s[:20]):
    poses = [torch.tensor(i[2]) for i in residue_constants.restype3_to_atoms[restype3]]
    for pid, p in enumerate(poses):
        default_black_hole_position[restypeid, pid] = p
    base_atom_positions = [[poses[residue_constants.restype3_to_atomtypes[restype3].index(atomname)] for atomname in
                            atomnames] for atomnames in residue_constants.restype3_to_chi_atomtypes[restype3]]
    # print(base_atom_positions)
    # BB and pre_omega set eye4
    # phi C0-N-CA-C
    default_frame_rt4[restypeid, 2] = make_frame_rt4(poses[0] - poses[1], torch.tensor([1., 0, 0]), poses[0])
    # psi N-C-CA-O
    # print(poses[2])
    default_frame_rt4[restypeid, 3] = make_frame_rt4(poses[2] - poses[1], poses[1] - poses[0], poses[2])

    for chi_id in range(len(base_atom_positions)):
        if chi_id == 0:
            default_frame_rt4[restypeid, chi_id + 4] = make_frame_rt4(
                base_atom_positions[chi_id][2] - base_atom_positions[chi_id][1],
                base_atom_positions[chi_id][0] - base_atom_positions[chi_id][1],
                base_atom_positions[chi_id][2]
            )
        else:
            default_frame_rt4[restypeid, chi_id + 4] = make_frame_rt4(
                base_atom_positions[chi_id][2],
                torch.tensor([-1., 0, 0]),
                base_atom_positions[chi_id][2]
            )
import torch.nn.functional as F

default_black_hole_position = F.pad(default_black_hole_position, pad=[0, 1, 0, 0, 0, 0], value=1.)

# print(default_black_hole_position[1])


resid_to_atom_frameid = torch.zeros([21, 14], dtype=torch.long)
for resid, restype3 in enumerate(residue_constants.restype3s):
    for atom_id, atom in enumerate(residue_constants.restype3_to_atoms[restype3]):
        resid_to_atom_frameid[resid, atom_id] = atom[1]


# resid_to_frame_4x4 = default_frame_rt4[[torch.arange(21)[:, None].repeat([1, 14]), resid_to_atom_frameid]]

# pos = torch.einsum("...Aij,...Aj->...Ai", resid_to_frame_4x4[1], default_black_hole_position[1])
# print(pos[:, :3])

# print(resid_to_atom_frameid[3])


def make_torsion_rt_4x4_sincos(sincos):
    NUM_RES = len(sincos)
    sins = F.pad(sincos[:, :, 0], [1, 0, 0, 0], value=0.)
    coss = F.pad(sincos[:, :, 1], [1, 0, 0, 0], value=1.)
    zeros = torch.zeros([NUM_RES, 8], device=sincos.device)
    ones = torch.ones([NUM_RES, 8], device=sincos.device)
    return torch.stack([ones, zeros, zeros, zeros,
                        zeros, coss, -sins, zeros,
                        zeros, sins, coss, zeros,
                        zeros, zeros, zeros, ones], dim=-1).view([NUM_RES, 8, 4, 4])


# def make_torsion_rt_4x4_arg(arg):
#     NUM_RES = len(arg)
#     _arg = F.pad(arg, [1, 0, 0, 0], value=0.)
#     sins = _arg.sin()
#     coss = _arg.cos()
#     zeros = torch.zeros([NUM_RES, 8])
#     ones = torch.ones([NUM_RES, 8])
#     return torch.stack([ones, zeros, zeros, zeros,
#                         zeros, coss, -sins, zeros,
#                         zeros, sins, coss, zeros,
#                         zeros, zeros, zeros, ones], dim=-1).view([NUM_RES, 8, 4, 4])


def make_bb_rt_4x4(rots, trans):
    bb_rt_4x4 = torch.zeros(rots.shape[:-2] + (4, 4), device=rots.device)
    bb_rt_4x4[..., 3, 3] = 1.
    bb_rt_4x4[..., :3, :3] = rots
    bb_rt_4x4[..., :3, 3] = trans
    return bb_rt_4x4


def make_local_rt_4x4(rigid_rt_4x4, torsion_rt_4x4):
    # NUM_RES,8,4,4
    # local_rt_4x4 = copy.deepcopy(rigid_rt_4x4)
    torsion_rt_4x4 = torch.einsum("nmij,nmjk->nmik", rigid_rt_4x4, torsion_rt_4x4)
    torsion_rt_4x4[:, 5] = torch.einsum("nij,njk->nik", torsion_rt_4x4[:, 4], torsion_rt_4x4[:, 5])
    torsion_rt_4x4[:, 6] = torch.einsum("nij,njk->nik", torsion_rt_4x4[:, 5], torsion_rt_4x4[:, 6])
    torsion_rt_4x4[:, 7] = torch.einsum("nij,njk->nik", torsion_rt_4x4[:, 6], torsion_rt_4x4[:, 7])
    return torsion_rt_4x4


def make_global_rt_4x4(bb_rt_4x4, local_rt_4x4):
    return torch.einsum("nij,nmjk->nmik", bb_rt_4x4, local_rt_4x4)


def make_blackhole_pos(aa):
    return default_black_hole_position[aa]


def make_pos(aa, bbrots, bbtrans, sincos):
    blackhole_pos = make_blackhole_pos(aa).to(bbrots.device)
    # print(blackhole_pos.shape)
    bb_rt_4x4 = make_bb_rt_4x4(bbrots, bbtrans)
    local_rt_4x4 = make_local_rt_4x4(default_frame_rt4[aa].to(bbrots.device), make_torsion_rt_4x4_sincos(sincos))
    global_rt_4x4 = make_global_rt_4x4(bb_rt_4x4, local_rt_4x4)
    global_rt_4x4_aa = global_rt_4x4[[torch.arange(len(aa))[:, None].repeat([1, 14]), resid_to_atom_frameid[aa]]]
    # real_pos = torch.einsum("nmij,nmj->nmi", global_rt_4x4_aa, blackhole_pos)
    real_pos = torch.einsum("nmij,nmj->nmi", global_rt_4x4_aa, blackhole_pos)
    return real_pos[..., :3] * (restypeid_to_atommasks[aa].to(bbrots.device)[..., None])


pseudo_beta = torch.tensor([4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], dtype=torch.long)


def pseudo_beta_index(aatype):
    return [torch.arange(len(aatype), dtype=torch.long), pseudo_beta[aatype]]

# print(make_blackhole_pos([19]))
# aa=torch.tensor([19],dtype=torch.long)
# rots=torch.eye(3).float()[None]
# trans=torch.tensor([[0,0,0]])
#
# sincos=torch.rand([1,7,2])
# sincos=sincos/sincos.norm(dim=-1,keepdim=True)
# print(make_pos(aa,rots,trans,sincos))
#

# print(residue_constants.restype3_to_restypeid["VAL"])

# def make_xyz(aa, pos):
#     for resid, (restypeid, pos) in enumerate(zip(aa.tolist(), pos.tolist())):
#         for atomid, atom in enumerate(
#                 residue_constants.restype3_to_atoms[residue_constants.restypeid_to_restype3[restypeid]]):
#             print(atom[0][0], *pos[atomid][:3])
#
