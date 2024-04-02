import requests
import bs4
import json
from fake_headers import Headers




def get_headers():
    return Headers(os='win', browser='chrome').generate()


def load_data_to_json_file(data):
    with open('vacancies_data', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)




if __name__ == '__main__':
    Url = 'https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&text=NAME%3Apython+and+DESCRIPTION%3ADjango+and+Flask&order_by=publication_time'
    response = requests.get(Url, headers = get_headers())
    main_html_data = response.text
    main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')
    tag_main_vacancy_serp_content = main_soup.find('main',
                                             class_='vacancy-serp-content')
    vacancies_tags = tag_main_vacancy_serp_content.find_all('div',
                                           class_='serp-item serp-item_link')
    parsed_data = []
    for vacancy_tag in vacancies_tags:
        h3_tag = vacancy_tag.find('h3',
                                  class_='bloko-header-section-3')
        a_tag = h3_tag.find('a')
        link = a_tag['href']
        salary = vacancy_tag.find('span',
                                  class_='bloko-header-section-2')
        try:
            salary_text = salary.text.replace('\xa0', ' ').replace(' ', ' ')
        except AttributeError:
            salary_text = ''
        vacancy_serp_item_company = vacancy_tag.find('div',
                                  class_='vacancy-serp-item-company')
        vacancy_item_company_info = vacancy_serp_item_company.find('div',
                                                    class_='vacancy-serp-item__info')
        vacancy_company = vacancy_item_company_info.find('div',
                                class_='bloko-v-spacing-container bloko-v-spacing-container_base-2')
        vacancy_company_text = vacancy_company.find('div',
                class_='bloko-text').text.replace('\xa0', ' ').replace(' ', ' ')
        vacancy_city_text = vacancy_item_company_info.find('div',
                            {'data-qa': 'vacancy-serp__vacancy-address',
                            }).text.replace('\xa0', ' ').replace(' ', ' ')
        parsed_data.append({
            'link': link,
            'salary': salary_text,
            'company_name': vacancy_company_text,
            'location': vacancy_city_text
        })

    load_data_to_json_file(parsed_data)
