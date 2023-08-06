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
from .._definitions.types cimport LongIndexType, DataType
from .._c_linear_algebra.c_matrix_decompositions cimport cMatrixDecompositions

# To avoid cython's bug that does not recognizes "long double" in template []
ctypedef long double long_double

__all__ = ['orthogonalize']


# =============
# orthogonalize
# =============

cpdef orthogonalize(A):
    """
    Orthogonalizes the columns of matrix.

    Parameters
    ----------
        A : array_like
            Input matrix. This matrix will be overwritten in place of the
            output orthogonal matrix.

    Warnings
    --------
        The input matrix will be overwritten inplace.

    Notes
    -----

    The Gram-Schmidt method is used to orthogonalize the columns of the input
    matrix.
    """

    data_type_name = get_data_type_name(A)

    if data_type_name == b'float32':
        _pyc_gram_schmidt_float(A, A.shape[0], A.shape[1])
    elif data_type_name == b'float64':
        _pyc_gram_schmidt_double(A, A.shape[0], A.shape[1])
    elif data_type_name == b'float128':
        _pyc_gram_schmidt_long_double(A, A.shape[0], A.shape[1])
    else:
        raise TypeError('Data type should be "float32", "float64", or ' +
                        '"float128".')


# ======================
# pyc gram schmidt float
# ======================

cdef void _pyc_gram_schmidt_float(
        float[:, ::1] A,
        const LongIndexType num_rows,
        const LongIndexType num_columns) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    float type.
    """

    # Get c-pointer from memoryviews
    cdef float* c_A = &A[0, 0]

    cMatrixDecompositions[float].gram_schmidt(c_A, num_rows, num_columns)


# =======================
# pyc gram schmidt double
# =======================

cdef void _pyc_gram_schmidt_double(
        double[:, ::1] A,
        const LongIndexType num_rows,
        const LongIndexType num_columns) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    double type.
    """

    # Get c-pointer from memoryviews
    cdef double* c_A = &A[0, 0]

    cMatrixDecompositions[double].gram_schmidt(c_A, num_rows, num_columns)


# ============================
# pyc gram schmidt long double
# ============================

cdef void _pyc_gram_schmidt_long_double(
        long double[:, ::1] A,
        const LongIndexType num_rows,
        const LongIndexType num_columns) except *:
    """
    Gram-Schmidt orthogonalization of the columns of a matrix, specialized for
    long double type.
    """

    # Get c-pointer from memoryviews
    cdef long double* c_A = &A[0, 0]

    cMatrixDecompositions[long_double].gram_schmidt(c_A, num_rows, num_columns)
