import os
from flask import Flask, render_template, request, redirect, url_for
import markdown
import json

app = Flask(__name__)

# Configure the path to the book's root directory (one level up from webapp)
BOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@app.route('/')
def index():
    chapters = []
    for dir_name in sorted(os.listdir(BOOK_DIR)):
        if os.path.isdir(os.path.join(BOOK_DIR, dir_name)) and not dir_name.startswith('.') and dir_name not in ['webapp', 'jules-scratch']:
            chapters.append(dir_name)
    return render_template('index.html', chapters=chapters)

@app.route('/chapter/<chapter_name>')
def chapter_view(chapter_name):
    # Construct the path to the markdown file
    # Note: The actual markdown file might have a different name.
    # Assuming the markdown file is named like the directory but lowercase and with .md
    md_filename = f"{chapter_name.lower()}.md"
    # A better approach would be to find the first .md file in the directory
    md_files = [f for f in os.listdir(os.path.join(BOOK_DIR, chapter_name)) if f.endswith('.md')]

    if not md_files:
        return "Markdown file not found for this chapter.", 404

    md_filename = md_files[0]
    filepath = os.path.join(BOOK_DIR, chapter_name, md_filename)

    if not os.path.exists(filepath):
        return "Chapter file not found.", 404

    with open(filepath, 'r', encoding='utf-8') as f:
        content_md = f.read()

    content_html = markdown.markdown(content_md)

    return render_template('chapter.html', chapter_name=chapter_name, content=content_html)

@app.route('/edit/<chapter_name>', methods=['GET', 'POST'])
def edit_chapter(chapter_name):
    md_files = [f for f in os.listdir(os.path.join(BOOK_DIR, chapter_name)) if f.endswith('.md')]
    if not md_files:
        return "Markdown file not found for this chapter.", 404

    md_filename = md_files[0]
    filepath = os.path.join(BOOK_DIR, chapter_name, md_filename)

    if request.method == 'POST':
        content = request.form['content']
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('chapter_view', chapter_name=chapter_name))

    with open(filepath, 'r', encoding='utf-8') as f:
        content_md = f.read()

    # Templates with real newlines for proper formatting
    templates = {
        "Nota do Narrador": "> **Nota do Narrador:** ",
        "Caixa de Texto": "\n---\n**Título da Caixa**\n\n*Conteúdo da caixa...*\n\n---\n",
        "Desafio": "### Desafio: \n**Descrição:** \n**Dificuldade:** "
    }

    return render_template('edit_chapter.html', chapter_name=chapter_name, content=content_md, templates=templates)

@app.route('/print')
def print_book():
    all_content_md = ""
    chapter_dirs = sorted([d for d in os.listdir(BOOK_DIR) if os.path.isdir(os.path.join(BOOK_DIR, d)) and not d.startswith('.') and d not in ['webapp', 'jules-scratch']])

    for chapter_dir in chapter_dirs:
        md_files = [f for f in os.listdir(os.path.join(BOOK_DIR, chapter_dir)) if f.endswith('.md')]
        if md_files:
            filepath = os.path.join(BOOK_DIR, chapter_dir, md_files[0])
            with open(filepath, 'r', encoding='utf-8') as f:
                all_content_md += f.read() + "\n\n<div class='page-break'></div>\n\n"

    all_content_html = markdown.markdown(all_content_md, extensions=['extra'])

    return render_template('print.html', content=all_content_html)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
