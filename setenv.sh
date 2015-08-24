####################################################################################################

source /srv/scratch/python-virtual-env/py3-pyqt5/bin/activate
append_to_path_if_not /usr/local/stow/python-3.4/bin
append_to_ld_library_path_if_not /usr/local/stow/python-3.4/lib/
append_to_python_path_if_not /usr/local/stow/opencv-3.0.0/lib/python3.4/site-packages/

####################################################################################################
# PyOpenGLng

append_to_ld_library_path_if_not /usr/local/stow/freetype-2.5.2/lib

append_to_python_path_if_not $HOME/pyglfw-cffi
append_to_python_path_if_not $HOME/PyOpenGLng

####################################################################################################

append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

append_to_python_path_if_not ${PWD}

####################################################################################################
#
# End
#
####################################################################################################
