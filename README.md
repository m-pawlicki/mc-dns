# DNS-IP Helper
This is a simple script to update the IP of a DNS using the command line.
# Usage
`python main.py [-IHS]`

  -I, --ipaddress IPADDRESS
                        IP address to apply, optional.
  -H, --hostname HOSTNAME
                        Target hostname, required.
  -S, --subdomain SUBDOMAIN
                        Target subdomain, optional.

If an IP address isn't provided, it'll pull the outgoing IP from the machine running the script.
If a subdomain isn't provided, the script will only pass in the hostname.