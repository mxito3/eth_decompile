import json
def main(data=None, addr=None):

    if data == None:
        assert addr != None

        with open(f'../panoramix/cache_pan/{addr[:5]}/{addr}.json') as f:
            data = f.read()

    data = json.loads(data)
    addr = data['addr']
    print('\nExperimental auto-generated ABI')
    for k in ['addr', 'network']:
        v = data[k]
        if k!='functions':
            # print(f'{k}: {COLOR_BLUE}{v}{ENDC}')
            pass

    print('')
    print('Please note:')
    print('- function parameter names may be off')
    if 'tuple' in str(data['functions']):
        print('- tuple parameters are not handled properly')
#    print('- names of the following functions were not found: ')
    print()

    res = []

    problems = []

    funcs = data['functions']

    for fname in data['problems']:
        funcs.append({
                'name': fname,
                'hash': '0x00000000',
            })

    for f in funcs:

#        'const' -> pure
#        'nonpayable' -> nonpayable
#        'payable' -> payable

        name = f['name']
        if 'unknown' in name and '?' in name:
            problems.append(f['hash'])
            continue

        name, params = name.split('(')
        params = params[:-1].split(', ')

        if '0x' not in f['hash']:
            assert f['name'] == '_fallback()'

            func = {
                'type': 'fallback',
            }

        else:

            func = {
                'type': 'function',
                'name': name,
                'inputs': []
            }


        if 'const' in f and f['const']:
            func['stateMutability'] = 'pure'

        # todo: handle stateMutability: 'view'

        elif 'payable' in f and f['payable']:
            func['stateMutability'] = 'payable'

        elif 'hash' != '0x00000000':
            func['stateMutability'] = 'nonpayable'

        fparams = []
        for p in params:
            if p == '': 
                continue

            if ' ' not in p:
                func['inputs'].append(p)
            else:
                ptype, pname = p.split(' ')
                pname = pname[1:] # remove leading '_'

                func['inputs'].append({
                        'name': pname,
                        'type': ptype})

        res.append(func)


    if len(problems) > 0:
        print('Functions not included')
        for p in problems:
            print('- ' + p)
        print('(no signatures found)')
        print()
    print(res)

if __name__ == "__main__":
    main(data=None,addr='0x06012c8cf97BEaD5deAe237070F9587f8E7A266d')