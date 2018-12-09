# текущие заботы

## project linking scheme

1. The source tree (files and directories) represent
   the structure of the language, be it C or Python or both.
   The dependancies in C are headers with declarations.
   The source is compiled into files of objects and shared objects.

   This is done with rules.

2. Which are linked into shared objects and executables.
   These are the output of the project, to be packed and run in operations.
   The production of these files is described explicitly in the project file.

   Explicit file rules in rakefile are used for these.


### exp

A file without undefines (test libCAEN) compiles to exactly the same file with and without `-fPIC`.
But a file with undefines has minimally more bytes with `-fPIC` compilation:

    $ ls -l simple_loop.so
    -rw-r--r-- 1 alex alex 1568 Dec  9 14:46 simple_loop.so
    $ ls -l simple_loop.o
    -rw-r--r-- 1 alex alex 1528 Dec  9 14:46 simple_loop.o

You can further link up such file:

    $ clang -fPIC -shared record_run/simple_loop.o -o record_run/simple_loop.so

But it does not know about necessary dynamic dependencies for the undefines:

    $ readelf -d simple_loop.so
    
    Dynamic section at offset 0xe20 contains 24 entries:
      Tag        Type                         Name/Value
     0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
     0x000000000000000c (INIT)               0x4d0
     0x000000000000000d (FINI)               0x6f0

And When you link it properly:

    $ rake build/simple_loop.so
    clang -fPIC -shared test_caen_lib/libCAENVME.o -o build/libCAENVMEtest.so
    clang -fPIC -shared build/libCAENVMEtest.so record_run/simple_loop.so -o build/simple_loop.so
    0 alex @niro :master ~/D/p/p/p/daq
    $ readelf -d build/simple_loop.so
    
    Dynamic section at offset 0xe30 contains 23 entries:
      Tag        Type                         Name/Value
     0x0000000000000001 (NEEDED)             Shared library: [build/libCAENVMEtest.so]
     0x0000000000000001 (NEEDED)             Shared library: [record_run/simple_loop.so]
     0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
     0x000000000000000c (INIT)               0x420

--- still not properly...

The proper way is to link against compiled with `-fPIC` file, not linked with `-shared`:

    $ clang -fPIC -shared build/libCAENVMEtest.so record_run/simple_loop.comp.so -o build/simple_loop.so
    0 alex @niro :master ~/D/p/p/p/daq
    $ readelf -d build/simple_loop.so
    
    Dynamic section at offset 0xe10 contains 25 entries:
      Tag        Type                         Name/Value
     0x0000000000000001 (NEEDED)             Shared library: [build/libCAENVMEtest.so]
     0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
     0x000000000000000c (INIT)               0x4e8
     0x000000000000000d (FINI)               0x700
     0x0000000000000019 (INIT_ARRAY)         0x200e00

--- where `clang -fPIC -I simple_loop.deps/ -c simple_loop.c -o simple_loop.comp.so`.
Let's compile all objects with `fPIC` in 1 rule for now.
In principle it could be separate rule with `file.fpico` extension.
And do the linking explicitly.
Then the only problem is correct path to the lib instead of `build/libCAENVMEtest.so`.



## could a rule do it?

but here each source file has different dependancy on headers..........
more discipline idea:
1. a src file has only 1 header with all its' dependencies
2. thus the header dependencies are put into these headers..
   one encodes them in rakefile
   or parses somehow
-- it seems as an unreasonable additional step, unnecessary file?
   no
   look at `count_words`, which uses the `counter.o` object -- it needs only the header of the object
   in general:
   1. the header is what the object provides to users
   2. internal dependencies of the object are included into its' source and not added to header

so, what is really done for build:

1. source.c file includes some headers -- that's the internal dependencies of the file,
   but source.h file is not the dependencies, it is the interface, the extern definitions or users
2. for building the source file depends on the internal headers,
   one should parse the file to get all dependency filenames
   and then where are they found? the actual dependency header file?
   and where is the link to the actual source of the dependecy?
   (what's the flatter, simpler system..)

   What `include <foo.h>` says is "I use that object, whatever functions it provides -- include them".
   The source file could actually declare each function. but project-wise you just say "that object".
   Then project-wise you at least know the location of that object.
   It is constant thing.
   (It is the interface of the object, even if you build it with some test version of the object,
   the interface is the same.)
   In the build of a given object you give it the environment of object dependancies, be it headers or full so files.

   So, the only question is how to define this dependency project-wise?
   How to swap in test versions of the object files?
   Or use the post-link `LD_PRELOAD` techniques with the linker?
   Or just make the RUNPATH .so files and swap them at operations?
   And when headers or so files are used? How to handle them?
   In the build system with `-Iinclude_path` or in the filesystem paths and `#include "path/dep.h"`?
   Or combination of both: `-Iinclude_package` and `#include "package/modules1/module_x.h"`?
   I think for programming it should be explicit directly in the code in the `#include` statements.
   The dependencies should be immediately visible.
   Without perusing the source files, headers, makefiles and the directory tree.
   Then the dir-names should be more specific than `src` and `include`.

   Linking with so.
   Probably just a header with definitions
   cannot be passed when linking against shared library,
   because the header is a part of the code for compilation
   and linkage is another stage of the whole process.
   The so files are passed to the linker like simple o files, together with main file.
   How are RPATH etc handled in the linkage?
   How to handle the files in the project, the main, o and so files?
   Example solution:
   1. all files are compiled into o files
   2. the shared libraries and executables
      are defined separately in the project file.
   It is the least intrusive solution, that's how things are done traditionally.
   A fault:
   the executable files should be identified automatically if they contain `main`.
   Also will the o and so files should not interfere during linking?
   Another possible trick is to add some kind of additional extension in the filename.

   Why doesn't it work just like python modules?
   Because python modules are homogeneous, they are all the same,
   and here the files are of different types.
   The executable `main` files, archive `a` files and `so` files.
   Also these differences are implicit, they are not evident
   neither from the filename nor from the source file itself.

   So basically, the conclusion for now:
   .o files are compiled from source + all the headers for missing declarations;
   .so and main executables are linked from .o and .so files,
   probably the particularities of .so are handled automatically by the linker;
   the linking does everything automatically,
   you give it a set of files (an .object environment) and it produces a .so or the main executable;
   linking should have options for RUNPATH;
   --- it's a good working hypothesis, further on testing is needed.

3. In principle, separate `src_dependency.h` header is useful:
   * less lines to parse dependencies from
   * kind of cleaner maintenance?

In principle, the header system should show
"interfaces of the system that's the most important!!!" as everybody says.
The dependency graph and stuff..
But parsing of headers or source files... Or of the GNU Makefile... Or even of rakefile...

What if put dependencies with symlinks in:

    ...
    src.c
    src_depns/*.h

then:
1. easy `rule` in rakefile for this
2. easy to see the project even with `tree` or similar stuff

OK, doing it.

    #include <counter.h>
    clang -I src/count_words.deps/ -c src/count_words.c -o count_words.o

and

    #include "count_words.deps/counter.h"
    clang -I src/ -c src/count_words.c -o count_words.o

both work

in any case the rule for rake should be simple
something like:

    rule '.c' [build_dir] => '.deps/*.h' do |task|
        clang -I '.deps/' -c task.name -o build_dir/task_base_filename.o
    end

-- yeah.. the problem is '.c' is rule for _`target_file`_, not a general task "to compile all these .c"


