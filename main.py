#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import requests
import time
import io


def build_str(data):
    result = ""
    for item in data:
        result += "{}: {}\n".format(item[0], item[1])
    return result


def sort_dict(data):
    temp = [[k, v] for k, v in data.items()]
    temp.sort(key=lambda i: -i[1])
    return temp


def draw_pie(data, figure_name, legend_name):
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
    explode = [0] * len(labels)
    if len(explode) > 2:
        explode[1] = 0.1

    fig, ax = plt.subplots()
    wedges, text, autotexts = ax.pie(x=sizes,
                                     explode=explode,
                                     labels=[my_label(i) for i in range(len(labels))],
                                     autopct=my_pct)

    for i in range(len(labels)):
        labels[i] += " (" + str(sizes[i]) + ")"
    if len(labels) > 5:
        labels = labels[0:5]

    ax.legend(handles=wedges,
              labels=labels,
              title=legend_name,
              bbox_to_anchor=(0.3, 0.3))
    plt.setp(autotexts,
             size=10,
             weight="bold")
    ax.set_title(figure_name)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer


class User:
    api = "http://codeforces.com/api/"
    last_call = 0
    profile = {}
    verdicts = {}
    tags = {}
    languages = {}
    attempted = []
    solved = []

    def call(self, link):
        while time.time() - self.last_call < 0.25:
            time.sleep(0.1)
        self.last_call = time.time()
        return requests.Session().get(link).json()

    def __init__(self, handle):
        self.last_call = 0
        self.profile = {}
        self.verdicts = {}
        self.tags = {}
        self.languages = {}
        self.attempted = []
        self.solved = []

        link = self.api + "user.info?handles=" + handle
        response = self.call(link)
        if response['status'] == 'OK':
            self.profile = response['result'][0]
        else:
            self.profile = None

    def build(self):
        link = self.api + "user.status?handle=" + self.profile['handle']
        if self.call(link)['status'] != 'OK':
            return False
        response = self.call(link)['result']

        for submit in response:
            problem = submit['problem']
            self.attempted.append(problem['name'])
            if submit['programmingLanguage']:
                if submit['programmingLanguage'] in self.languages:
                    self.languages[submit['programmingLanguage']] += 1
                else:
                    self.languages[submit['programmingLanguage']] = 1
            if submit['verdict']:
                if submit['verdict'] in self.verdicts:
                    self.verdicts[submit['verdict']] += 1
                else:
                    self.verdicts[submit['verdict']] = 1
                if submit['verdict'] == 'OK' and submit['problem']:
                    self.solved.append(problem['name'])
            if submit['problem']:
                if problem['tags']:
                    for tag in problem['tags']:
                        if tag in self.tags:
                            self.tags[tag] += 1
                        else:
                            self.tags[tag] = 1

        self.attempted = list(dict.fromkeys(self.attempted))
        self.solved = list(dict.fromkeys(self.solved))

        return True
