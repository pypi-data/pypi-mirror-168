import torch
import copy


def rigid_rots_trans(input: torch.Tensor):
    # *n-ca-c,x-y-z
    n_, ca, c_ = input[..., 0, :], input[..., 1, :], input[..., 2, :]
    trans = ca
    n_ = n_ - ca
    c = c_ - ca
    c_xy_norm = c[..., :2].norm(dim=-1) + 1E-10
    cos_c1 = c[..., 0] / c_xy_norm

    sin_c1 = -c[..., 1] / c_xy_norm
    rots1 = torch.zeros([*cos_c1.shape, 3, 3])
    rots1[..., 0, 0] = cos_c1
    rots1[..., 0, 1] = -sin_c1
    rots1[..., 1, 0] = sin_c1
    rots1[..., 1, 1] = cos_c1
    rots1[..., 2, 2] = 1.
    c_xyz_norm = c.norm(dim=-1) + 1E-10
    sin_c2 = c[..., 2] / c_xyz_norm
    cos_c2 = c_xy_norm / c_xyz_norm
    rots2 = torch.zeros([*cos_c1.shape, 3, 3])
    rots2[..., 0, 0] = cos_c2
    rots2[..., 0, 2] = sin_c2
    rots2[..., 1, 1] = 1
    rots1[..., 2, 0] = -sin_c2
    rots1[..., 2, 2] = cos_c2
    rots_c = torch.einsum("...ij,...jk->...ik", rots2, rots1)
    n = torch.einsum("...ik,...k->...i", rots_c, n_)
    n_yz_norm = n[..., 1:].norm(dim=-1) + 1E-10
    sin_n = -n[..., 2] / n_yz_norm
    cos_n = n[..., 1] / n_yz_norm
    rots_n = torch.zeros([*cos_c1.shape, 3, 3])
    rots_n[..., 0, 0] = 1.
    rots_n[..., 1, 1] = cos_n
    rots_n[..., 1, 2] = -sin_n
    rots_n[..., 2, 1] = sin_n
    rots_n[..., 2, 2] = cos_n
    rots = torch.einsum("...ij,...jk->...ik", rots_n, rots_c).transpose(-1, -2)
    # print(rots)
    return rots, trans


def rigid_vec(input_xyz):
    rots, trans = rigid_rots_trans(input_xyz)
    pts = trans[..., None, :, :] - trans[..., None, :]
    return torch.einsum("...ij,...j->...i", rots[..., None, :, :].transpose(-1, -2), pts)


def rots_to_quats(rots):
    rot = [[rots[..., i, j] for j in range(3)] for i in range(3)]
    [[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]] = rot

    k = [
        [xx + yy + zz, zy - yz, xz - zx, yx - xy, ],
        [zy - yz, xx - yy - zz, xy + yx, xz + zx, ],
        [xz - zx, xy + yx, yy - xx - zz, yz + zy, ],
        [yx - xy, xz + zx, yz + zy, zz - xx - yy, ]
    ]
    k = (1. / 3.) * torch.stack([torch.stack(t, dim=-1) for t in k], dim=-2)
    _, vectors = torch.linalg.eigh(k)
    return vectors[..., -1]


_QUAT_MULTIPLY_BY_VEC = torch.tensor([[[0., 1., 0., 0.],
                                       [0., 0., 1., 0.],
                                       [0., 0., 0., 1.]],
                                      [[-1., 0., 0., 0.],
                                       [0., 0., 0., 1.],
                                       [0., 0., -1., 0.]],
                                      [[0., 0., 0., -1.],
                                       [-1., 0., 0., 0.],
                                       [0., 1., 0., 0.]],
                                      [[0., 0., 1., 0.],
                                       [0., -1., 0., 0.],
                                       [-1., 0., 0., 0.]]])

_QTR_MAT=[[[[ 1.,  0.,  0.],
   [ 0. , 1. , 0.],
   [ 0. , 0. , 1.]],

  [[ 0.,  0.,  0.],
   [ 0. , 0., -2.],
   [ 0. , 2. , 0.]],

  [[ 0. , 0. , 2.],
   [ 0. , 0. , 0.],
   [-2. , 0. , 0.]],

  [[ 0. ,-2. , 0.],
   [ 2.,  0. , 0.],
   [ 0.,  0. , 0.]]],


 [[[ 0. , 0. , 0.],
   [ 0. , 0.,  0.],
   [ 0.,  0. , 0.]],

  [[ 1. , 0.  ,0.],
   [ 0., -1. , 0.],
   [ 0. , 0. ,-1.]],

  [[ 0. , 2.,  0.],
   [ 2. , 0. , 0.],
   [ 0. , 0. , 0.]],

  [[ 0. , 0.,  2.],
   [ 0. , 0.,  0.],
   [ 2. , 0.  ,0.]]],


 [[[ 0. , 0.,  0.],
   [ 0. , 0. , 0.],
   [ 0. , 0.,  0.]],

  [[ 0.,  0. , 0.],
   [ 0. , 0.,  0.],
   [ 0.,  0. , 0.]],

  [[-1. , 0. , 0.],
   [ 0.  ,1.,  0.],
   [ 0. , 0., -1.]],

  [[ 0. , 0.,  0.],
   [ 0. , 0.,  2.],
   [ 0. , 2. , 0.]]],


 [[[ 0.,  0.,  0.],
   [ 0. , 0. , 0.],
   [ 0. , 0. , 0.]],

  [[ 0.  ,0. , 0.],
   [ 0. , 0. , 0.],
   [ 0. , 0.  ,0.]],

  [[ 0. , 0. , 0.],
   [ 0. , 0.,  0.],
   [ 0. , 0. , 0.]],

  [[-1. , 0.,  0.],
   [ 0. ,-1.  ,0.],
   [ 0. , 0. , 1.]]]]




def quats_multiply_by_vecs(quats, vecs):
    mat = _QUAT_MULTIPLY_BY_VEC.to(quats.device)
    return torch.einsum("abc,...a,...b->...c", mat, quats, vecs)


def quats_to_rots(quats: torch.Tensor) -> torch.Tensor:
    """
        Converts a quaternion to a rotation matrix.

        Args:
            quat: [*, 4] quaternions
        Returns:
            [*, 3, 3] rotation matrices
    """
    # [*, 4, 4]
    quats=quats/quats.norm(dim=-1,keepdim=True)
    quat = quats[..., None] * quats[..., None, :]

    # [4, 4, 3, 3]
    mat = quat.new_tensor(_QTR_MAT)

    # [*, 4, 4, 3, 3]
    shaped_qtr_mat = mat.view((1,) * len(quat.shape[:-2]) + mat.shape)
    quat = quat[..., None, None] * shaped_qtr_mat

    # [*, 3, 3]
    return torch.sum(quat, dim=(-3, -4))


def updateRTbyBB(rots, trans, BB):
    Q, V = BB[..., :3], BB[..., 3:]
    quats = rots_to_quats(rots)
    new_quats = quats + quats_multiply_by_vecs(quats, Q)
    new_rots = quats_to_rots(new_quats)
    new_trans = trans + torch.einsum("...ij,...j->...i", rots, V)
    return new_rots, new_trans
