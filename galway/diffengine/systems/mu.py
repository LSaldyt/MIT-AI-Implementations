from .system import System

def mu_branches(node):
    options = []
    if node.endswith('I'):
        options.append(node + 'U')
    options.append(node + node[1:])
    options.append(node.replace('III', 'U'))
    options.append(node.replace('UU', ''))
    return options

mu = System(mu_branches)
