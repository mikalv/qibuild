## Copyright (c) 2012-2018 SoftBank Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.
cmake_minimum_required(VERSION 2.8)
project(warnings)

find_package(qibuild)
qi_sanitize_compile_flags()

qi_create_bin(foo "main.cpp")

