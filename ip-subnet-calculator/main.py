from conversors import SubnetCalc

if __name__ == "__main__":
    ipv4 = SubnetCalc('192.168.0.25', cidr=12)

    print(f'Address: {ipv4.address}\n'
          f'Netmask: {ipv4.net} = {ipv4.cidr}\n'
          f'Wildcard: {ipv4.wildcard}\n'
          f'=>\n'
          f'Network: {ipv4.network}/{ipv4.cidr}\n'
          f'Broadcast: {ipv4.broadcast} \n'
          f'HostsMin: {ipv4.hostmin} \n'
          f'HostsMax: {ipv4.hostmax} \n'
          f'Hosts/Net: {ipv4.hosts_number}')