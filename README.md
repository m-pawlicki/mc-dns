# DNS-IP Helper

This is a small python script to update the IP of a DNS using the command line. Requires python to be installed.

The environmental variable `CF_API_KEY` is _required_ to be set in order for the script to run. Uses Cloudflare API calls under the hood.

# Usage

`python main.py [-IHS]`

>`-I, --ipaddress`
>IP address to apply, optional.
>If an IP address isn't provided, it'll pull the outgoing IP from the machine running the script.

>`-H, --hostname`
>Target hostname, **required**.

>`-S, --subdomain`
>Target subdomain, optional.
>If a subdomain isn't provided, the script will only pass in the hostname.

# Examples

> ### Change IP of hostname
> `python main.py -H foo.bar`
> Sets foo.bar to the machine's outgoing IP address.


> ### Change IP of hostname with a subdomain
> `python main.py -H foo.bar -S baz`
> Sets baz.foo.bar to the machine's outgoing IP address.

> ### Set hostname with a custom IP
> `python main.py -I 1.1.1.1 -H foo.bar`
> Sets foo.bar's IP address to 1.1.1.1.
