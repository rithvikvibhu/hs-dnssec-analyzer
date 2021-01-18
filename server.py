from flask import Flask, render_template, request
import re
import traceback
import functions

app = Flask(__name__)


# Home Page
@app.route('/')
def Home():
    return render_template('home.html')


# Analyze Page
@app.route('/analyze/<domain>', methods=['GET'])
def Analyze(domain):
    return render_template('analyze.html', **{'domain': domain})


# The actual data request on Analyze Page
@app.route('/analysis', methods=['POST'])
def Analysis():
    domain = request.get_json()['domain'].rstrip('/')

    if domain is None or not is_valid_hostname(domain):
        return 'Invalid domain'

    try:
        probe_data = functions.create_probe_data(domain)
        graph_data = functions.graph_data(domain, probe_data)
        print_data = functions.query_data(domain, probe_data)
        delv_data = functions.delv_data(domain)
    except Exception:
        traceback.print_exc()
        return 'Something went wrong. Refresh to try again.'

    graph_data = re.sub('''[^"']*share\/dnsviz''',
                        '/static/dnsviz', graph_data)
    print_data = print_data.replace('\\n', '\n')

    context = {
        'domain': domain,
        'graph_data': graph_data,
        'print_data': print_data,
        'delv_data': delv_data,
    }
    return context


def is_valid_hostname(hostname):
    # Source: https://stackoverflow.com/a/2532344/1724828
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))
