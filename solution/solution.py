from typing import List, Tuple

import numpy as np
import cirq


def matrix_to_sycamore_operations(target_qubits: List[cirq.GridQubit], matrix: np.ndarray) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    """A method to convert a unitary matrix to a list of Sycamore operations.

    This method will return a list of `cirq.Operation`s using the qubits and (optionally) ancilla
    qubits to implement the unitary matrix `matrix` on the target qubits `qubits`.
    The operations are also supported by `cirq.google.gate_sets.SYC_GATESET`.

    Args:
        target_qubits: list of qubits the returned operations will act on. The qubit order defined by the list
            is assumed to be used by the operations to implement `matrix`.
        matrix: a matrix that is guaranteed to be unitary and of size (2**len(qs), 2**len(qs)).
    Returns:
        A tuple of operations and ancilla qubits allocated.
            Operations: In case the matrix is supported, a list of operations `ops` is returned.
                `ops` acts on `qs` qubits and for which `cirq.unitary(ops)` is equal to `matrix` up
                 to certain tolerance. In case the matrix is not supported, it might return NotImplemented to
                 reduce the noise in the judge output.
            Ancilla qubits: In case ancilla qubits are allocated a list of ancilla qubits. Otherwise
                an empty list.
        .
    """
    #number of target qubits
    l = target_qubits
    if isinstance(target_qubits, list):
        qs = len(target_qubits)
    else:
        qs = 1
    
    #check for the input matrix to be unitary
    unitary = cirq.is_unitary(matrix)
    if not(unitary):
        print("Error: Non unitary matrix")
        return NotImplemented, []
    
    #class for the input unitary gate
    class unigate(cirq.Gate):
        def __init__(self, qs, matrix):
            super(unigate, self)
        
        def _num_qubits_(self):
            return qs
        
        def _unitary_(self):
            return matrix
        
        def _circuit_diagram_info_(self, args):
            return "Uni"
    
    #gate with the unitary input matrix
    ug = unigate(qs, matrix)
    
    #we make use of the converter for sycamore gates
    converter = cirq.google.ConvertToSycamoreGates()
    
    #we create the input qubits
    if qs==1:
        converted = converter.convert(ug.on(l[0]))
    elif qs==2:
        converted = converter.convert(ug.on(l[0],l[1]))
    elif qs==3:
        converted = converter.convert(ug.on(l[0],l[1],l[2]))
    elif qs==4:
        converted = converter.convert(ug.on(l[0],l[1],l[2],l[3]))
    elif qs==5:
        converted = converter.convert(ug.on(l[0],l[1],l[2],l[3],l[4]))
    elif qs==6:
        converted = converter.convert(ug.on(l[0],l[1],l[2],l[3],l[4],l[5]))
    elif qs==7:
        converted = converter.convert(ug.on(l[0],l[1],l[2],l[3],l[4],l[5],l[6]))
    elif qs==8:
        converted = converter.convert(ug.on(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]))
    else:
        print("Error in conversion")
        return NotImplemented, []
      
    
    
    return converted, []
