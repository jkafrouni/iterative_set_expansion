

def check_arguments(args):
    """
    Makes sure that 4 arguments are passed, and that:
        args[0] = r: int between 0 and 4
        args[1] = t: float between 0 and 1, extraction confidence threshold
        args[2] = q: string, seed query of plausible tuple
        args[3] = k: int greater than 0, number of tuples wanted
    """
    if len(args) < 4:
        raise Exception('Use: python -m iterative_set_expansion <r> <t> <q> <k>')

    r, t, q, k = args

    try:
        r = int(r)
        t = float(t)
        k = int(k)
    except Exception:
        raise Exception('Required types: <r> int, <t> float, <q> string, <k> int')

    if r not in range(1,5):
        raise Exception('<r> needs to be an int between 1 and 4, for Live_In (1), Located_In (2), OrgBased_In (3), Work_For (4)')

    if t < 0 or t > 1:
        raise Exception('<t> needs to be a float between 0 and 1')

    if not isinstance(q, str):
        raise Exception('<q> needs to be a string')

    if not isinstance(k, int) or k < 0:
        raise Exception('<k> needs to be a positive integer')

    return r, t, q, k

def print_arguments(r, t, q, k):
    
    print('Parameters:')
    print('Relation \t =', {1: 'Live_In', 2: 'Located_In', 3: 'OrgBased_In', 4: 'Work_For'}[r])
    print('Threshold \t =', t)
    print('Query \t\t =', q)
    print('# of Tuples \t =', k)

def any_two(iterable):
    """Similar to the built-in function any except it retains True if an iterable is True (at least) twice (and not only at least once)"""
    return (len([i for i in iterable if i]) > 1)

def sentence_to_string(sentence):
    words = [t.word for t in sentence.tokens]
    words = [w if w != '-LSB-' else '[' for w in words]
    words = [w if w != '-RSB-' else ']' for w in words]
    return ' '.join(words)
