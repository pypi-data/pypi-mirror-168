
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from sitreps_python_api.api.code_coverage_api import CodeCoverageApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from sitreps_python_api.api.code_coverage_api import CodeCoverageApi
from sitreps_python_api.api.count_line_of_code_api import CountLineOfCodeApi
from sitreps_python_api.api.integration_tests_api import IntegrationTestsApi
from sitreps_python_api.api.jira_api import JiraApi
from sitreps_python_api.api.project_groups_api import ProjectGroupsApi
from sitreps_python_api.api.projects_api import ProjectsApi
from sitreps_python_api.api.repositories_api import RepositoriesApi
from sitreps_python_api.api.sonar_qube_api import SonarQubeApi
from sitreps_python_api.api.unit_tests_api import UnitTestsApi
from sitreps_python_api.api.default_api import DefaultApi
