# Win11 ARM 23H2 "ACPI fix" EFI build in general Ubuntu x86 server #

- Intention: My TK630 / PT620 doesn't work based from [#3](https://github.com/dixyes/d920s10/issues/3). Rebuild code is *a bit complicated*.
  - Getting the concept on cross compiling, especially Linux x86 to Winodws ARM (instead of Winodws x86 to Linux ARM), is a bit messy.
  - After a bit of research, it can be solved elegently by [a built toolchain](https://github.com/mstorsjo/llvm-mingw).

- Using the release version [20240709](https://github.com/dixyes/d920s10/releases/tag/20240709) instead of the recent dynamic one.

- ISO: [Windows 11 23H2 ARM64 (French)](https://archive.org/details/windows-11-23-h-2-arm-64)

```sh
wget https://github.com/dixyes/d920s10/archive/refs/tags/20240709.tar.gz
tar -xzf 20240709.tar.gz
# Export tgz from https://gitlab.com/bztsrc/posix-uefi
git pull https://gitlab.com/bztsrc/posix-uefi

# https://voxelmanip.se/2024/12/10/cross-compiling-for-windows-using-llvm-mingw/
wget https://github.com/mstorsjo/llvm-mingw/releases/download/20260922/llvm-mingw-20260922-ucrt-ubuntu-22.04-aarch64.tar.xz
tar -xf llvm-mingw-20260922-ucrt-ubuntu-22.04-aarch64.tar.xz

# Ref: https://www.biosconfessions.com/posts/from-silicon-to-shell/2-toolchain-setup/
# Ref: https://www.reddit.com/r/rust/comments/s45mn7/how_to_crosscompile_from_linux_to_windows/?show=original
# LLVM-MinGW Clang Toolchains. Warning: 2-3GB of space (SDK matters)
sudo apt install gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu clang llvm mingw-w64

# 11.4.0 (22.04), 13.3.0 (24.04)
aarch64-linux-gnu-gcc --version
# 14.0.0 (22.04), 18.1.3 (24.04)
clang -v
# exec format error
# ./llvm-mingw-20260922-ucrt-ubuntu-22.04-aarch64/bin/clang -v
# 23.1.2
./llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang -v

# Build first: https://gitlab.com/bztsrc/posix-uefi
# 920 special: Must be ARM
cd posix-uefi-master/uefi

# USE_GCC=1
ARCH=aarch64 CROSS_COMPILE=aarch64-linux-gnu- make

cd ../../

cd d920s10-20240709
# Codes modified! See below.
# It should works already.
POSIX_UEFI_PATH=../posix-uefi-master ./buildaa64.sh 

# Probably need MSVC (msvc-wine)
# unable to execute command: Executable "lld-link" doesn't exist!

# Need QEMU with --sysroot
# lld-link: error: ../posix-uefi-master/uefi/string.o: machine type x64 conflicts with arm64

# Ref: https://stackoverflow.com/questions/78720570/cross-compiling-for-aarch64-with-clang-built-from-source
# Just make clean and try again!
```

- Success build log:

```log
+ '[' '!' -d ../posix-uefi-master ']'
+ CFLAGS=(-target arm64-unknown-windows -ffreestanding -fshort-wchar -mno-red-zone -Ofast -Wall -I/usr/include/efi -I/usr/include/efi/protocol "-I${POSIX_UEFI_PATH}/uefi" -Wframe-larger-than=8192)
+ LDFLAGS=(-target arm64-unknown-windows -nostdlib '-Wl,-entry:uefi_init' '-Wl,-subsystem:efi_application' -fuse-ld=lld-link '-Wl,-DEBUG')
+ build_efi tablesfix tablesfix.c
+ target=tablesfix
+ shift
+ sources=tablesfix.c
+ objs=()
+ for x in $sources
+ /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang -target arm64-unknown-windows -ffreestanding -fshort-wchar -mno-red-zone -Ofast -Wall -I/usr/include/efi -I/usr/include/efi/protocol -I../posix-uefi-master/uefi -Wframe-larger-than=8192 -g -c -o tablesfix.o tablesfix.c
clang: warning: argument '-Ofast' is deprecated; use '-O3' to enable only conforming optimizations, or consult the documentation for the same behavior [-Wdeprecated-ofast]
+ objs+=("${x%.*}.o")
+ /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang -target arm64-unknown-windows -nostdlib -Wl,-entry:uefi_init -Wl,-subsystem:efi_application -fuse-ld=lld-link -Wl,-DEBUG -v -o tablesfix.efi tablesfix.o ../posix-uefi-master/uefi/crt_aarch64.o ../posix-uefi-master/uefi/stdio.o ../posix-uefi-master/uefi/stdlib.o ../posix-uefi-master/uefi/string.o ../posix-uefi-master/uefi/time.o
clang version 23.1.2 (https://github.com/llvm/llvm-project.git 85ac560262434c9ccfc0c183ec22d4138ed647fb)
Target: arm64-unknown-windows-msvc
Thread model: posix
InstalledDir: /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin
 "/home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/lld-link" -out:tablesfix.efi -libpath:lib/arm64 -libpath:atlmfc/lib/arm64 -libpath:/home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/lib/clang/23/lib/windows -nologo -entry:uefi_init -subsystem:efi_application -DEBUG tablesfix.o ../posix-uefi-master/uefi/crt_aarch64.o ../posix-uefi-master/uefi/stdio.o ../posix-uefi-master/uefi/stdlib.o ../posix-uefi-master/uefi/string.o ../posix-uefi-master/uefi/time.o
+ build_efi readnor readnor.c
+ target=readnor
+ shift
+ sources=readnor.c
+ objs=()
+ for x in $sources
+ /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang -target arm64-unknown-windows -ffreestanding -fshort-wchar -mno-red-zone -Ofast -Wall -I/usr/include/efi -I/usr/include/efi/protocol -I../posix-uefi-master/uefi -Wframe-larger-than=8192 -g -c -o readnor.o readnor.c
clang: warning: argument '-Ofast' is deprecated; use '-O3' to enable only conforming optimizations, or consult the documentation for the same behavior [-Wdeprecated-ofast]
+ objs+=("${x%.*}.o")
+ /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/clang -target arm64-unknown-windows -nostdlib -Wl,-entry:uefi_init -Wl,-subsystem:efi_application -fuse-ld=lld-link -Wl,-DEBUG -v -o readnor.efi readnor.o ../posix-uefi-master/uefi/crt_aarch64.o ../posix-uefi-master/uefi/stdio.o ../posix-uefi-master/uefi/stdlib.o ../posix-uefi-master/uefi/string.o ../posix-uefi-master/uefi/time.o
clang version 23.1.2 (https://github.com/llvm/llvm-project.git 85ac560262434c9ccfc0c183ec22d4138ed647fb)
Target: arm64-unknown-windows-msvc
Thread model: posix
InstalledDir: /home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin
 "/home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/bin/lld-link" -out:readnor.efi -libpath:lib/arm64 -libpath:atlmfc/lib/arm64 -libpath:/home/user/opt_261005/llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64/lib/clang/23/lib/windows -nologo -entry:uefi_init -subsystem:efi_application -DEBUG readnor.o ../posix-uefi-master/uefi/crt_aarch64.o ../posix-uefi-master/uefi/stdio.o ../posix-uefi-master/uefi/stdlib.o ../posix-uefi-master/uefi/string.o ../posix-uefi-master/uefi/time.o
```

- Codes changed:
  - **TK630 behaves like W510!** [ACPI_BIOS_ERROR](https://dixyes.dev/posts/2023/03/27/run-windows-on-d920s10/) is reproduced. [W510 case](https://github.com/dixyes/d920s10/issues/3) has been expended.
  - **TK630 does not have UEFI shell!** [Synchronous Excception](https://github.com/dixyes/d920s10/issues/2) appears after chainload. Therefore chainload has been disabled. Now it exits to BIOS screen then boot overridde.
  - *Boot menu key is F3.*

- Post install EFI:
  - Revert the swap and use the no-chain EFI again. Now it is magically carry to the next UEFI option i.e. OS Boot.
  - BSOD `CLOCK_WATCHDOG_TIMEOUT` appears after first OS boot.
  - Removing USB key will have `ACPI_BIOS_ERROR`.
  - ~~Use the "non W510 no chain"?~~ **Use a tiny (say 2GB, must be FAT) USB with the exact same EFI file path.** [Ref.](https://developer.seco.com/how-to/uefi-bootable-usb/) will magically get into Windows!
  