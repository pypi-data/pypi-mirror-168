import numpy as np
from quantumsymmetry.core import apply_encoding, get_character_table, HartreeFock_ket, find_ground_state_irrep, get_molecule_name, make_clifford_tableau, find_symmetry_generators
from openfermion import QubitOperator, FermionOperator, jordan_wigner, utils, linalg
from qiskit import opflow, quantum_info
from qiskit_nature.operators.second_quantization import FermionicOp
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit.circuit.quantumcircuit import QuantumCircuit
from pyscf import gto, scf, symm, ao2mo

def apply_encoding_mapper(operator, suppress_none=True):
    apply_encoding(operator = operator, encoding = SymmetryAdaptedEncoding_encoding, output_format = 'qiskit')

def convert_encoding(operators, suppress_none=True, check_commutes=False, num_particles=None, sector_locator=None):
    if type(operators) == FermionicOp:
        operator = operators
        output = 0
        operator = fix_qubit_order_convention(operator)
        encoded_operator = apply_encoding(operator = operator, encoding = SymmetryAdaptedEncoding_encoding, output_format = 'qiskit')
        if type(encoded_operator) != int and type(encoded_operator) != None:
            output = encoded_operator
    elif type(operators) == list:
        output = list()
        for operator in operators:
            operator = fix_qubit_order_convention(operator)
            encoded_operator = apply_encoding(operator = operator, encoding = SymmetryAdaptedEncoding_encoding, output_format = 'qiskit')
            if type(encoded_operator) != int and type(encoded_operator) != None:
                output.append(encoded_operator)
    return output

def transform(driver, operators):
    output1 = driver
    output2 = list()
    if operators == None:
        return output1, None
    for operator in operators:
        operator = fix_qubit_order_convention(operator)
        encoded_operator = apply_encoding(operator = operator, encoding = SymmetryAdaptedEncoding_encoding, output_format = 'qiskit')
        if type(encoded_operator) != int and type(encoded_operator) != None:
            output2.append(encoded_operator)
    return output1, output2

def fix_qubit_order_convention(input):
    output = 0
    input.display_format="dense"
    N = input.register_length
    input_list = input.to_list()
    for x in range(len(input_list)):
        output_label = str()
        input_label = input_list[x][0]
        input_label = input_label[::-1]
        for j in range(N//2):
            output_label += input_label[j]
            output_label += input_label[N//2 + j]
        output += FermionicOp([(output_label[::-1], input_list[x][1])], display_format='dense')
    return output
    
def SymmetryAdaptedEncodingQubitConverter(encoding):
    global SymmetryAdaptedEncoding_encoding
    SymmetryAdaptedEncoding_encoding = encoding
    qubit_transformation = QubitConverter(apply_encoding_mapper)
    qubit_transformation.convert_match = convert_encoding
    qubit_transformation.mapper.map = apply_encoding_mapper
    qubit_transformation.convert = convert_encoding
    return qubit_transformation

def SymmetryAdaptedEncodingHartreeFock(atom, basis, charge = 0, spin = 0, irrep = None):
    mol = gto.Mole()
    mol.atom = atom
    mol.symmetry = True
    mol.basis = basis
    mol.charge = charge
    mol.spin = spin
    mol.verbose = 0
    mol.build()
    if mol.groupname == 'Dooh' or mol.groupname == 'SO3':
        mol.symmetry = 'D2h'
        mol.build()
    if mol.groupname == 'Coov':
        mol.symmetry = 'C2v'
        mol.build()
    mf = scf.RHF(mol)
    mf.kernel()
    
    label_orb_symm = symm.label_orb_symm(mol, mol.irrep_name, mol.symm_orb, mf.mo_coeff)
    character_table, conj_labels, irrep_labels, conj_descriptions = get_character_table(mol.groupname)
    if irrep == None:
        irrep =  find_ground_state_irrep(label_orb_symm, mf.mo_occ, character_table, irrep_labels)
    molecule_name = get_molecule_name(mol)
    symmetry_generator_labels, symmetry_generators_strings, target_qubits, symmetry_generators, signs, descriptions = find_symmetry_generators(mol, mf, irrep)
    tableau, tableau_signs = make_clifford_tableau(symmetry_generators, signs, target_qubits)

    n = len(tableau)//2
    ZZ_block = (-tableau[:n, :n] + 1)//2
    sign_vector = (-tableau_signs[:n]+ 1)//2
    b = HartreeFock_ket(mf.mo_occ)
    string_b = f'{b:0{n}b}'
    b_list = list(string_b)[::-1]
    for i in range(len(b_list)):
        b_list[i] = int(b_list[i])
    c_list = np.matmul(ZZ_block, b_list + sign_vector)[::-1] % 2
    string_c = ''.join(str(x) for x in c_list)
    target_qubits.sort(reverse = True)
    for qubit in target_qubits:
        l = len(string_c)
        string_c = string_c[:l - qubit - 1] + string_c[l - qubit:]
    
    output = QuantumCircuit(len(string_c))
    for i, bit in enumerate(string_c[::-1]):
        if bit == '1':
            output.x(i)
    return output

from itertools import combinations
from qiskit_nature.operators.second_quantization import FermionicOp

def swap_plus_and_minuses(input):
    output = str()
    for s in input:
        if s == '+':
            output += '-'
        elif s == '-':
            output += '+'
        else:
            output += s
    return output

def make_fermionic_excitation_ops(reference_state):
    number_of_qubits = len(reference_state)
    occ = []
    unocc = []
    reference_state = list(reference_state)
    reference_state.reverse()

    #get occupations
    for i, x in enumerate(reference_state):
        if x == '0':
            unocc.append(i)
        if x == '1':
            occ.append(i)
    print(unocc)
    print(occ)

    #singles
    operators_s = []
    for perm_plus in list(combinations(occ, 1)):
        for perm_minus in list(combinations(unocc, 1)):
            if len(set(perm_plus).union(set(perm_minus))) == 2:
                operator = ['I']*number_of_qubits
                for i in perm_plus:
                    operator[i] = '+'
                for i in perm_minus:
                    operator[i] = '-'
                operator = ''.join(operator)
                operators_s.append(operator)

    #doubles
    operators_d = []
    for perm_plus in list(combinations(occ, 2)):
        for perm_minus in list(combinations(unocc, 2)):
            operator = ['I']*number_of_qubits
            for i in perm_plus:
                operator[i] = '+'
            for i in perm_minus:
                operator[i] = '-'
            operator = ''.join(operator)
            operators_d.append(operator)
    
    #create fermionic operators
    operators2 = []
    for operator in operators_s:
        excitation = FermionicOp([(operator, 1j), (swap_plus_and_minuses(operator), 1j)], register_length = number_of_qubits, display_format='dense')
        if excitation not in operators2:
            operators2.append(excitation)

    for operator in operators_d:
        excitation = FermionicOp([(operator, 1j), (swap_plus_and_minuses(operator), -1j)], register_length = number_of_qubits, display_format='dense')
        if excitation not in operators2:
            operators2.append(excitation)

    return operators2

def make_excitation_ops(reference_state, encoding):
    operators = []
    excitations = make_fermionic_excitation_ops(reference_state)
    for excitation in excitations:
        op = apply_encoding(encoding = encoding, operator = excitation, output_format = 'qiskit')
        operators.append(op)
    return operators