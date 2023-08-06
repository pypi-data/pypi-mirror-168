"""_1521.py

ScriptingSetup
"""


from mastapy._internal import constructor
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_SCRIPTING_SETUP = python_net_import('SMT.MastaAPI.Utility.Scripting', 'ScriptingSetup')


__docformat__ = 'restructuredtext en'
__all__ = ('ScriptingSetup',)


class ScriptingSetup(_1395.PerMachineSettings):
    """ScriptingSetup

    This is a mastapy class.
    """

    TYPE = _SCRIPTING_SETUP

    def __init__(self, instance_to_wrap: 'ScriptingSetup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def image_height(self) -> 'int':
        """int: 'ImageHeight' is the original name of this property."""

        temp = self.wrapped.ImageHeight

        if temp is None:
            return None

        return temp

    @image_height.setter
    def image_height(self, value: 'int'):
        self.wrapped.ImageHeight = int(value) if value else 0

    @property
    def image_width(self) -> 'int':
        """int: 'ImageWidth' is the original name of this property."""

        temp = self.wrapped.ImageWidth

        if temp is None:
            return None

        return temp

    @image_width.setter
    def image_width(self, value: 'int'):
        self.wrapped.ImageWidth = int(value) if value else 0

    @property
    def load_scripted_properties_when_opening_masta(self) -> 'bool':
        """bool: 'LoadScriptedPropertiesWhenOpeningMASTA' is the original name of this property."""

        temp = self.wrapped.LoadScriptedPropertiesWhenOpeningMASTA

        if temp is None:
            return None

        return temp

    @load_scripted_properties_when_opening_masta.setter
    def load_scripted_properties_when_opening_masta(self, value: 'bool'):
        self.wrapped.LoadScriptedPropertiesWhenOpeningMASTA = bool(value) if value else False

    @property
    def python_exe_path(self) -> 'str':
        """str: 'PythonExePath' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PythonExePath

        if temp is None:
            return None

        return temp

    @property
    def python_home_directory(self) -> 'str':
        """str: 'PythonHomeDirectory' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PythonHomeDirectory

        if temp is None:
            return None

        return temp

    @property
    def python_install_directory(self) -> 'str':
        """str: 'PythonInstallDirectory' is the original name of this property."""

        temp = self.wrapped.PythonInstallDirectory

        if temp is None:
            return None

        return temp

    @python_install_directory.setter
    def python_install_directory(self, value: 'str'):
        self.wrapped.PythonInstallDirectory = str(value) if value else ''

    @property
    def run_scripts_in_separate_threads(self) -> 'bool':
        """bool: 'RunScriptsInSeparateThreads' is the original name of this property."""

        temp = self.wrapped.RunScriptsInSeparateThreads

        if temp is None:
            return None

        return temp

    @run_scripts_in_separate_threads.setter
    def run_scripts_in_separate_threads(self, value: 'bool'):
        self.wrapped.RunScriptsInSeparateThreads = bool(value) if value else False

    @property
    def use_default_net_solution_directory(self) -> 'bool':
        """bool: 'UseDefaultNETSolutionDirectory' is the original name of this property."""

        temp = self.wrapped.UseDefaultNETSolutionDirectory

        if temp is None:
            return None

        return temp

    @use_default_net_solution_directory.setter
    def use_default_net_solution_directory(self, value: 'bool'):
        self.wrapped.UseDefaultNETSolutionDirectory = bool(value) if value else False

    @property
    def use_default_plug_in_directory(self) -> 'bool':
        """bool: 'UseDefaultPlugInDirectory' is the original name of this property."""

        temp = self.wrapped.UseDefaultPlugInDirectory

        if temp is None:
            return None

        return temp

    @use_default_plug_in_directory.setter
    def use_default_plug_in_directory(self, value: 'bool'):
        self.wrapped.UseDefaultPlugInDirectory = bool(value) if value else False

    @property
    def use_default_python_scripts_directory(self) -> 'bool':
        """bool: 'UseDefaultPythonScriptsDirectory' is the original name of this property."""

        temp = self.wrapped.UseDefaultPythonScriptsDirectory

        if temp is None:
            return None

        return temp

    @use_default_python_scripts_directory.setter
    def use_default_python_scripts_directory(self, value: 'bool'):
        self.wrapped.UseDefaultPythonScriptsDirectory = bool(value) if value else False

    @property
    def mastapy_version(self) -> 'str':
        """str: 'MastapyVersion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MastapyVersion

        if temp is None:
            return None

        return temp

    def add_existing_net_solution(self):
        """ 'AddExistingNETSolution' is the original name of this method."""

        self.wrapped.AddExistingNETSolution()

    def restore_api_packages(self):
        """ 'RestoreAPIPackages' is the original name of this method."""

        self.wrapped.RestoreAPIPackages()

    def select_net_solution_directory(self):
        """ 'SelectNETSolutionDirectory' is the original name of this method."""

        self.wrapped.SelectNETSolutionDirectory()

    def select_plug_in_directory(self):
        """ 'SelectPlugInDirectory' is the original name of this method."""

        self.wrapped.SelectPlugInDirectory()

    def select_python_install_directory(self):
        """ 'SelectPythonInstallDirectory' is the original name of this method."""

        self.wrapped.SelectPythonInstallDirectory()

    def select_python_scripts_directory(self):
        """ 'SelectPythonScriptsDirectory' is the original name of this method."""

        self.wrapped.SelectPythonScriptsDirectory()
