# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Classical energies."""
# pylint: disable=duplicate-code

import numpy as np
from pyscf import gto, scf, mp, ao2mo, fci

from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.properties.second_quantization.electronic.bases import (
    ElectronicBasis,
)
from qiskit_nature.drivers.second_quantization import ElectronicStructureDriver

from entanglement_forging.core.cholesky_hamiltonian import (
    get_fermionic_ops_with_cholesky,
)
from entanglement_forging.core.orbitals_to_reduce import OrbitalsToReduce


# pylint: disable=invalid-name
class ClassicalEnergies:  # pylint: disable=too-many-instance-attributes disable=too-few-public-methods
    """Runs classical energy computations.

    Attributes:
        HF (float) = Hartree Fock energy
        MP2 (float) = MP2 Energy
        FCI (float) = Full Configuration Interaction energy
        shift (float) = The sum of the nuclear repulsion energy
                        and the energy shift due to orbital freezing
    """

    def __init__(self, problem: ElectronicStructureProblem, all_orbitals_to_reduce):
        """Initialize the classical energies.
        Args:
            qmolecule (ElectronicStructureProblem): Problem class containing molecule driver
            all_to_reduce (entanglement_forging.core.orbitals_to_reduce.OrbitalsToReduce):
                All orbitals to be reduced.
        """
        # pylint: disable=too-many-locals disable=too-many-statements
        self.problem = problem

        self.all_orbitals_to_reduce = all_orbitals_to_reduce
        self.orbitals_to_reduce = OrbitalsToReduce(self.all_orbitals_to_reduce, problem)
        self.epsilon_cholesky = 1e-10

        if isinstance(problem.driver, ElectronicStructureDriver):
            particle_number = self.problem.grouped_property.get_property(
                "ParticleNumber"
            )
            electronic_basis_transform = self.problem.grouped_property.get_property(
                "ElectronicBasisTransform"
            )
            electronic_energy = self.problem.grouped_property.get_property(
                "ElectronicEnergy"
            )

            num_alpha = particle_number.num_alpha
            num_beta = particle_number.num_beta
            mo_coeff = electronic_basis_transform.coeff_alpha
            hcore = electronic_energy.get_electronic_integral(
                ElectronicBasis.AO, 1
            )._matrices[0]
            eri = electronic_energy.get_electronic_integral(
                ElectronicBasis.AO, 2
            )._matrices[0]

            num_molecular_orbitals = mo_coeff.shape[0]

            nuclear_repulsion_energy = electronic_energy.nuclear_repulsion_energy

        else:
            hcore = problem.driver._hcore
            mo_coeff = problem.driver._mo_coeff
            eri = problem.driver._eri
            num_alpha = problem.driver._num_alpha
            num_beta = problem.driver._num_beta
            nuclear_repulsion_energy = problem.driver._nuclear_repulsion_energy
            num_molecular_orbitals = mo_coeff.shape[0]

        n_electrons = num_molecular_orbitals - len(self.orbitals_to_reduce.all)

        n_alpha_electrons = num_alpha - len(self.orbitals_to_reduce.occupied())
        n_beta_electrons = num_beta - len(self.orbitals_to_reduce.occupied())

        fermionic_op = get_fermionic_ops_with_cholesky(
            mo_coeff,
            hcore,
            eri,
            opname="H",
            halve_transformed_h2=True,
            occupied_orbitals_to_reduce=self.orbitals_to_reduce.occupied(),
            virtual_orbitals_to_reduce=self.orbitals_to_reduce.virtual(),
            epsilon_cholesky=self.epsilon_cholesky,
        )
        # hi - 2D array representing operator coefficients of one-body integrals in the AO basis.
        _, _, freeze_shift, h1, h2 = fermionic_op
        Enuc = freeze_shift + nuclear_repulsion_energy
        # 4D array representing operator coefficients of two-body integrals in the AO basis.
        h2 = 2 * h2
        mol_FC = gto.M(verbose=0)
        mol_FC.charge = 0
        mol_FC.nelectron = n_alpha_electrons + n_beta_electrons
        mol_FC.spin = n_alpha_electrons - n_beta_electrons
        mol_FC.incore_anyway = True
        mf_FC = scf.RHF(mol_FC)
        mf_FC.get_hcore = lambda *args: h1
        mf_FC.get_ovlp = lambda *args: np.eye(n_electrons)

        mf_FC._eri = ao2mo.restore(8, h2, n_electrons)
        rho = np.zeros((n_electrons, n_electrons))
        for i in range(n_alpha_electrons):
            rho[i, i] = 2.0

        Ehf = mf_FC.kernel(rho)
        ci_FC = fci.FCI(mf_FC)
        Emp = mp.MP2(mf_FC).kernel()[0]
        Efci, _ = ci_FC.kernel()

        self.HF = Ehf
        self.MP2 = Ehf + Emp
        self.FCI = Efci
        self.shift = Enuc
