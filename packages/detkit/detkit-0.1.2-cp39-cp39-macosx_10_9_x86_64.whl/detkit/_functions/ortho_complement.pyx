# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

from ._utilities import get_data_type_name
from .._definitions.types cimport LongIndexType, DataType, FlagType
from .._c_linear_algebra.c_matrix_decompositions cimport cMatrixDecompositions

# To avoid cython's bug that does not recognizes "long double" in template []
ctypedef long double long_double

__all__ = ['ortho_complement']


# ================
# ortho complement
# ================

cpdef ortho_complement(Xp, X, X_orth):
    """
    Orthogonalizes the columns of matrix `Xp` against `X`.

    Parameters
    ----------
        Xp : array_like
            Output matrix. This matrix will be overwritten in place of the
            output orthogonal matrix. `X` and `Xp` must have the same number
            of rows, but they can have different number of columns.
        X : array_like
            Input matrix.
        X_orth: boolean
            Determines whether `X` is already orthonormalized or not.

    Warnings
    --------
        The input matrix will be overwritten inplace.

    Notes
    -----

    The Gram-Schmidt method is used to orthogonalize the columns of the matrix.
    """

    data_type_name = get_data_type_name(X)

    if data_type_name == b'float32':
        _pyc_ortho_complement_float(Xp, X, X.shape[0], Xp.shape[1], X.shape[1],
                                    int(X_orth))
    elif data_type_name == b'float64':
        _pyc_ortho_complement_double(Xp, X, X.shape[0], Xp.shape[1],
                                     X.shape[1], int(X_orth))
    elif data_type_name == b'float128':
        _pyc_ortho_complement_long_double(Xp, X, X.shape[0], Xp.shape[1],
                                          X.shape[1], int(X_orth))
    else:
        raise TypeError('Data type should be "float32", "float64", or ' +
                        '"float128".')


# =========================
# pyc orth complement float
# =========================

cdef void _pyc_ortho_complement_float(
        float[:, ::1] Xp,
        float[:, ::1] X,
        const LongIndexType num_rows,
        const LongIndexType num_columns_Xp,
        const LongIndexType num_columns_X,
        const FlagType X_orth,) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    float type.
    """

    # Get c-pointer from memoryviews
    cdef float* c_Xp = &Xp[0, 0]
    cdef float* c_X = &X[0, 0]

    cMatrixDecompositions[float].ortho_complement(
            c_Xp, c_X, num_rows, num_columns_Xp, num_columns_X, X_orth)


# ===========================
# pyc ortho complement double
# ===========================

cdef void _pyc_ortho_complement_double(
        double[:, ::1] Xp,
        double[:, ::1] X,
        const LongIndexType num_rows,
        const LongIndexType num_columns_Xp,
        const LongIndexType num_columns_X,
        const FlagType X_orth) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    double type.
    """

    # Get c-pointer from memoryviews
    cdef double* c_Xp = &Xp[0, 0]
    cdef double* c_X = &X[0, 0]

    cMatrixDecompositions[double].ortho_complement(
            c_Xp, c_X, num_rows, num_columns_Xp, num_columns_X, X_orth)


# ================================
# pyc ortho complement long double
# ================================

cdef void _pyc_ortho_complement_long_double(
        long double[:, ::1] Xp,
        long double[:, ::1] X,
        const LongIndexType num_rows,
        const LongIndexType num_columns_Xp,
        const LongIndexType num_columns_X,
        const FlagType X_orth) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    long double type.
    """

    # Get c-pointer from memoryviews
    cdef long double* c_Xp = &Xp[0, 0]
    cdef long double* c_X = &X[0, 0]

    cMatrixDecompositions[long_double].ortho_complement(
            c_Xp, c_X, num_rows, num_columns_Xp, num_columns_X, X_orth)
