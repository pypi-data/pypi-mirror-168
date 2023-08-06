import sys, os
from threading import Thread

env = os.environ

n = lambda msg: os.system(
    f'notify-send {msg if isinstance(msg, str) else msg.decode("utf-8") }'
)   # dbg


class Fifos(Thread):
    fn_fifo = fn_user = handler = None

    def run(self):
        fd_fifo = os.open(self.fn_fifo, os.O_WRONLY)
        fd_user = os.open(self.fn_user, os.O_RDONLY)

        def send(data, fd=fd_fifo):
            os.write(fd, data)

        h = self.handler
        while True:
            d = os.read(fd_user, 1024)
            if d:
                h(d, send)
                continue
            break   # EOF


join_argv = lambda argv: ' '.join([f'"{k}"' for k in argv])


def restart(fn_fifo='auto', handle_user_input=None):

    env_fn_fifo, fn_user = env.get('STDIN_FIFO'), env.get('USER_INPUT_FIFO')
    if not env_fn_fifo:
        a = join_argv(sys.argv)
        user = '' if not handle_user_input else '--fn_user'
        # TODO: test fork
        sys.exit(os.system(f'with_termcontrol --fn_fifo="{fn_fifo}" {user} {a}'))

    if handle_user_input:
        assert fn_user
        t = Fifos(daemon=True)
        t.fn_user = fn_user
        t.fn_fifo = env_fn_fifo
        t.handler = handle_user_input

    t.start()
