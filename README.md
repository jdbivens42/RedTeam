# RedTeam
A collection of miscellaneous tools and snippets for Red Teaming too small to justify their own repositories.

## handle_http.py
A simple HTTP shell handler that borrows heavily from c2trash (https://github.com/jdbivens42/c2trash/tree/master/c2trash).

### Features
Supports multiple targets.
Anything that can download and execute an HTTP page is a fully supported client.
Optional SSL / HTTPS encryption

### Known Limitations
NAT'ed targets are a race condition (the first client to request the page will consume all commands).


## php_shell.py
A PHP backdoor generator and client.

### Features
Highly customizable, lots of options to tweak to meet your confidentiality and space requirements.
Optional authenticated backdoors.
Optional encrypted communications with backdoor (rc4 with single-use keys).
Client transparently manages all communications.
Client provides shell-like interface with arrow keys and command history (prompt_toolkit).
Can produce an infection one-liner to backdoor all PHP files on a webserver without disrupting normal functionality.
Randomly generated keys and passwords keep communications [relatively] secure.
Includes detailed help menu with examples of usage.
