#!/usr/bin/env python
"""
Starts a command within a pty from a controlling process, which reads "keystrokes" from a fifo and forwards into the child.
User input may be forwarded to another fifo, instead of sending it into the child process' pty.

This way any terminal process waiting for user input can be controlled from outside.

USAGE: with_termcontrol [Params] COMMAND

- The fifo filename (`fn_fifo`) is available as `$STDIN_FIFO` within the child. All data on this fifo will be sent into the pty.
- If fn_fifo is set to 'auto' then we'll create a tempfile fifo
- If you configure a forward fifo (`fn_user`), then all _user_ input will be forwarded to it,
  instead of sending into the pty
- The program will block(!) until a reader is attached to that user fifo
- `fn_user` simply set to true will result in its filename set to `$STDIN_FIFO` + '.user' (and exported as `$USER_INPUT_FIFO`)
- Fifos will be created only if they don't exist at process start
- Fifos will be unlinked at exit only if they where created by us
"""

import os, sys, tempfile, termios, fcntl, pty, select, signal, struct, time, threading
from tty import setraw

cfg = dict(fn_user=False, fn_fifo='auto')
fd_pty = None
fd_tty_stdin = sys.stdin.fileno()
fd_tty_stdout = sys.stdout.fileno()

now = lambda: int(time.time() * 1000)
t0 = now()


def log(msg):
    with open('/tmp/pyteco.debug', 'a') as fd:
        fd.write(f'[{now()-t0:5}] {msg}\n')


class fifo_reader(threading.Thread):
    """fake keyboard input into the child - from a fifo, from outside"""

    def run(self):
        while 1:
            fd = os.open(cfg['fn_fifo'], os.O_RDONLY)
            s = os.read(fd, 1024)   # blocks, waiting
            into_pty(s) if s else None


def into_pty(data: bytes):
    for c in data:
        log(c)
    while data:
        n = os.write(fd_pty, data)
        data = data[n:]


def start_select_loop_over_input_fds():
    fd_inputs = [fd_pty, fd_tty_stdin]
    fn_user = cfg['fn_user']
    if fn_user:
        fd_user = os.open(fn_user, os.O_WRONLY)

    while True:
        try:
            polled_fds, _, _ = select.select(fd_inputs, [], [])
        except KeyboardInterrupt:
            break

        if fd_pty in polled_fds:
            # typing into the terminal:
            try:
                data = os.read(fd_pty, 1024)
            except OSError:
                data = 0
            if data:
                log(f'fd_pty {data}')
                os.write(fd_tty_stdout, data)
            else:
                return   # EOF, stop program

        if fd_tty_stdin in polled_fds:
            # piped into this parent process:
            data = os.read(fd_tty_stdin, 1024)
            if data:
                log(f'tty   {data} {fn_user}')
                if fn_user:
                    # blocks until reader present:
                    try:
                        os.write(fd_user, data)
                    except Exception as ex:
                        # reader gone (normally: parent process  closes and cleans up)
                        return
                else:
                    into_pty(data)
                continue
            # got EOF
            fd_inputs.remove(fd_tty_stdin)


def term_size_into_pty(signal=0, _=0):
    """called at beginning and when we(parent) get WINCH
    The forked pty has no idea about size changes, otherwise
    """
    if signal:
        assert signal == 28   # WINCH, we are signal handler
    if fd_pty is None:
        return
    try:
        cols, rows = os.get_terminal_size()
    except Exception as _:
        f = os.popen('stty size').read().strip()   # works in tee
        rows, cols = [int(i) for i in f.split()] if f else [25, 80]
    # https://stackoverflow.com/a/6420070/4583360 - and yes, the child gets sigwinch :-)
    size = struct.pack('HHHH', rows, cols, 0, 0)
    fcntl.ioctl(fd_pty, termios.TIOCSWINSZ, size)


def parse_args(args):
    ocfg = dict(cfg)
    while args and args[0].startswith('--'):
        arg = args.pop(0)[2:]
        k, v = arg.split('=', 1) if '=' in arg else (arg, True)
        cfg[k.replace('-', '_')] = v
    if cfg.get('help') or len(cfg) != len(ocfg):
        print(f'{__doc__}\nParams:')
        [print(f'--{k}[={v}]') for k, v in ocfg.items()]
        sys.exit(0 if cfg.get('help') else 1)
    return args


def make_fifos():
    fn_fifo = cfg['fn_fifo']
    if fn_fifo == 'auto':
        fn_fifo = cfg['fn_fifo'] = tempfile.NamedTemporaryFile().name
    fnf = cfg['fn_user']
    if fnf == True:
        fnf = cfg['fn_user'] = f'{fn_fifo}.user'
    fn_fifos = [fn_fifo, fnf]
    rm_after = []
    [
        os.mkfifo(fn) or rm_after.append(fn)
        for fn in fn_fifos
        if fn and not os.path.exists(fn)
    ]
    return rm_after, fn_fifos


def run(args):
    if 'STDIN_FIFO' in os.environ:
        print('Terminal already controlled. Refusing to nest', file=sys.stderr)
        sys.exit(1)
    args = parse_args(args[1:])
    global fd_pty
    if not args:
        args.append(os.environ.get('SHELL', '/bin/bash'))
    rm_after, fn_fifos = make_fifos()
    fifo_reader(daemon=True).start()
    os.environ['STDIN_FIFO'] = fn_fifos[0]
    if fn_fifos[1]:
        os.environ['USER_INPUT_FIFO'] = fn_fifos[1]

    signal.signal(signal.SIGWINCH, term_size_into_pty)

    pid, fd_pty = pty.fork()

    if pid == 0:
        # We are in forked pty, run the actual program therein, in a shell:
        cmd = ' '.join([f'"{i}"' for i in args])
        os.execvpe('sh', ['sh', '-c', cmd], os.environ)

    term_size_into_pty()
    try:
        cooked_attrs_before = termios.tcgetattr(fd_tty_stdin)
        setraw(fd_tty_stdin)
        was_cooked = True   # 'canonical mode'
    except termios.error:
        # e.g. when in a pipe we are already raw:
        was_cooked = False
    try:
        # blocking the master until EOF:
        start_select_loop_over_input_fds()
        os.close(fd_pty)
    finally:
        for fn in rm_after:
            os.unlink(fn) if fn and os.path.exists(fn) else 0
        if was_cooked:
            time.sleep(0.05)   # receive all into the term, before we switch back
            termios.tcsetattr(fd_tty_stdin, termios.TCSAFLUSH, cooked_attrs_before)

    os.waitpid(pid, 0)


main = lambda: run(sys.argv)

if __name__ == '__main__':
    main()
