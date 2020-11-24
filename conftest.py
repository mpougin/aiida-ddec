"""
For pytest
initialise a test database and profile
"""
from __future__ import absolute_import
import os
import pytest

from aiida_ddec.calculations import DENSITY_DIR_EXTRA

from tests import DATA_DIR
from examples import DATA_DIR as EXAMPLES_DATA_DIR

pytest_plugins = ['aiida.manage.tests.pytest_fixtures', 'aiida_testing.mock_code']  # pylint: disable=invalid-name


@pytest.fixture(scope='function', autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope='function')
def ddec_code(mock_code_factory):
    """Create mocked "DDEC" code."""
    code = mock_code_factory(
        label='chargemol-09_26_2017',
        data_dir_abspath=DATA_DIR,
        entry_point='ddec',
        # files *not* to copy into the data directory
        ignore_paths=('_aiidasubmit.sh', '*.cube')
    )

    # Set atomic density directory extra on code
    density_dir = os.environ.get(DENSITY_DIR_EXTRA)
    if not density_dir:
        density_dir = EXAMPLES_DATA_DIR / 'ddec' / 'atomic_densities'
    code.set_extra(DENSITY_DIR_EXTRA, str(density_dir))

    return code


@pytest.fixture(scope='function')
def cp2k_code(mock_code_factory):
    """Create mocked "cp2k" code."""
    return mock_code_factory(
        label='cp2k-7.1',
        data_dir_abspath=DATA_DIR,
        entry_point='cp2k',
        # files *not* to copy into the data directory
        ignore_paths=('_aiidasubmit.sh', 'BASIS_MOLOPT', 'GTH_POTENTIALS', 'dftd3.dat', '*.bak*')
    )
