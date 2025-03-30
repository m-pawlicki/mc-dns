# DNS-IP Helper

This is a simple script to update the IP of a DNS using the command line. 

The environmental variable `CF_API_KEY` is _required_ to be set in order for the script to run. Uses Cloudflare API calls under the hood.

# Usage

`python main.py [-IHS]`

`-I, --ipaddress`

IP address to apply, optional.

If an IP address isn't provided, it'll pull the outgoing IP from the machine running the script.

`-H, --hostname`

Target hostname, required.

`-S, --subdomain`

Target subdomain, optional.

If a subdomain isn't provided, the script will only pass in the hostname.

# Examples

`python main.py -H foo.bar -S baz`

baz.foo.bar -> machine's IP

`python main.py -H foo.bar`

foo.bar -> machine's IP

`python main.py -I 1.1.1.1 -H foo.bar`

foo.bar -> 1.1.1.1
