.. _qibuild-cmake-coding-guide:

CMake coding guide
==================

.. highlight:: cmake


General
-------

* Keep the length of the line below 80 characters when possible, and when it
  does not hurt readability, and below 100 characters at any case.

* Indentation is made with two spaces

* No trailing whitespace are allowed.

* Wrap the line at 80-100 characters.

* Every text file must be pushed using UNIX line endings. (On windows, you are
  advised to set core.autocrlf to true).

* Please use a spell checker when you write comments. Typos in
  comments are annoying and distractive.

* Never use old CMake syntax code for loop constructs::

    # NO
    if(foo)
    #  ...
    else(foo)
    #  ...
    endif(foo)

    # YES
    if(foo)
    #  ...
    else()
    # ...
    endif()

* Although CMake is rather lenient with case sensitivity, please write every
  function lower-case, and separate words by underscores::

    #NO
    function(QI_MY_WONDERFUL_FUNCTION)
    #  ...
    endfunction()

    #YES
    function(qi_my_nice_function)
    #  ...
    endfunction()

* Every function in the public API of qiBuild code (i.e: that could en up in a
  user cmake code) must start with qi, other should not start with qi (prefer
  using _qi for example).

* When writing a convenience function, not to be used outside, start the name
  with an underscore, if you have a whole bunch of internal functions, put them
  in a separated file, in the ``internal`` subdirectory.

* The ``CMakeParseArguments`` module is very useful, please use it.

* Please do not use C-like construct for strings spanning on several lines;
  rather use nice CMake feature for this::

    # NO
    message(STATUS  "This is a very long\n"
                  "message on\n"
                  "several lines\n"
    )

    # YES
    message(STATUS "This is a very long
      message spanning on
      several lines
    ")

  See `CMake Syntax <http://www.cmake.org/cmake/help/syntax.html>`_

* Use the log functions carefully. The output of CMake must stay minimal (when
  it gets too long, it is impossible for the user to see if something went
  wrong)

* If you run into a CMake warning, never ignore it. Fix your code or file a bug
  report. (CMake warnings almost always mean there is a nasty bug somewhere)

Documentation
-------------

In the CMake code
++++++++++++++++++


* Every function in the public API must have corresponding documentation. It
  works a bit like Doxygen, but with the python-sphinx syntax

.. code-block:: cmake

    #! foobar : this function does foo then bar! (small description)
    # this is a long description for the function, the function have two
    # parameters accept two flags, two params and two groups.
    # \argn: a list of optional arguments
    # \arg:first_arg the first argument
    # \arg:second_arg the second argument
    # \param:PARAM1 PARAM1 specify the fooness of the function
    # \param:PARAM2 PARAM2 should always be 42
    # \group:GROUP1 GROUP1 is a list of project to foo
    # \group:GROUP2 This group represent optional projects to pass to bar
    function(foobar first_arg second_arg)
      cmake_parse_arguments(ARG "FLAG1;FLAG2" "PARAM1;PARAM2" "GROUP1;GROUP2" ${ARGN})
    endfunction()

Note the bang in the first line of the documentation of the function.

The rest is straightforward

**\\arg:<name>**
  this represent a function parameter, the name is the name of the parameter
  you are documenting.

**\\flag:<FLAG>**
   This represent a boolean value, the flag could be present or not. (see
   CMakeParseArguments)

**\\param:<PARAM>**
   indicates a "one-value option" : the keyword must be followed by a value
   (see CMakeParseArguments)

**\\group:<GROUP>**
  indicates a "multi-value option" : the keyword will be followed by a list of
  values (see CMakeParseArguments)


In sphinx
+++++++++

* Note: if you add a completely new functionality, you may want to add the
  new functions in a new file. For instance ``qi_make_coffee`` in ``coffee.cmake``
  In this case you have to:

  * add ``include(qibuild/coffee.cmake)`` somewhere in ``qibuild/general.cmake``
  * add you file to the list of the documented files in ``doc/tools/gen_cmake_doc.py``
  * and of course adding a tutorial on how to make coffee with qibuild :)


Conditions and Variables
------------------------

* Always quote variable that represent a string::

    set(myvar "foo")
    if ("${myvar}" STREQUAL "bar")
    # ...
    endif()

* Do not quote variable that are booleans ::

    set(mybvar ON)
    set(mybvar OFF)
    if (myvar)
    # ...
    endif()

    # Note that this will NOT produce the
    # expected result:
    if(${myvar}) # bug!

    endif()

* When storing paths in variables, do NOT have the CMake variables end up with
  a slash::

    # YES:
    set(_my_path "path/to/foo")
    set(_my_other_path "${_my_path}/${_my_var}")

    # NO:
    set(my_path "path/to/foo/")
    set(_my_other_path "${_my_path}${_my_var}")   # wrong: this is ugly
    set(_my_other_path "${_my_path}/${_my_var}")  # this is a bug!, see below

