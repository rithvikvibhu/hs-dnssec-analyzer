import subprocess

# DNS_SERVER = ('dns.resolvr.info', 53)     # Resolvr
# DNS_SERVER = ('1.1.1.1', 53)              # Cloudflare
# DNS_SERVER = ('192.168.0.55', 53)         # Pi-Hole -> Hnsd
DNS_SERVER = ('192.168.0.55', 53530)      # Hnsd


def create_probe_data(domain):
    out = subprocess.check_output(
        ['dnsviz', 'probe', '-s', f'{DNS_SERVER[0]}:{str(DNS_SERVER[1])}', domain])
    print('PROBE length:', len(out))
    return out


def graph_data(domain, probe_data):
    out = subprocess.check_output(
        ['dnsviz', 'graph', '-Thtml', '-t', 'trusted-keys.txt'], input=probe_data)
    return out.decode('utf-8')


def query_data(domain, probe_data):
    out = subprocess.check_output(
        ['dnsviz', 'print', '-t', 'trusted-keys.txt'], input=probe_data, stderr=subprocess.STDOUT)
    out = out.decode('utf-8')

    print('QUERY length:', len(out))
    print(out)

    html_data = ''
    for line in out.splitlines():
        if line.lstrip().startswith("[."):
            html_data += f'<span class="text-green-600">{line}</span>'
        elif line.lstrip().startswith("[?"):
            html_data += f'<span class="text-yellow-600">{line}</span>'
        elif line.lstrip().startswith("W:"):
            html_data += f'<span class="text-yellow-600">{line}</span>'
        elif line.lstrip().startswith("[!"):
            html_data += f'<span class="text-red-700">{line}</span>'
        elif line.lstrip().startswith("E:"):
            html_data += f'<span class="text-red-700">{line}</span>'
        else:
            html_data += f'<span>{line}</span>'
        html_data += '\n'
    return html_data


def delv_data(domain):
    out = subprocess.check_output(
        ['delv', f'@{DNS_SERVER[0]}', '-p', str(DNS_SERVER[1]), '-a', 'hsd-ksk', domain, 'A', '+rtrace', '+vtrace'], stderr=subprocess.STDOUT)
    return out.decode('utf-8')
