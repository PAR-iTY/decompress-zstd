# -----------------------

# Zstd decompression

# -----------------------

Python CLI utility for handling zstd compression and tar contents - includes stream and sync decompression techniques, as well as a more verbose sync approach that ensures proper tar file output.

Uses fire library to automatically create and handle CLI args sourced from init function

Originally written when I was experimenting with customising the Godot game engine and with cross-compilation from a windows environment, using approaches like Scoop, SCons, MSYS2, Mingw-w64, LLVM.

At this time GCC downloads suddenly switched to zstd and Scoop's 7zip version was not updated to support zstd - so I ended up writing this script both as a solution and to learn more about it.

Below are some further notes and commands I wrote for cross-compiling Godot.

# -----------------------

## Godot

# -----------------------

use godot-3.2.2-stable to match docs for ECMAScript compilation

use godot-3.2.3-stable to match docs for Rust compilation

Godot 3.2 requires a C++ 11-compatible compiler to be built from source
Godot 4.0 will require a C++ 17-compatible compiler to be built from source

run from path/to/godot-[version]-stable to compile
place SConsctruct file at script root

# -----------------------

## SCons

# -----------------------

scons -j6 platform=windows use_mingw=yes use_lto=yes bits=64

use LLVM:
use_llvm=yes use_lld=yes

add link-time optimization:
use_lto=yes

get more output:
verbose=yes

pick x86 or x86_64 for Windows:
bits=32
bits=64

# -----------------------

## Scoop

# -----------------------

custom scoop manifest json file: scoop + custom gcc url + posix threads

{
"version": "9.3.0",
"homepage": "https://repo.msys2.org/mingw/x86_64/",
"url": "https://repo.msys2.org/mingw/x86_64/mingw-w64-x86_64-gcc-9.3.0-2-any.pkg.tar.xz",
"args": ["--enable-threads=posix"]
}
