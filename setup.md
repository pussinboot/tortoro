## prereqs

you will need to have both `tor` and `privoxy` installed

## tor config

open `/etc/tor/torrc` with your preferred editor

make sure to uncomment the lines for `ControlPort` and `HashedControlPassword`

to generate the password hash run `tor --hash-password YOUR_PASSWORD`

restart tor to apply the config changes

## privoxy config

open `/etc/privoxy/config` with your preferred editor

enable `forward-socks5t`

`forward-socks5t / localhost:9050`

now restart privoxy