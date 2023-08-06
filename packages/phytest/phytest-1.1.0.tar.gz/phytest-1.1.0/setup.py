# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phytest', 'phytest.bio']

package_data = \
{'': ['*'], 'phytest': ['report/*']}

install_requires = \
['biopython>=1.79,<2.0',
 'numpy>=1.22.3,<2.0.0',
 'phylo-treetime>=0.8.6,<0.9.0',
 'pytest-html>=3.1.1,<4.0.0',
 'pytest-sugar>=0.9.4,<0.10.0',
 'pytest>=7.1.1,<8.0.0',
 'scipy>=1.8.0,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['phytest = phytest.cli:app'],
 'pytest11': ['phytest = phytest']}

setup_kwargs = {
    'name': 'phytest',
    'version': '1.1.0',
    'description': 'Quality control for phylogenetic pipelines using pytest',
    'long_description': '.. image:: https://raw.githubusercontent.com/phytest-devs/phytest/main/docs/images/logo.png\n  :alt: Phytest logo\n\n.. start-badges\n\n|pypi badge| |tests badge| |coverage badge| |docs badge| |black badge| |pre-commit badge| |doi badge|\n\n\n.. |pypi badge| image:: https://img.shields.io/pypi/v/phytest.svg\n    :target: https://pypi.org/project/phytest/\n\n.. |tests badge| image:: https://github.com/phytest-devs/phytest/workflows/tests/badge.svg\n    :target: https://github.com/phytest-devs/phytest/actions\n\n.. |docs badge| image:: https://github.com/phytest-devs/phytest/workflows/docs/badge.svg\n    :target: https://phytest-devs.github.io/phytest/\n\n.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/smutch/e8160655e03d9015b1e93b97ed611f4f/raw/coverage-badge.json\n    :target: https://phytest-devs.github.io/phytest/coverage/\n\n.. |pre-commit badge| image:: https://results.pre-commit.ci/badge/github/phytest-devs/phytest/main.svg\n    :target: https://results.pre-commit.ci/latest/github/phytest-devs/phytest/main\n\n.. |doi badge| image:: https://img.shields.io/badge/DOI-10.21203%2Frs.3.rs1903486%2Fv1-success.svg\n    :target: https://www.researchsquare.com/article/rs-1903486/v1\n\n.. end-badges\n\n\n\nPhytest: Quality Control for Phylogenetic Analyses.\n\n----\n\nDocumentation: https://phytest-devs.github.io/phytest\n\nCode: https://github.com/phytest-devs/phytest\n\nTutorials: https://github.com/phytest-devs?q=example\n\n----\n\n.. start-quickstart\n\nInstallation\n============\nInstall phytest using pip:\n\n.. code-block:: bash\n\n    pip install phytest\n\n\nQuick Start\n============\n\nPhytest is a tool for automating quality control checks on sequence, tree and metadata files during phylogenetic analyses.\nPhytest ensures that phylogenetic analyses meet user-defined quality control tests.\n\nHere we will create example data files to run our tests on.\n\nCreate an alignment fasta file :code:`example.fasta`\n\n.. code-block:: text\n\n    >Sequence_A\n    ATGAGATCCCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG\n    >Sequence_B\n    ATGAGATCCCCGATAGCGAGCTAGXGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG\n    >Sequence_C\n    ATGAGA--CCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG\n    >Sequence_D\n    ATGAGATCCCCGATAGCGAGCTAGCGATNNNNNNNNNNNNNNNNNTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG\n\nCreate a tree newick file :code:`example.tree`\n\n.. code-block:: text\n\n    (Sequence_A:1,Sequence_B:0.2,(Sequence_C:0.3,Sequence_D:0.4):0.5);\n\nWriting a test file\n########################\n\nWe want to enforce the follow constraints on our data:\n    1. The alignment has 4 sequences\n    2. The sequences have a length of 100\n    3. The sequences only contains the characters A, T, G, C, N and -\n    4. The sequences are allowed to only contain single base deletions\n    5. The longest stretch of Ns is 10\n    6. The tree has 4 tips\n    7. The tree is bifurcating\n    8. The alignment and tree have the same names\n    9. All internal branches are longer than the given threshold\n    10. There are no outlier branches in the tree\n\nWe can write these tests in a python files :code:`example.py`\n\n.. code-block:: python\n\n    from phytest import Alignment, Sequence, Tree\n\n\n    def test_alignment_has_4_sequences(alignment: Alignment):\n        alignment.assert_length(4)\n\n\n    def test_alignment_has_a_width_of_100(alignment: Alignment):\n        alignment.assert_width(100)\n\n\n    def test_sequences_only_contains_the_characters(sequence: Sequence):\n        sequence.assert_valid_alphabet(alphabet="ATGCN-")\n\n\n    def test_single_base_deletions(sequence: Sequence):\n        sequence.assert_longest_stretch_gaps(max=1)\n\n\n    def test_longest_stretch_of_Ns_is_10(sequence: Sequence):\n        sequence.assert_longest_stretch_Ns(max=10)\n\n\n    def test_tree_has_4_tips(tree: Tree):\n        tree.assert_number_of_tips(4)\n\n\n    def test_tree_is_bifurcating(tree: Tree):\n        tree.assert_is_bifurcating()\n\n\n    def test_aln_tree_match_names(alignment: Alignment, tree: Tree):\n        aln_names = [i.name for i in alignment]\n        tree.assert_tip_names(aln_names)\n\n\n    def test_all_internal_branches_lengths_above_threshold(tree: Tree, threshold=1e-4):\n        tree.assert_internal_branch_lengths(min=threshold)\n\n\n    def test_outlier_branches(tree: Tree):\n        # Here we create a custom function to detect outliers\n        import statistics\n\n        tips = tree.get_terminals()\n        branch_lengths = [t.branch_length for t in tips]\n        cut_off = statistics.mean(branch_lengths) + statistics.stdev(branch_lengths)\n        for tip in tips:\n            assert tip.branch_length < cut_off, f"Outlier tip \'{tip.name}\' (branch length = {tip.branch_length})!"\n\nRunning Phytest\n################\n\nWe can then run these tests on our data with :code:`phytest`:\n\n.. code-block:: bash\n\n    phytest examples/example.py -s examples/data/example.fasta -t examples/data/example.tree\n\nGenerate a report by adding :code:`--report report.html`.\n\n.. image:: https://raw.githubusercontent.com/phytest-devs/phytest/main/docs/images/report.png\n    :alt: HTML Report\n\nFrom the output we can see several tests failed:\n\n.. code-block::\n\n    FAILED examples/example.py::test_sequences_only_contains_the_characters[Sequence_B] - AssertionError: Invalid pattern found in \'Sequence_B\'!\n    FAILED examples/example.py::test_single_base_deletions[Sequence_C] - AssertionError: Longest stretch of \'-\' in \'Sequence_C\' > 1!\n    FAILED examples/example.py::test_longest_stretch_of_Ns_is_10[Sequence_D] - AssertionError: Longest stretch of \'N\' in \'Sequence_D\' > 10!\n    FAILED examples/example.py::test_outlier_branches - AssertionError: Outlier tip \'Sequence_A\' (branch length = 1.0)!\n\n    Results (0.07s):\n        15 passed\n        4 failed\n            - examples/example.py:12 test_sequences_only_contains_the_characters[Sequence_B]\n            - examples/example.py:16 test_single_base_deletions[Sequence_C]\n            - examples/example.py:20 test_longest_stretch_of_Ns_is_10[Sequence_D]\n            - examples/example.py:32 test_outlier_branches\n\n.. end-quickstart\n\nSee docs for more information https://phytest-devs.github.io/phytest.\n',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
