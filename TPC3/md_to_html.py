import re

def md_to_html(text):

    # Headings
    text = re.sub(r'### (.+)', r'<h3>\1</h3>', text)
    text = re.sub(r'## (.+)', r'<h2>\1</h2>', text)
    text = re.sub(r'# (.+)', r'<h1>\1</h1>', text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text) #uso de ? para que não seja greedy

    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

    # listas ordenadas
    lista_itens = re.findall(r'\d+\.\s(.+)', text)
    
    if lista_itens:
        lista_html = ''.join(f"<li>{item}</li>\n" for item in lista_itens)
        text = re.sub(r'(\d+\.\s.+\n?)+', f"<ol>\n{lista_html}</ol>", text)
    
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # Imagens
    text = re.sub(r'!\[(.*?)\]\((.+?)\)', r'<img src="\2" alt="\1"/>', text)

    return text
