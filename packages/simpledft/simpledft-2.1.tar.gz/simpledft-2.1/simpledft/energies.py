import math

import numpy as np


def get_E(scf):
    '''Calculate energy contributions.
    Thesis: Eq. 2.49
    '''
    Ekin = get_Ekin(scf.atoms, scf.op, scf.Y)
    Ecoul = get_Ecoul(scf.op, scf.n, scf.phi)
    Exc = get_Exc(scf.op, scf.n, scf.exc)
    Een = get_Een(scf.n, scf.pot)
    return Ekin + Ecoul + Exc + Een + scf.Eewald


def get_Ekin(atoms, op, W):
    '''Calculate the kinetic energy.
    Thesis: Eq. 2.37
    '''
    F = np.diag(atoms.f)
    T = -0.5 * np.trace(F @ (W.conj().T @ op.L(W)))
    return np.real(T)


def get_Ecoul(op, n, phi):
    '''Calculate the Coulomb energy.
    Thesis: Eq. 2.40 + Eq. 2.41 (as in Eq. 2.49)
    '''
    Ecoul = 0.5 * n.conj().T @ op.Jdag(op.O(phi))
    return np.real(Ecoul)


def get_Exc(op, n, exc):
    '''Calculate the exchange-correlation energy.
    Thesis: Eq. 2.39
    '''
    Exc = n.conj().T @ op.Jdag(op.O(op.J(exc)))
    return np.real(Exc)


def get_Een(n, Vreciproc):
    '''Calculate the electron-ion interaction.
    Thesis: Eq. 2.38
    '''
    Een = Vreciproc.conj().T @ n
    return np.real(Een)


def get_Eewald(atoms, gcut=2, gamma=1e-8):
    '''Calculate the Ewald energy.
    Thesis: Eq. A.12 ff.
    '''
    def get_index_vectors(s):
        m1 = np.arange(-s[0], s[0] + 1)
        m2 = np.arange(-s[1], s[1] + 1)
        m3 = np.arange(-s[2], s[2] + 1)
        M = np.transpose(np.meshgrid(m1, m2, m3)).reshape(-1, 3)
        return M[~np.all(M == 0, axis=1)]

    gexp = -np.log(gamma)
    nu = 0.5 * np.sqrt(gcut**2 / gexp)

    Eewald = -nu / np.sqrt(np.pi) * np.sum(atoms.Z**2)
    Eewald += -np.pi * np.sum(atoms.Z)**2 / (2 * nu**2 * atoms.Omega)

    Rm = np.linalg.norm(atoms.R, axis=1)
    tmax = np.sqrt(0.5 * gexp) / nu
    s = np.rint(tmax / Rm + 1.5)
    M = get_index_vectors(s)
    T = M @ atoms.R

    for ia in range(atoms.Natoms):
        for ja in range(atoms.Natoms):
            dX = atoms.X[ia] - atoms.X[ja]
            ZiZj = atoms.Z[ia] * atoms.Z[ja]
            for t in T:
                rmag = np.sqrt(np.linalg.norm(dX - T)**2)
                Eewald += 0.5 * ZiZj * math.erfc(rmag * nu) / rmag
            if ia != ja:
                rmag = np.sqrt(np.linalg.norm(dX)**2)
                Eewald += 0.5 * ZiZj * math.erfc(rmag * nu) / rmag

    g = 2 * np.pi * np.linalg.inv(atoms.R.T)
    gm = np.linalg.norm(g, axis=1)
    s = np.rint(gcut / gm + 1.5)
    M = get_index_vectors(s)
    G = M @ g
    G2 = np.linalg.norm(G, axis=1)**2
    prefactor = 2 * np.pi / atoms.Omega * np.exp(-0.25 * G2 / nu**2) / G2

    for ia in range(atoms.Natoms):
        for ja in range(atoms.Natoms):
            dX = atoms.X[ia] - atoms.X[ja]
            ZiZj = atoms.Z[ia] * atoms.Z[ja]
            GX = np.sum(G * dX, axis=1)
            Eewald += ZiZj * np.sum(prefactor * np.cos(GX))
    return Eewald
