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
