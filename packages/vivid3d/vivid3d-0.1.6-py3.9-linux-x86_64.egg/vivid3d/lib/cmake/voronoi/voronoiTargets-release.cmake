#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "voronoi::voronoi" for configuration "Release"
set_property(TARGET voronoi::voronoi APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(voronoi::voronoi PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libvoronoi.so"
  IMPORTED_SONAME_RELEASE "libvoronoi.so"
  )

list(APPEND _cmake_import_check_targets voronoi::voronoi )
list(APPEND _cmake_import_check_files_for_voronoi::voronoi "${_IMPORT_PREFIX}/lib/libvoronoi.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
