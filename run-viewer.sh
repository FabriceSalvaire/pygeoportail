export VGL_FAKEXCB=1
append_to_path_if_not /opt/VirtualGL/bin
append_to_ld_library_path_if_not /opt/libjpeg-turbo/lib64/
append_to_ld_library_path_if_not /opt/VirtualGL/lib64/
command=optirun
$command ./bin/pygeoportail
unset command