If you don't do this, you may end up with paths containing //. This does not
matter much on Linux, but on Windows, this path may be re-converted into native
paths (for instance in the .bat generated by CMake), so you end up with
\\\\ in the path name on Windows, which is the notation for shared folders ...

* Declaring a list::

    # declare an empty list:
    set(mylist)

* Declaring and initializing a list at the same time::

    # a list with 3 items:
    set(mylist item1 "a second item" item3)

    #or

    set(mylist
      item1
      "a second item"
      item3
    )

* Always use ``list(APPEND)`` to append to a list::

    list(APPEND mylist "one item")

* Always quote string when comparing string in a `if`::

    set(myvar "test")
    if ("${myvar}" STREQUAL "test")
    # ...
    endif()

* Do not use "empty" vars::

    # YES:
    qi_create_bin(bar bar.cpp)
    set(_deps baz)
    if (WITH_FOO)
      list(APPENDS _deps FOO)
    endif()
    qi_use_lib(bar ${_deps})

    # NO:
    if(WITH_FOO)
      set(_foo FOO)
    endif()

    qi_use_lib(bar baz ${_foo})

  This is confusing and does not save that much lines.
  Actually the best solution is::

    qi_create_bin(bar bar.cpp)
    qi_use_lib(bar baz)
    if(WITH_FOO)
      qi_use_lib(bar FOO)
    endif()


* Always use ``if(DEFINED varname)`` to check if a variable is set::

    if (DEFINED myvar)
    #  ...
    endif()

* Do not quote variables that CMake expects to be a list::

    set(_foo_args "--foo" "--bar")

    # YES:
    execute_process(COMMAND foo ${_foo_args})

    # NO:
    execute_process(COMMAND foo "${_foo_args}")

In the second line, since you have quoted the list, you are calling foo with one
argument, ("--foo --bar").

* When you need a function to return a result, use::

    function(compute_stuff arg res)
      set(_result)
      # Store something in _result using ${arg}
      set(${res} ${_result} PARENT_SCOPE)
    endfunction()
    compute_stuff(my_arg result)
    do_something(${result})
    # NOT set(res ... PARENT_SCOPE)


.. _qibuild-cmake-common-mistakes:

Common mistakes
----------------


* A very common mistake is to use something like::

    set(_my_out ${CMAKE_BINARY_DIR}/sdk)

  This will work fine most of the time, but :
   - qibuild users may have chosen a unique sdk dir
   - they also may have chose a unique build directory
     (useful for eclipse, for instance)

  so please use `QI_SDK_DIR` instead


* Do not set CMAKE_CXX_FLAGS::

    # This will break cross-compilation
    set(CMAKE_CXX_FLAGS "-DFOO=42")

    # use:
    add_definitions("-DFOO=42")

    # or, better, set the compile flags
    # only when necessary:
    # (this will save compile time when you change the define!)
    set_source_files_properties(
      src/foo.cpp
        PROPERTIES
          COMPILE_DEFINITIONS FOO=42
    )


* Do not set CMAKE_FIND_ROOT_PATH::

    # This will break finding packages in the toolchain:

    set(CMAKE_FIND_ROOT_PATH "/path/to/something")

    # Use this instead:

    # (create an empty list if CMAKE_FIND_ROOT_PATH does not exist)
    if(NOT CMAKE_FIND_ROOT_PATH)
      set(CMAKE_FIND_ROOT_PATH)
    endif()
    list(APPEND CMAKE_FIND_ROOT_PATH "/path/to/something")


* Do not set CMAKE_MODULE_PATH::

    # This will break finding the qibuild framework
    #  include (qibuild/general) will no longer work

    set (CMAKE_MODULE_PATH "/path/to/something")

    # Use this instead:

    # (create an empty list if CMAKE_FIND_ROOT_PATH does not exist)
    if(NOT CMAKE_MODULE_PATH)
      set(CMAKE_MODULE_PATH)
    endif()
    list(APPEND CMAKE_MODULE_PATH "/path/to/something")

* Do not use ``${PROJECT_NAME}``, or ``${CMAKE_PROJECT_NAME}``,
  especially when not at the top ``CMakeLists.txt``::

    # YES:
    project(foo)
    find_package(qibuild)

    qi_create_lib(foo foo.cpp)
    qi_use_lib(foo BAR BAZ)

    # NO:
    project(foo)
    find_package(qibuild)

    qi_create_lib(${PROJECT_NAME} foo.cpp)
    qi_use_lib(${PROJECT_NAME} BAR BAZ)


The small duplication (writing the name of the target ``foo`` 3 times)
is OK, because:

* otherwise you need to scroll to the top of the file to find out
  the name of the library
* ``PROJECT_NAME`` is something that ends up in the IDE, so it's not
  a target name
* calling ``project()`` causes the toolchain file to be parsed again
  for no good reason
* there's often more than one lib per project
