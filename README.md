# DNS-IP Helper

Our personal server's IP kept changing and breaking the domain so I wrote something to help update the IP on the provided entries on Cloudflare and if it doesn't find an entry, will make one for you! Comes with a cache with a timeout to curb excessive API calls because how often does the IP change, anyway?

Requires Python to run. Now comes with its own Dockerfile for easy building and deployment!

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

# Contributing
If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
