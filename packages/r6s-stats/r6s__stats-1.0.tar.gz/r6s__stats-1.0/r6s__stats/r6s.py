import requests
from bs4 import BeautifulSoup as BS


def R6S(nickname):
    r6s = requests.get(f"https://r6.tracker.network/profile/pc/{nickname}")
    html = BS(r6s.content, "html.parser")

    r6s_op = requests.get(f"https://r6.tracker.network/profile/pc/{nickname}/operators")
    html_op = BS(r6s_op.content, "html.parser")

    best_mmr_find = str(html.find("div", class_="trn-defstat__value-stylized").contents[0]).strip()
    mmr = float(best_mmr_find.replace(",", "."))
    mmr_name = html.findAll("tspan")[0].text.strip()
    mmr_score = html.findAll("tspan")[1].text.strip()

    rank = 'UNKNOWN'
    if mmr >= 5.000:
        rank = 'CHAMPION'
    if mmr < 5.000:
        rank = 'DIAMOND'
    if mmr < 4.400:
        rank = 'PLAT 1'
    if mmr < 4.000:
        rank = 'PLAT 2'
    if mmr < 3.600:
        rank = 'PLAT 3'
    if mmr < 3.200:
        rank = 'GOLD 1'
    if mmr < 3.000:
        rank = 'GOLD 2'
    if mmr < 2.800:
        rank = 'GOLD 3'
    if mmr < 2.600:
        rank = 'SILVER 1'
    if mmr < 2.500:
        rank = 'SILVER 2'
    if mmr < 2.400:
        rank = 'SILVER 3'
    if mmr < 2.300:
        rank = 'SILVER 4'
    if mmr < 2.200:
        rank = 'SILVER 5'
    if mmr < 2.100:
        rank = 'BRONZE 1'
    if mmr < 2.000:
        rank = 'BRONZE 2'
    if mmr < 1.900:
        rank = 'BRONZE 3'
    if mmr < 1.800:
        rank = 'BRONZE 4'
    if mmr < 1.700:
        rank = 'BRONZE 5'
    if mmr < 1.600:
        rank = 'COPPER 1'
    if mmr < 1.500:
        rank = 'COPPER 2'
    if mmr < 1.400:
        rank = 'COPPER 3'
    if mmr < 1.300:
        rank = 'COPPER 4'
    if mmr < 1.200:
        rank = 'COPPER 5'

    return f"""
Нік: {html.find("span", class_="trn-profile-header__name").text.strip()} 
Кількість переглядів: {html.find("span", class_="trn-profile-header__views trn-text--dimmed").text.split()[0].strip()} 
Кращий ммр: {mmr} : {rank} 
Нинішній ммр: {mmr_score} : {mmr_name} 
K/D рейтинг: {html.findAll("div", class_="trn-defstat__value")[28].text.strip()} 
W/L рейтинг: {html.findAll("div", class_="trn-defstat__value")[27].text.strip()} 
Зіграні матчі:  {html.findAll("div", class_="trn-defstat__value")[24].text.strip()} 
Мейн атаки: {html_op.findAll("span")[25].text.strip()} 
Мейн захисту: {html_op.findAll("span")[87].text.strip()}
Сайт: https://r6.tracker.network/profile/pc/{nickname}
"""
