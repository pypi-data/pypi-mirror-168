# qutrunk

qutrunk is a free, open-source and cross-platform Python library for quantum computing. qutrunk also work as a foundation of high-level applications, such as: quantum algorithm, quantum machine learning, quantum composer and so on

## qutrunk features

1. Quantum programming based on quantum circuit and quantum gate.  
2. Simulate quantum programs on classical computers, provide full amplitude calculation
3. Device independent, Run the same quantum circuit on various quantum backends(e.g: BackendLocalCpp, BackendLocalPy, BackendQuSprout, BackendIBM, etc.)
4. Compatible with openqasm/2.0
5. Provide resource statistics

## Install
1. Install from whl package, run the following command directly:
```
pip install qutrunk
```

2. Install from source code(the cpp simulater BackendLocalCpp will be used as default), run the following command to install qutrunk by source code(see the detailed installation steps xxx):
```
python3 setup.py install
```

## Example:
bell-pair quantum algorithm：

``` python
# import package
from qutrunk.circuit import QCircuit
from qutrunk.circuit.gates import H, CNOT, Measure, All

# allocate resource
qc = QCircuit()
qr = qc.allocate(2) 

# apply quantum gates
H * qr[0]   
CNOT * (qr[0], qr[1])
All(Measure) * qr

# print circuit
qc.print(qc)   
# run circuit
res = qc.run(shots=1024) 
# print result
print(res.get_counts()) 
# draw circuit
qc.draw()
```

 ## License

 qutrunk is free and open source, release under the Apache Licence, Version 2.0.
