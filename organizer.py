import re
import os

# CSSファイルの読み込み
def read_css(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# セレクタがどのカテゴリに属するかを判定
def categorize_selector(selector):
    if selector.startswith('.'):
        return 'components'  # クラス名
    elif selector.startswith('#'):
        return 'layout'  # ID名
    elif re.match(r'[a-zA-Z]+', selector):
        return 'base'  # タグ名（要素セレクタ）

# セレクタごとに分類してファイルに書き込む
def categorize_css(css_content, output_directory):
    # 各カテゴリごとのCSSファイルの準備
    categorized_css = {
        'base.css': [],
        'layout.css': [],
        'components.css': [],
    }

    # @media や @page を分けるための準備
    media_rules = []
    page_rules = []

    # 正規表現で @media と @page を正しくキャッチ
    media_regex = r'(@media[^{]*\{[^}]*\})'  # @media とその内容
    page_regex = r'(@page[^{]*\{[^}]*\})'    # @page とその内容

    # @media と @page を抽出
    media_rules = re.findall(media_regex, css_content)
    page_rules = re.findall(page_regex, css_content)

    # @media と @page を除いたCSSの通常部分をパース
    css_content = re.sub(media_regex, '', css_content)
    css_content = re.sub(page_regex, '', css_content)

    # 通常のCSSのルールをパースして分類
    rules = re.findall(r'([^{]+)\s*\{([^}]+)\}', css_content)  # セレクタとそのスタイルを抽出
    for selector, style in rules:
        selectors = selector.split(',')  # セレクタをカンマで分ける
        for selector in selectors:
            selector = selector.strip()
            category = categorize_selector(selector)
            rule = f'{selector} {{{style.strip()}}}'
            if category == 'components':
                categorized_css['components.css'].append(rule)
            elif category == 'layout':
                categorized_css['layout.css'].append(rule)
            elif category == 'base':
                categorized_css['base.css'].append(rule)


    # 出力ファイルに書き込む
    for file_name, rules in categorized_css.items():
        output_path = os.path.join(output_directory, file_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(rules))

    return categorized_css, media_rules, page_rules



# 使用例
css_file_path = r'D:\01_program\01_prog. lang\05_Python\css-organizer\static\css\common.css' # スラッシュを使用した例
output_directory = r'D:\01_program\01_prog. lang\05_Python\css-organizer\static\css'  # 出力先ディレクトリ

# CSS内容を読み込んで処理
css_content = read_css(css_file_path)
categorized_css, media_rules, page_rules = categorize_css(css_content, output_directory)


print("CSSファイルが自動的に分類され保存されました。")
