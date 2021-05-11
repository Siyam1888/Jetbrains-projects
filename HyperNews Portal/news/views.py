from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from itertools import count
import json

news_json_path = 'C:\\Users\\Administrator\\python_projects\\HyperNews Portal\\HyperNews Portal\\task\\news.json'

posts = json.load(open(news_json_path))
counter = 4

# for group in grouped_posts:
#     print(group)
#     for post in grouped_posts[group]:
#         print(post['link'])


# Create your views here.
def hello(request):
    return redirect('home')


def index(request):
    posts = json.load(open(news_json_path))

    if request.method == 'GET':
        filtered_posts = []
        query = request.GET.get('q')
        if query:
            for post in posts:
                if query in post['title']:
                    filtered_posts.append(post)
            filtered_posts = {'groups': group_by_date(filtered_posts)}
            return render(request, 'news/index.html', context=filtered_posts)

    posts = {'groups': group_by_date(posts)}
    return render(request, 'news/index.html', context=posts)


def news(request, link):
    posts = json.load(open(news_json_path))
    context = None

    for post in posts:
        if post['link'] == int(link):
            context = post

    return render(request, 'news/news.html', context=context)


def create(request):
    global counter

    # declaring the variables necessary for a post
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.now()
        created_str = created.strftime('%Y-%m-%d %H:%M:%S')
        link = counter
        counter += 1

        posts = json.load(open(news_json_path))
        post = {"created": created_str, "text": text, "title": title, "link": link}
        posts.append(post)

        json.dump(posts, open(news_json_path, 'w'))

        return redirect('home')
    return render(request, 'news/create.html')


def group_by_date(posts):
    # grouping the posts by date
    created_times = []
    for post in posts:
        created = datetime.strptime(post['created'], '%Y-%m-%d %H:%M:%S')
        created_times.append(created)

    sorted_times = list(reversed(sorted(created_times)))
    grouped_posts = dict()
    # print(sorted_times)
    for date in sorted_times:
        str_date = date.strftime('%Y-%m-%d')
        grouped_posts[str_date] = []

    for date in sorted_times:
        str_date = date.strftime('%Y-%m-%d')
        for post in posts:
            created_date = datetime.strptime(post['created'], '%Y-%m-%d %H:%M:%S')
            if date == created_date:
                grouped_posts[str_date].append(post)

    return grouped_posts


