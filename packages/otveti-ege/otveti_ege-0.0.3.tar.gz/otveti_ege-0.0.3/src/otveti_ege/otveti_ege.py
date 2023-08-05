import requests
from re import search


def otvet_pzh(problem, subject='inf'):
    url = f"https://{subject}-ege.sdamgia.ru/problem?id={problem}"
    resp = requests.get(url).text
    try:
        print(search(r'(Тип|Задания) \w*', resp).group(0))
    except AttributeError:
        print('Тип задания не найден')
    try:
        print(search(r'Ответ: \w*', resp).group(0))
    except AttributeError:
        print('Ответ не найден')


if __name__ == "__main__":
    while True:
        otvet_pzh(input())
