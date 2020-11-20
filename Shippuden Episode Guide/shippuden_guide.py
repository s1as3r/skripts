from sys import argv as args
from requests import get
from bs4 import BeautifulSoup


help_notice = '''
Shippuden Episode Guide.

Gives the name of an episode and its type. (Filler/Cannon)

Provide the script with arguments.
Arguments must be numbers or a range seperated by '-'.

Example Usage:
    >>> python guide.py 100
    >>> python guide.py 100-200
    >>> python guide.py 100 101 102 105
'''

filler = [
    28,  170, 171, 257, 258, 259, 260, 271, 279, 280, 281, 376,
    377, 388, 389, 390, 416, 417, 422, 423, 480, 481, 482, 483,
    *list(range(303, 321)), *list(range(144, 152)), *list(range(176, 197)),
    *list(range(223, 243)), *list(range(347, 362)), *list(range(427, 451)),
    *list(range(394, 414)), *list(range(284, 296)), *list(range(464, 470)),
    *list(range(57, 72)),   *list(range(91, 113))
]


def get_ep_name(ep_no: int) -> str:
    ep_url = 'https://en.wikipedia.org/wiki/List_of_Naruto:_Shippuden_episodes'

    soup = BeautifulSoup(get(ep_url).text, 'html.parser')
    ep = soup.find(id=f'ep{ep_no}').findNext().next[1:-1]

    return ep


def print_episode(ep):
    if ep in filler:
        print(f'{ep:<5} - {get_ep_name(ep):<65} - Filler')
        return

    print(f'{ep:<5} - {get_ep_name(ep):<65} - Canon')
    return


if __name__ == '__main__':
    if len(args) > 1:
        print(f'\n{"No.":<5} - {"Episode Name":<65} - Type\n')

        for i in args[1:]:
            if '-' in i:
                rng = [int(j) for j in i.split('-')]
                for k in range(rng[0], rng[1]+1):
                    print_episode(k)
            else:
                print_episode(int(i))
    else:
        print(help_notice)

    print('\n')
