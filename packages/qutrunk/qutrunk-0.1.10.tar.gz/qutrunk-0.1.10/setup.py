# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qutrunk',
 'qutrunk.backends',
 'qutrunk.backends.ibm',
 'qutrunk.backends.qusprout',
 'qutrunk.circuit',
 'qutrunk.circuit.gates',
 'qutrunk.circuit.ops',
 'qutrunk.converters',
 'qutrunk.dagcircuit',
 'qutrunk.example',
 'qutrunk.qasm',
 'qutrunk.qasm.node',
 'qutrunk.sim',
 'qutrunk.sim.local',
 'qutrunk.sim.local.pybind11',
 'qutrunk.sim.local.pybind11.docs',
 'qutrunk.sim.local.pybind11.pybind11',
 'qutrunk.sim.local.pybind11.tests',
 'qutrunk.sim.local.pybind11.tests.extra_python_package',
 'qutrunk.sim.local.pybind11.tests.extra_setuptools',
 'qutrunk.sim.local.pybind11.tests.test_cmake_build',
 'qutrunk.sim.local.pybind11.tests.test_embed',
 'qutrunk.sim.local.pybind11.tools',
 'qutrunk.test',
 'qutrunk.test.gate',
 'qutrunk.tools',
 'qutrunk.visualizations']

package_data = \
{'': ['*'],
 'qutrunk': ['config/*',
             'doc/distribute_package.md',
             'doc/distribute_package.md',
             'doc/project_documentation.md',
             'doc/project_documentation.md'],
 'qutrunk.backends': ['qusprout/idl/*'],
 'qutrunk.qasm': ['libs/*'],
 'qutrunk.sim': ['Release/*',
                 'local/QuEST/*',
                 'local/QuEST/include/*',
                 'local/QuEST/src/*',
                 'local/QuEST/src/CPU/*',
                 'local/QuEST/src/GPU/*',
                 'local/pybind11/docs/_static/*',
                 'local/pybind11/docs/advanced/*',
                 'local/pybind11/docs/advanced/cast/*',
                 'local/pybind11/docs/advanced/pycpp/*',
                 'local/pybind11/docs/cmake/*',
                 'local/pybind11/include/pybind11/*',
                 'local/pybind11/include/pybind11/detail/*',
                 'local/pybind11/include/pybind11/stl/*',
                 'local/pybind11/tests/test_cmake_build/installed_embed/*',
                 'local/pybind11/tests/test_cmake_build/installed_function/*',
                 'local/pybind11/tests/test_cmake_build/installed_target/*',
                 'local/pybind11/tests/test_cmake_build/subdirectory_embed/*',
                 'local/pybind11/tests/test_cmake_build/subdirectory_function/*',
                 'local/pybind11/tests/test_cmake_build/subdirectory_target/*']}

install_requires = \
['networkx>=2.8,<3.0',
 'numpy>=1.22.3,<2.0.0',
 'ply>=3.11,<4.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.27.1,<3.0.0',
 'retworkx>=0.11.0,<0.12.0',
 'thrift>=0.15.0,<0.16.0',
 'thriftpy2>=0.4.14,<0.5.0']

setup_kwargs = {
    'name': 'qutrunk',
    'version': '0.1.10',
    'description': 'qutrunk is an open source library for quantum computing.',
    'long_description': '# qutrunk\n\nqutrunk is a free, open-source and cross-platform Python library for quantum computing. qutrunk also work as a foundation of high-level applications, such as: quantum algorithm, quantum machine learning, quantum composer and so on\n\n## qutrunk features\n\n1. Quantum programming based on quantum circuit and quantum gate.  \n2. Simulate quantum programs on classical computers, provide full amplitude calculation\n3. Device independent, Run the same quantum circuit on various quantum backends(e.g: BackendLocalCpp, BackendLocalPy, BackendQuSprout, BackendIBM, etc.)\n4. Compatible with openqasm/2.0\n5. Provide resource statistics\n\n## Install\n1. Install from whl package, run the following command directly:\n```\npip install qutrunk\n```\n\n2. Install from source code(the cpp simulater BackendLocalCpp will be used as default), run the following command to install qutrunk by source code(see the detailed installation steps xxx):\n```\npython3 setup.py install\n```\n\n## Example:\nbell-pair quantum algorithm：\n\n``` python\n# import package\nfrom qutrunk.circuit import QCircuit\nfrom qutrunk.circuit.gates import H, CNOT, Measure, All\n\n# allocate resource\nqc = QCircuit()\nqr = qc.allocate(2) \n\n# apply quantum gates\nH * qr[0]   \nCNOT * (qr[0], qr[1])\nAll(Measure) * qr\n\n# print circuit\nqc.print(qc)   \n# run circuit\nres = qc.run(shots=1024) \n# print result\nprint(res.get_counts()) \n# draw circuit\nqc.draw()\n```\n\n ## License\n\n qutrunk is free and open source, release under the Apache Licence, Version 2.0.\n',
    'author': 'qudoorzh2022',
    'author_email': 'qudoorzh2022@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.qudoor.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
