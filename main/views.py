from django.shortcuts import render
from Store_ranking.settings import *
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from main import models
from bs4 import BeautifulSoup
import requests
import json


def naver_api(keyword):
    url = 'https://openapi.naver.com/v1/search/shop.json?query='
    search = keyword
    url = url + search + '&display=50'
    res = requests.get(url, headers={'X-Naver-Client-Id': CLIENT_ID, 'X-Naver-Client-Secret': CLIENT_SECRET})
    dict_value = json.loads(res.text)
    select_value = dict_value["items"]

    return select_value


def actions(request):
    product_address = request.POST.get('product_address')
    action = request.POST.get('action')
    selected_product = request.POST.get('selected_product')

    if action == 'add-product':
        return add_product(product_address, request)

    elif action == 'show-page':
        return show_page(selected_product)

    elif action == 'delete-product':
        return delete_product(selected_product)

    elif action == 'modify-keyword':
        return modify_keyword(selected_product, request)

    elif action == 'search-start':
        return search_start(selected_product)

    return HttpResponseRedirect('/main/')


def main(request):
    products = models.Product.objects.all()
    keywords = []
    rank = []
    num = range(1, 11)

    if products.count() > 0:
        context = {"keywords": keywords, "range": num, "products": products, 'rank': rank}

    else:
        context = {"keywords": [], "range": num, "products": [], 'rank': []}

    return render(request, 'main/templates/title_table.html', context)


def selected(request):
    selected_product_id = request.POST.get('selected_id')
    selected_product = models.Product.objects.get(id=selected_product_id)
    keywords = selected_product.keywords.all()
    data = {}
    num = 1

    for keyword in keywords:
        data[str(num)] = keyword.name
        num += 1

    keywords_json = json.dumps(data)
    return HttpResponse(keywords_json)


def get_html(url):
    html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text

    return html


def add_product(url, request):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', {'class': '_copyable'})
    product_name = product.dt.strong.get_text()
    product_num = product.p.span.get_text()

    try:
        create_product_model = models.Product(name=product_name, address=url, num=product_num)
        create_product_model.save()
        for num in range(10):
            create_keyword_model = models.Keyword(name='', number=num+1, product=create_product_model)
            create_keyword_model.save()

    except IntegrityError:
        messages.error(request, '중복된 url입니다.')

    return HttpResponseRedirect('/main/')


def show_page(selected_product):
    instance = models.Product.objects.get(id=selected_product)
    url = instance.address

    return HttpResponseRedirect(url)


def delete_product(selected_product):
    instance = models.Product.objects.get(id=selected_product)
    instance.delete()

    return HttpResponseRedirect('/main/')


def modify_keyword(selected_product, request):

    keywords = [
        request.POST.get('keyword-name-1'),
        request.POST.get('keyword-name-2'),
        request.POST.get('keyword-name-3'),
        request.POST.get('keyword-name-4'),
        request.POST.get('keyword-name-5'),
        request.POST.get('keyword-name-6'),
        request.POST.get('keyword-name-7'),
        request.POST.get('keyword-name-8'),
        request.POST.get('keyword-name-9'),
        request.POST.get('keyword-name-10')]

    product = models.Product.objects.get(id=selected_product)
    product_keywords = models.Keyword.objects.filter(product=product)

    for index, keyword in enumerate(keywords):
        product_keyword = product_keywords[index]
        product_keyword.name = keyword
        product_keyword.save()

    return HttpResponseRedirect('/main/')


def product_ranking(request):

    selected_product_id = request.POST.get('selected_id')
    selected_product = models.Product.objects.get(id=selected_product_id)
    keywords = selected_product.keywords.all()
    rank_info = {}

    for keyword in keywords:
        ranks = []
        if len(keyword.name) > 0:
            keyword_ranks = models.Rank.objects.filter(keyword=keyword)
            if len(keyword_ranks) > 10:
                keyword_ranks = keyword_ranks[-10:]

            for keyword_rank in keyword_ranks:
                searched_date = str(keyword_rank.date_searched.date())
                ranks.append([searched_date, keyword_rank.rank])
            rank_info[keyword.name] = ranks

    ranks_json = json.dumps(rank_info)

    return HttpResponse(ranks_json)



def search_start(selected_product):
    product = models.Product.objects.get(id=selected_product)
    keywords = models.Keyword.objects.filter(product=product)

    for keyword in keywords:
        check = ''
        if len(keyword.name) > 0:
            keyword_info = naver_api(keyword.name)
            for rank, info in enumerate(keyword_info):
                changed_link = info['link']
                link_html = get_html(changed_link)
                if len(link_html) > 0:
                    product_url = link_html.split('\'')[1]
                    if product_url[8:18] == 'smartstore':
                        product_number_index = product_url.rfind('/')
                        product_number = product_url[product_number_index + 1:]
                        if product_number == product.num:
                            check = 'Y'
                            create_rank_model = models.Rank(product=product, keyword=keyword, rank=str(rank+1))
                            create_rank_model.save()

            if check == '':
                create_rank_model = models.Rank(product=product, keyword=keyword, rank='-')
                create_rank_model.save()


        else:
            create_rank_model = models.Rank(product=product, keyword=keyword, rank='-')
            create_rank_model.save()

    return HttpResponseRedirect('/main/')


def error_404(request):
    return render(request, 'main/templates/404.html')

