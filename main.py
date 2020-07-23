#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import requests
import time


def call(link):
    global last_call
    while time.time() - last_call < 0.25:
        time.sleep(0.1)
    last_call = time.time()
    return cur_sess.get(link).json()


def ask_profile():
    while True:
        # handle = input()
        handle = open("data.txt", "r").readline()
        link = api + "user.info?handles=" + handle
        response = call(link)
        if response['status'] == 'OK':
            break
        else:
            print(response['comment'])
    response = response['result'][0]
    return response


def draw_pie(languages, name, legend):
    languages = [[k, v] for k, v in languages.items()]
    languages.sort(key=lambda i: -i[1])
    print(languages)
    labels = [item[0] for item in languages]
    sizes = [item[1] for item in languages]
    explode = [0 for i in range(len(labels))]
    if len(explode) > 2:
        explode[1] = 0.1

    fig, ax = plt.subplots()

    def my_pct(i):
        if i > 5:
            return str(int(i * 10) / 10) + "%"

    def my_label(i):
        if 100 * sizes[i] / sum(sizes) > 5:
            return labels[i]
        else:
            return ""

    wedges, text, autotexts = ax.pie(sizes, explode=explode,
                                     labels=[my_label(i) for i in range(len(labels))],
                                     autopct=my_pct)

    for i in range(len(labels)):
        labels[i] += " (" + str(sizes[i]) + ")"

    if len(labels) > 5:
        labels = labels[0:5]

    ax.legend(wedges, labels,
              title = legend,
              bbox_to_anchor = (0.1, 0.1))

    plt.setp(autotexts, size=10, weight="bold")

    ax.set_title(name)

    plt.show()


def ask_submits():
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

    print("number of attempted tasks:", len(attempted))
    print("number of solved tasks:", len(solved))

    print(tags)

    draw_pie(languages, "Language of submits statistics", "Programming languages")
    draw_pie(tags, "Tasks statistics", "Tags")
    draw_pie(verdicts, "Verdicts statistics", "Verdicts")

    return response


def ask_rate_diff():
    link = api + "user.rating?handle=" + profile['handle']
    response = call(link)
    if response['status'] != 'OK':
        print(response['comment'])
        return
    response = response['result']
    return response


with requests.Session() as cur_sess:
    api = "http://codeforces.com/api/"
    last_call = time.time()
    profile = ask_profile()
    submits = ask_submits()
    rate_diff = ask_rate_diff()
