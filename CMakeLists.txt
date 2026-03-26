# CMakeLists.txt - Part of QPlot, (C) Daniel Wagenaar 2013-2024


######################################################################
cmake_minimum_required(VERSION 3.10.0)

######################################################################
# Set the project name and version
project(QPlot VERSION 0.6.1)
set(CMAKE_PROJECT_HOMEPAGE_URL "http://danielwagenaar.net/qplot")
set(OCTPKG "qplot-${QPlot_VERSION_MAJOR}.${QPlot_VERSION_MINOR}")
set(PYPKG "pyqplot")

######################################################################
# Specify the C++ standard [must be done _before_ adding executable!]
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON) # I thought this would do the trick...
if (UNIX) 
  add_compile_options(-fPIC) # ... but in fact, this is required on Linux
endif()

# Qt stuff
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
##find_package(pybind11 CONFIG REQUIRED)

# ── Locate Qt6 via PyQt6's bundled installation ──────────────────────────────
find_package(Python REQUIRED COMPONENTS Interpreter)

# ── Locate Qt6 headers (build-time) ──────────────────────────────────────────
# Priority:
#   1. QT_INSTALL_PREFIX env var (set by cibuildwheel before-all or developer)
#   2. qt_install_prefix.txt written by install_qt_dev.py
#   3. PyQt6's own directory (has CMake configs on some platforms — last resort)
execute_process(COMMAND "python" "tools/install_qt_dev.py")
if(DEFINED ENV{QT_INSTALL_PREFIX})
  list(PREPEND CMAKE_PREFIX_PATH "$ENV{QT_INSTALL_PREFIX}")
  message(STATUS "Qt6 prefix from QT_INSTALL_PREFIX: $ENV{QT_INSTALL_PREFIX}")

elseif(EXISTS "${CMAKE_SOURCE_DIR}/qt_install_prefix.txt")
  file(READ "${CMAKE_SOURCE_DIR}/qt_install_prefix.txt" _qt_prefix)
  string(STRIP "${_qt_prefix}" _qt_prefix)
  list(PREPEND CMAKE_PREFIX_PATH "${_qt_prefix}")
  message(STATUS "Qt6 prefix from qt_install_prefix.txt: ${_qt_prefix}")
  set(Qt6_DIR "${_qt_prefix}/lib/cmake/Qt6")

else()
  message(WARNING
    "QT_INSTALL_PREFIX not set and qt_install_prefix.txt not found. "
    "Falling back to system Qt — run scripts/install_qt_dev.py first "
    "or set QT_INSTALL_PREFIX to your Qt installation."
  )
endif()

find_package(Qt6 COMPONENTS Core Widgets Svg PrintSupport REQUIRED)

qt_standard_project_setup() #?

######################################################################
# Add the executables
add_executable(qplot WIN32 MACOSX_BUNDLE)

include(backend/src/CMakeLists.txt)
target_sources(qplot PRIVATE backend/src/qplot.qrc )

# Libraries to link to - Qt must be mentioned
target_link_libraries(qplot PRIVATE Qt6::Widgets)
target_link_libraries(qplot PRIVATE Qt6::Svg)
target_link_libraries(qplot PRIVATE Qt6::PrintSupport)

if (WIN32)
  target_link_libraries(qplot secur32.lib)
endif()

# Produce configuration files
configure_file(backend/src/config.h.in config.h)
##configure_file(doc/version.tex.in version.tex)

# Include paths - Qt must be mentioned
target_include_directories(qplot PUBLIC "${PROJECT_BINARY_DIR}")
target_include_directories(qplot PUBLIC "${Qt6Widgets_INCLUDE_DIRS}")

######################################################################
# Copy RPATH settings so the binary also finds Qt6 via PyQt6 at runtime
if(APPLE)
  set_target_properties(qplot PROPERTIES
    INSTALL_RPATH "@loader_path/../PyQt6/Qt6/lib"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
elseif(UNIX)
  set_target_properties(qplot PROPERTIES
    INSTALL_RPATH "$ORIGIN/../PyQt6/Qt6/lib"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
endif()


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
#  get_target_property(_qmake_executable Qt6::qmake IMPORTED_LOCATION)
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

