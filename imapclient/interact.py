#!/usr/bin/python

# Copyright (c) 2012, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses


from getpass import getpass
from optparse import OptionParser

from config import parse_config_file, create_client_from_config

def command_line():
    p = OptionParser()
    p.add_option('-H', '--host', dest='host', action='store',
                 help='IMAP host connect to')
    p.add_option('-u', '--username', dest='username', action='store',
                 help='Username to login with')
    p.add_option('-p', '--password', dest='password', action='store',
                 help='Password to login with')
    p.add_option('-P', '--port', dest='port', action='store',
                 default=None, help='IMAP port to use (default is 143)')
    p.add_option('-s', '--ssl', dest='ssl', action='store_true', default=False,
                 help='Use SSL connection')
    p.add_option('-f', '--file', dest='file', action='store', default=None,
                 help='Config file (same as livetest)')

    opts, args = p.parse_args()
    if args:
        p.error('unexpected arguments %s' % ' '.join(args))

    if opts.file:
        if opts.host or opts.username or opts.password or opts.port or opts.ssl:
            p.error('If -f/--file is given no other options can be used')
        # Use the options in the config file
        opts = parse_config_file(opts.file)
    else:
        # Get compulsory options if not given on the command line
        for opt_name in ('host', 'username', 'password'):
            if not getattr(opts, opt_name):
                setattr(opts, opt_name, getpass(opt_name + ': '))
        if not opts.port:
            opts.port = 143
        opts.oauth = False     # OAUTH not supported on command line
    return opts

def main():
    opts = command_line()
    print 'Connecting...'
    client = create_client_from_config(opts)
    print 'Connected.'
    banner = '\nIMAPClient instance is "c"'

    def ipython_011(c):
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed(banner1=banner)
        ipshell('')

    def ipython_010(c):
        from IPython.Shell import IPShellEmbed
        IPShellEmbed('', banner=banner)()

    def builtin(c):
        import code
        code.interact(banner, local=dict(c=c))
    
    for shell_attempt in (ipython_011, ipython_010, builtin):
        try:
            shell_attempt(client)
            break
        except ImportError:
            pass

if __name__ == '__main__':
    main()
