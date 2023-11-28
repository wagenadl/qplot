# CMakeLists.txt - Part of QPlot, (C) Daniel Wagenaar 2021


######################################################################
cmake_minimum_required(VERSION 3.10.0)

######################################################################
# Set the project name and version
project(QPlot VERSION 0.4.6)
set(CMAKE_PROJECT_HOMEPAGE_URL "http://danielwagenaar.net/qplot")
set(OCTPKG "qplot-${QPlot_VERSION_MAJOR}.${QPlot_VERSION_MINOR}")
set(PYPKG "qplot")

######################################################################
# Specify the C++ standard [must be done _before_ adding executable!]
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON) # I thought this would do the trick...
if (UNIX) 
  add_compile_options(-fPIC) # ... but in fact, this is required on Linux
endif()

# Qt stuff
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
find_package(Qt5 COMPONENTS Widgets Svg PrintSupport REQUIRED)

######################################################################
# Add the executables
add_executable(qplot WIN32 MACOSX_BUNDLE)

include(src/CMakeLists.txt)

# Libraries to link to - Qt must be mentioned
target_link_libraries(qplot Qt5::Widgets)
target_link_libraries(qplot Qt5::Svg)
target_link_libraries(qplot Qt5::PrintSupport)

if (WIN32)
  target_link_libraries(qplot secur32.lib)
endif()

# Produce configuration files
configure_file(src/config.h.in config.h)
##configure_file(doc/version.tex.in version.tex)

# Include paths - Qt must be mentioned
target_include_directories(qplot PUBLIC "${PROJECT_BINARY_DIR}")
target_include_directories(qplot PUBLIC "${Qt5Widgets_INCLUDE_DIRS}")

########################################################################
# Userguide
#if (UNIX AND NOT APPLE)
#  include(doc/UseLATEX.cmake)
#  add_latex_document(doc/userguide.tex IMAGE_DIRS doc doc/icons
#    FORCE_PDF INCLUDE_DIRECTORIES doc)
#endif()

######################################################################
# General packaging / installation
set(CPACK_PACKAGE_VENDOR "Daniel Wagenaar")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "QPlot - Publication-quality plotting package for Python, Matlab, Octave, or stand-alone")
set(CPACK_PACKAGE_DESCRIPTION
  "QPlot is a package for production of publication-quality 2D graphics. QPlot can run stand-alone, or, more conveniently, from within Python, Matlab, or Octave.")
set(CPACK_PACKAGE_EXECUTABLES "qplot;QPlot")

if (WIN32)
  include(WinPack.CMakeLists.txt)
  
#elseif (APPLE)
#  set(CPACK_GENERATOR "DMG") # NYI
#
#  get_target_property(_qmake_executable Qt5::qmake IMPORTED_LOCATION)
#  get_filename_component(_qt_bin_dir "${_qmake_executable}" DIRECTORY)
#  find_program(MACDEPLOYQT_EXECUTABLE macdeployqt HINTS "${_qt_bin_dir}")
#  add_custom_command(TARGET myapp POST_BUILD
#    COMMAND "${MACDEPLOYQT_EXECUTABLE}"
#    "$<TARGET_FILE_DIR:myapp>/../.."
#    -always-overwrite
#    COMMENT "Running macdeployqt..."
#    )
elseif (UNIX)
  include(UnixInstall.CMakeLists.txt)
  include(DebPack.CMakeLists.txt)
endif()

# Packaging
include(CPack)

