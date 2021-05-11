import requests
import sys
from bs4 import BeautifulSoup

# global variables
languages = {'1': 'Arabic', '2': 'German', '3': 'English', '4': 'Spanish', '5': 'French', '6': 'Hebrew',
             '7': 'Japanese', '8': 'Dutch', '9': 'Polish', '10': 'Portuguese', '11': 'Romanian',
             '12': 'Russian', '13': 'Turkish'}

session = requests.Session()
Http404 = False
word = ''


def meanings(limit, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    # soup = soup.prettify()
    translations_div = soup.find('div', {'id': 'translations-content'})
    a_tags = translations_div.find_all('a', {'class': 'translation'})
    translated_words = [a.text.strip() for a in a_tags][:limit]
    formatted_words = [word.strip("'").strip('"').strip(',') for word in translated_words]
    return '\n'.join(translated_words)


def examples(limit, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    examples_section = soup.find('section', {'id': 'examples-content'})
    example_spans = examples_section.find_all('span', {'class': 'text'})

    example_texts = [span.text.strip() for span in example_spans][:limit * 2]

    english_texts = [text.strip("'").strip('"').strip(',') for text in example_texts[::2]]
    french_texts = [text.strip("'").strip('"').strip(',') for text in example_texts[1::2]]
    zipped_examples = zip(english_texts, french_texts)

    formatted_examples = """"""
    for en, fr in zipped_examples:
        formatted_examples += (en + '\n' + fr + '\n\n')

    return formatted_examples


def user_input():
    print('Type "en" if you want to translate from French into English,'
          ' or "fr" if you want to translate from English into French:')
    language = input()
    print("Type the word you want to translate:")
    word = input()
    print(f'You chose "{language}" as the language to translate "{word}".')


def generate_url(language1, language2, word):
    language1, language2, word = language1.lower(), language2.lower(), word.lower()
    language_direction = f'{language1}-{language2}'
    add_to_url = language_direction + '/' + word
    url = 'https://context.reverso.net/translation/' + add_to_url
    return url


def get_response(url):
    user_agent = 'Mozilla/5.0'
    try:
        session.headers.update({'User-Agent': user_agent})
        response = session.get(url)
        return response
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")


def list_languages(languages):
    for index, language in languages.items():
        print(f"{index}. {language}")


def main():
    global word
    # print("Hello, you're welcome to the translator. Translator supports: ")
    # list_languages(languages)
    # language1 = input("Type the number of your language:\n").strip()
    # language2 = input("Type the number of a language you want to translate to or '0' to translate to all languages:\n").strip()
    #
    # language1 = languages[language1]
    # language2 = languages[language2] if language2 != '0' else 'all'
    # word = input("Type the word you want to translate:\n").strip().lower()

    # adding command line arguments
    args = sys.argv
    language1, language2, word = args[1].lower(), args[2].lower(), args[3].lower()

    if language2 != 'all':
        if language2.capitalize() in languages.values():
            url = generate_url(language1, language2, word)
            response = get_response(url)
            result(language2, response, 5)
        else:
            print(f"Sorry, the program doesn't support {language2}")

    else:
        languages_list = list(languages.values())
        languages_list.remove(language1.capitalize())
        for language in languages_list:
            url = generate_url(language1, language, word)

            response = get_response(url)
            output = result(language, response, 1)
            if output:
                with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                    f.write(output)


def result(language2, response, limit):
    global Http404

    assert isinstance(int(limit), int), 'limit should be a number'
    if response.ok:
        print(f"{language2} Translations:")
        print(meanings(limit, response) + '\n')
        print(f"{language2} Examples:")
        print(examples(limit, response))
        output = f"""
{language2} Translations:
{meanings(limit, response)}

{language2} Examples:
{examples(limit, response)}
"""
        return output
    elif response.status_code == 404:
        Http404 = True
    else:
        print("Sorry, could not connect to the server")


main()
if Http404:
    print(f"Sorry, unable to find {word}")