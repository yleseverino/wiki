import re

def mk2html(markdown_text):
    'A function the performs a change from Markdown to HTML'

    
    '''First is removed the \r caracter in texts that are written in DOS system like windows
    Because can cause wrong behaves in the convetion
    
    Mor information in https://en.wikipedia.org/wiki/Newline
    '''
    html = markdown_text.replace('\r','') 
    html = convert_bolds_mk_to_html(html)
    html = convert_headings_mk_to_html(html)
    html = convert_anchors_mk_to_html(html)

    return convert_paragraphs_to_html(html)

def convert_bolds_mk_to_html(mk):
    '''Get the bold marks in markdown and replace for <strong> tags in html'''
    return re.sub(
                    pattern = r"[\*]{2}([^\*]*)[\*]{2}",                                # Pattern in regex used to find the tex
                    repl = lambda matchobj : f'<strong>{matchobj.group(1)}</strong>',   # A function that return the string with a part os the string matched and will replace where the pattern matched
                    string = mk                                                         # The text where will be search the pattern
                    )

def convert_headings_mk_to_html(mk):
    '''Get the Headings in Markdown and convert to HTML'''
    return re.sub(
                    pattern = r"([#]+)\s(.*)",                                                                                  # Pattern in regex used to find the tex
                    repl = lambda matchobj : f'<h{len(matchobj.group(1))}>{matchobj.group(2)}</h{len(matchobj.group(1))}>',     # A function that return the string with a part os the string matched and will replace where the pattern matched
                    string = mk                                                                                                 # The text where will be search the pattern
                    )

def convert_anchors_mk_to_html(mk):
    '''Get the Headings in Markdown and convert to HTML'''
    return re.sub(
                    pattern = r"[\[]([^\[]+)[\]][\(]([^)]+)[\)]",                                                                               
                    repl = lambda matchobj : f'<a href="{matchobj.group(2)}">{matchobj.group(1)}</a>',     
                    string = mk                                                                                               
                    )

def convert_paragraphs_to_html(mk):
    '''Separate de text in list with paragraphs'''
    html_list = mk.split(2*'\n')
    
    '''Add paragraphs and list'''
    for i in range(len(html_list)):

        html_list[i] = convert_ul_list_to_html(html_list[i])

        "If not is a heading or list them is a paragraph"
        if not ( html_list[i][0:2] == '<h' or  html_list[i][0:2] == '<u' ) :
            html_list[i] = '<p>' + html_list[i]  + '</p>'
    
    html = ''.join(html_list)

    return html

def convert_ul_list_to_html(mk_paragraph):
    '''Convert unordered list from markdown to HTML'''

    list_elements = re.findall("[\*|\-|\+]\s(.*)\n*", mk_paragraph)
    if list_elements:
        new_html_list = ['<ul>']
        for element in list_elements:
            new_html_list.append(f'<li>{element}</li>')
        new_html_list.append('</ul>')
        mk_paragraph = ''.join(new_html_list)
    
    return mk_paragraph

