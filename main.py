#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import requests
import time

api = "http://codeforces.com/api/"
profile = {}
last_call = 0
verdicts = {}
tags = {}
languages = {}
attempted = []
solved = []


def sort_dict(data):
    temp = [[k, v] for k, v in data.items()]
    temp.sort(key=lambda i: -i[1])
    return temp


def call(link):
    global last_call
    while time.time() - last_call < 0.25:
        time.sleep(0.1)
    last_call = time.time()
    return requests.Session().get(link).json()


def check_handle(handle):
    link = api + "user.info?handles=" + handle
    response = call(link)
    if response['status'] == 'OK':
        return 'OK'
    else:
        return response['comment']


def draw_pie(name_path, data, name, legend):
    def my_pct(i):
        if i > 5:
            return str(int(i * 10) / 10) + "%"

    def my_label(i):
        if 100 * sizes[i] / sum(sizes) > 5:
            return labels[i]
        else:
            return ""

    data = sort_dict(data)
    labels = [item[0] for item in data]
    sizes = [item[1] for item in data]
    explode = [0 for i in range(len(labels))]
    if len(explode) > 2:
        explode[1] = 0.1
    fig, ax = plt.subplots()
    wedges, text, autotexts = ax.pie(sizes, explode=explode,
                                     labels=[my_label(i) for i in range(len(labels))],
                                     autopct=my_pct)
    for i in range(len(labels)):
        labels[i] += " (" + str(sizes[i]) + ")"
    if len(labels) > 5:
        labels = labels[0:5]
    ax.legend(wedges, labels,
              title=legend,
              bbox_to_anchor=(0.3, 0.3))
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title(name)
    plt.savefig('temp/{}.png'.format(name_path))


def process_submits(name_path):
    global verdicts, tags, languages, attempted, solved

    link = api + "user.status?handle=" + profile['handle']
    response = call(link)
    if response['status'] != 'OK':
        print(response['comment'])
        return
    response = response['result']

    verdicts = {}
    tags = {}
    languages = {}
    attempted = []
    solved = []

    for submit in response:
        problem = submit['problem']
        attempted.append(problem['name'])
        if submit['programmingLanguage']:
            if submit['programmingLanguage'] in languages:
                languages[submit['programmingLanguage']] += 1
            else:
                languages[submit['programmingLanguage']] = 1
        if submit['verdict']:
            if submit['verdict'] in verdicts:
                verdicts[submit['verdict']] += 1
            else:
                verdicts[submit['verdict']] = 1
            if submit['verdict'] == 'OK' and submit['problem']:
                solved.append(problem['name'])
        if submit['problem']:
            if problem['tags']:
                for tag in problem['tags']:
                    if tag in tags:
                        tags[tag] += 1
                    else:
                        tags[tag] = 1

    attempted = list(dict.fromkeys(attempted))
    solved = list(dict.fromkeys(solved))

    # print("number of attempted tasks:", len(attempted))
    # print("number of solved tasks:", len(solved))
    # print(tags)
    # print(languages)

    draw_pie("0" + name_path, languages, "Статистика по языкам программирования", "Языки программирования")
    draw_pie("1" + name_path, tags, "Статистика по задачам", "Тэги")
    draw_pie("2" + name_path, verdicts, "Статистика по вердиктам", "Вердикты")

    return response


def main(handle, name_path):
    global last_call, profile
    last_call = time.time()
    profile = call(api + "user.info?handles=" + handle)['result'][0]
    process_submits(name_path)
