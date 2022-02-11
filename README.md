# Zstd decompression

Python CLI utility for handling zstd compression and tar contents - includes stream and sync decompression techniques, as well as a more verbose sync approach that ensures proper tar file output.

Uses fire library to automatically create and handle CLI args sourced from init function.

## Inspiration

Originally written when I was experimenting with customising the Godot game engine and with cross-compilation from a windows environment, using approaches like Scoop, SCons, MSYS2, Mingw-w64, LLVM.

At this time GCC downloads suddenly switched to zstd and Scoop's 7zip version was not updated to support zstd - so I ended up writing this script both as a solution and to learn more about it.

Some further notes and commands on compiling GCC and Godot are found [here](https://github.com/PAR-iTY/cli-notes/blob/main/gcc-godot.md)
