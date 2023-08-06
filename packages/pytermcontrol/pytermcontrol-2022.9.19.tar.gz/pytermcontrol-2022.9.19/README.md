# PyTermControl

Python only version of https://github.com/axiros/termcontrol

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

Params:
--fn_user[=False]
--fn_fifo[=auto]
