import argparse
import cloud
import json
import subprocess


def get_aks_witness(n):
    '''Shell out to aks-picloud-worker to test primality and return
    the result as a dictionary.
    '''
    result_str = subprocess.check_output(
        ['/home/picloud/src/aks-picloud/aks-picloud-worker/aks-picloud-worker',
         str(n)])
    result = json.loads(result_str)
    result['n'] = int(result['n'])
    result['r'] = int(result['r'])
    result['M'] = int(result['M'])
    result['start'] = int(result['start'])
    result['end'] = int(result['end'])
    if 'factor' in result:
        result['factor'] = int(result['factor'])
    if 'witness' in result:
        result['witness'] = int(result['witness'])
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Test primality via the AKS algorithm.')
    parser.add_argument('n', type=int, help='the number to test')
    args = parser.parse_args()

    print 'calling into PiCloud...'
    jid = cloud.call(get_aks_witness, args.n,
                     _env='aks', _label='get_aks_witness(%d)' % args.n)
    print 'waiting for results...'
    print cloud.result(jid)


if __name__ == '__main__':
    main()