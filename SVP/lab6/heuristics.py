def h1(node, dims):
    ''' Overestimating Heuristic '''
    indices = node.indices
    if len(indices) <= 0:
        return 0
    val = dims[indices[0]]
    for i in indices:
        val = val * dims[i+1]
    return val * len(indices)

def h2(node, dims):
    ''' Underestimating Heuristic '''
    x = min(dims)
    return x ** 3 * (len(node.indices)-2)