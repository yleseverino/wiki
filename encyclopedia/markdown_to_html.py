from cgitb import html
import re

def mk2html(markdown_text):

    html_text = convert_text(markdown_text)

    # Get the first h1 title    
    try:
        h1 = re.search('[\<h1\>]([^<]*)[\<\/h1\>]', html_text).group(1)
    except AttributeError:
        h1 = "Without title"

    return h1, html_text


def convert_text(markdown_text):

    html = convert_bolds_mk_to_html(markdown_text)
    html = convert_titles_mk_to_html(html)
    html = convert_anchors_mk_to_html(html)

    return convert_paragraphs_to_html(html)

def convert_bolds_mk_to_html(mk):
    '''Get the bold marks in the line'''

    bold_text = re.findall("[\*]{2}([^\*]*)[\*]{2}", mk)
    for bold in bold_text:
        mk = mk.replace(f'**{bold}**',f'<strong>{bold}</strong>',1)

    return mk

def convert_titles_mk_to_html(mk):
    '''Get titles'''
    titles = re.findall("([#]+)\s(.*)", mk) 
    for title in titles:

        '''Bug windows caracter \r\n'''
        title_text = title[1].replace('\r','')

        mk = mk.replace(f'{title[0]} {title_text}',f'<h{len(title[0])}>{title_text}</h{len(title[0])}>',1)

    return mk

def convert_anchors_mk_to_html(mk):
    '''Get anchors'''
    anchors = re.findall("[\[]([^\[]+)[\]][\(]([^)]+)[\)]", mk)
    for a in anchors:
        mk = mk.replace(f'[{a[0]}]({a[1]})',f'<a href="{a[1]}">{a[0]}</a>',1)
    return mk

def convert_paragraphs_to_html(mk):
    '''Separate de text in list with paragraphs'''
    html_list = mk.split(2*'\n')

    if len(html_list) == 1:
        html_list = mk.split(2*'\r\n')
    
    '''Add paragraphs and list'''
    for i in range(len(html_list)):

        html_list[i] = convert_list_to_html(html_list[i])

        "If not is a heading or list them is a paragraph"
        if not ( html_list[i][0:2] == '<h' or  html_list[i][0:2] == '<u' ) :
            html_list[i] = '<p>' + html_list[i]  + '</p>'
    
    html = ''.join(html_list)

    return html

def convert_list_to_html(mk_paragraph):
    '''Get a paragraph of list markdown and convert to list in HTML 
    if not a list just return it without change it'''

    list_elements = re.findall("[\*|\-|\+]\s(.*)\n*|\r\n*", mk_paragraph)
    print(list_elements)
    if list_elements:
        new_html_list = ['<ul>']
        for element in list_elements:
            new_html_list.append(f'<li>{element}</li>')
        new_html_list.append('</ul>')
        mk_paragraph = ''.join(new_html_list)
    
    return mk_paragraph
