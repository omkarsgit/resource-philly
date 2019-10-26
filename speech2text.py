import json
import requests
from bs4 import BeautifulSoup

def get_intent(text):
    headers = {
    'Authorization': 'EndpointKey c561db23-694a-4355-b6c8-89545d4fc929',
    'Content-type': 'application/json',
    }
    data = '{\'question\':\'' + text + '\'}'
    response = requests.post('https://philly-resouce.azurewebsites.net/qnamaker/knowledgebases/abbf2bf8-6d2b-4805-bc4d-8fb9d4e64db7/generateAnswer', headers=headers, data=data)
    j = json.loads(response.text)

    return j['answers'][0]['answer'], j['answers'][0]['score']



def make_request(criterion, gender, eligibility):
    cookies = {
            # 'client_location': '40.5118976%3A-74.440704',
            }

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            }

    params = (
            ('_wrapper_format', 'drupal_ajax'),
            )

    genders = {'Any': 'All', 'Female': '6', 'Gender Non-Binary': '17', 'Male': '5', 'Transgender': '16'}
    eligibilities = {'Any': 'All', 'Adult': '3', 'Children': '1', 'Families': '18', 'Senior': '4', 'Youth': '2'}
    criteria = {'food': '11', 'housing': '12'}

    data = {
            'field_service_gender_target_id': genders[gender],
            'field_age_elibility_target_id': eligibilities[eligibility],
            'field_available_value': '1',
            'a': '',
            'view_name': 'service_view',
            'view_display_id': 'page_3',
            'view_args': criteria[criterion],
            'view_path': '/views/ajax',
            'view_base_path': 'services/housing',
            'view_dom_id': 'fc26a9fb9c938458c467e7d50b3a6da91943923d29bfd0f78b895f07ae03cdd4',
            'pager_element': '0',
            '_drupal_ajax': '1',
            'ajax_page_state[theme]': 'link2',
            'ajax_page_state[theme_token]': '',
            'ajax_page_state[libraries]': 'better_exposed_filters/auto_submit,better_exposed_filters/general,bootstrap/popover,bootstrap/tooltip,core/html5shiv,geolocation/geolocation.proximity.html5,system/base,views/views.module,views_ajax_history/history'
            }

    response = requests.post('https://dev-link-love.pantheonsite.io/views/ajax', headers=headers, params=params, cookies=cookies, data=data)

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.post('https://dev-link-love.pantheonsite.io/views/ajax?_wrapper_format=drupal_ajax', headers=headers, cookies=cookies, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')
    j = json.loads(soup.textarea.string)
    soup = BeautifulSoup(j[2]['data'], 'html.parser')
    titles = soup.find_all("div", {"class": "location-name col-xs-7"})
    times = soup.find_all("div", {"class": "location-opens col-md-5"})
    locations = soup.find_all("div", {"class": "col-md-7"})

    food = []
    # print(len(titles))
    # print(len(times))
    # print(len(locations))

    for i in range(len(titles)):
        food.append((titles[i].string, times[i].div.string, locations[i].string, times[i].find("div", {"class": "open-now"}) is not None))
    print(len(food))
    return food

if __name__ == "__main__":
    a = input('Enter text: ')
    intent = get_intent(a)[0]
    b = input('Enter gender: ')
    c = input('Enter eligibility: ')
    print(make_request(intent, b, c))
