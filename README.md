I use this script whenever I want to set up a fresh CS50 Appliance for
development. The main thing that's really nice about it is that,
together with add_passphrases.py, it sets up all of my SSH keys and
passphrases.

`setup.py` copies your whole `~/.ssh` directory to the appliance via `scp`
and also copies the `_setup.sh` script to the appliance, runs it, and then
removes it from the appliance. If there are any additional tasks that you want
to run on the appliance on setup, add them to `_setup.sh`.

`add_passphrases.py` reads an encrypted file named `.passphrases` of the format:
`<private-key-name>:<passphrase>` and adds all of the passphrases to the
appliance's `ssh-agent`. To run, you first need to create the encrypted file to
store your passphrases. `add_passphrases.py` expects the encrypted file to use
`openssl`'s AES-256-CBC algorithm with salt, so you can create it as follows:

$ openssl aes-256-cbc -salt -in <infile> -out .passphrases

If you omit the `-in` option, openssl will just read from `stdin`.

Then, to use `add_passphrases.py` with `setup.py`:

1. `cp add_passphrases.py ~/.ssh`.
2. `cp .passphrases ~/.ssh` (if you didn't create it there)
3. Run `setup.py`
4. From the appliance itself (not via SSH, which doesn't allow access to
`ssh-agent`), run `cd ~/.ssh ; ./add_passphrases.py`. You'll be prompted to
enter the same password that you used to encrypt your .passphrases file with
`openssl`.