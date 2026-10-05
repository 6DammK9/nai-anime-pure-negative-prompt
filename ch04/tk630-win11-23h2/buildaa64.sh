#!/bin/bash

set -xeo pipefail

[ ! -d "${POSIX_UEFI_PATH}" ] && echo "POSIX_UEFI_PATH not set" && exit 1

# -target arm64-unknown-windows
CFLAGS=(
    -target arm64-unknown-windows
    -ffreestanding
    -fshort-wchar
    -mno-red-zone
    -Ofast
    -Wall 
    -I/usr/include/efi
    -I/usr/include/efi/protocol
    "-I${POSIX_UEFI_PATH}/uefi"
    -Wframe-larger-than=8192
)
LDFLAGS=(
    -target arm64-unknown-windows
    -nostdlib
    '-Wl,-entry:uefi_init'
    '-Wl,-subsystem:efi_application'
    -fuse-ld=lld-link
    '-Wl,-DEBUG'
)

build_efi()
{
    target="$1"
    shift
    sources="$*"
    objs=()

    for x in $sources
    do
        /home/safeuser/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang "${CFLAGS[@]}" -g -c -o "${x%.*}.o" "$x"
        objs+=("${x%.*}.o")
    done
    
    /home/safeuser/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang "${LDFLAGS[@]}" -v -o "${target}.efi" \
        "${objs[@]}" \
        "${POSIX_UEFI_PATH}/uefi/crt_aarch64.o" \
        "${POSIX_UEFI_PATH}/uefi/stdio.o" \
        "${POSIX_UEFI_PATH}/uefi/stdlib.o" \
        "${POSIX_UEFI_PATH}/uefi/string.o" \
        "${POSIX_UEFI_PATH}/uefi/time.o"
}

build_efi tablesfix tablesfix.c
build_efi readnor readnor.c

