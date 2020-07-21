#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    for item in tags:
        print("{}:".format(item), tags[item])

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
    ask_submits()
    rate_diff = ask_rate_diff()
