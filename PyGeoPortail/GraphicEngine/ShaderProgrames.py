####################################################################################################
#
# PyGeoPortail - A IGN GeoPortail Map Viewer
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import glob
import os

import yaml

####################################################################################################

from PyOpenGLng.HighLevelApi.Shader import GlShaderManager, GlShaderProgramInterface

####################################################################################################

class ConfigPath(object):

    module_path = os.path.dirname(__file__)

    ##############################################

    @staticmethod
    def glsl(file_name):

        return os.path.join(ConfigPath.module_path, 'glslv4', file_name)

    ##############################################

    def __init__(self):

        glsl_files = glob.glob(os.path.join(self.module_path, 'glslv4', '*', '*.glsl'))
        self._paths = {os.path.basename(path):path for path in glsl_files}

    ##############################################

    def __getitem__(self, name):

        return self._paths[name + '.glsl']

####################################################################################################

config_path = ConfigPath()
shader_program_definitions = yaml.load(open(ConfigPath.glsl('shader-programs.yml'), 'r'))

shader_manager = GlShaderManager()

program_interfaces = {}
for name, kwargs in shader_program_definitions['interfaces'].items():
    program_interfaces[name] = GlShaderProgramInterface(**kwargs)

if shader_manager.has_visual():
    loaded_shaders = set()
    for name, kwargs in shader_program_definitions['programs'].items():
        shaders = kwargs['shaders']
        for shader_name in shaders:
            if shader_name not in loaded_shaders:
                shader_manager.load_from_file(shader_name, config_path[shader_name])
                loaded_shaders.add(shader_name)
        # kwargs.get('interface', None)
        program_interface = program_interfaces[kwargs['interface']]
        shader_manager.link_program(name, shaders, program_interface=program_interface)

####################################################################################################
#
# End
#
####################################################################################################
