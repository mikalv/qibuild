##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2010 Aldebaran Robotics
##

include("qibuild/log")
include("qibuild/set")
include("qibuild/expect")
include("qibuild/layout")

if (NOT QI_SDK_DIR)
  qi_set_global(QI_SDK_DIR "${CMAKE_BINARY_DIR}/sdk/")
  qi_info("QI_SDK_DIR: ${QI_SDK_DIR}")
endif (NOT QI_SDK_DIR)

#force buildtype to be Upper case
if (DEFINED CMAKE_BUILD_TYPE)
  string(TOUPPER "${CMAKE_BUILD_TYPE}" "_BUILD_TYPE")
  qi_set_global(CMAKE_BUILD_TYPE "${_BUILD_TYPE}")
endif()

#ensure CMAKE_BUILD_TYPE is either Debug or Release
if (CMAKE_BUILD_TYPE STREQUAL "")
  qi_set_global(CMAKE_BUILD_TYPE "RELEASE")
endif (CMAKE_BUILD_TYPE STREQUAL "")

include("qibuild/uselib")
include("qibuild/launcher")
include("qibuild/tests")
include("qibuild/target")
include("qibuild/submodule")
