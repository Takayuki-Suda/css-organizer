import os
import re

common_css_path = r"D:\01_program\01_prog. lang\05_Python\css-organizer\static\css\common.css"
base_css_path = r"D:\01_program\01_prog. lang\05_Python\css-organizer\static\css\base.css"

# **base.css の内容を取得**
if os.path.exists(base_css_path):
    with open(base_css_path, "r", encoding="utf-8") as f:
        base_css = f.read()
else:
    base_css = ""

# **common.css の内容を取得**
if os.path.exists(common_css_path):
    with open(common_css_path, "r", encoding="utf-8") as f:
        common_css = f.read()
else:
    print("common.css が見つかりません。")
    exit()

# **@media ブロックを一時的に保護**
media_blocks = []
def media_block_replacer(match):
    media_blocks.append(match.group(0))
    return f"__MEDIA_BLOCK_{len(media_blocks)-1}__"

common_css = re.sub(r"@media[^{]+\{(?:[^{}]|\{[^{}]*\})*\}", media_block_replacer, common_css, flags=re.DOTALL)

# **CSS のブロックを取得する正規表現**
css_block_pattern = re.compile(r"([^{]+)\s*\{([^}]*)\}", re.MULTILINE)

# **base.css に含まれるセレクターとその内容をセットに**
base_blocks = set()
for match in css_block_pattern.finditer(base_css):
    selector = match.group(1).strip()
    properties = match.group(2).strip()
    if selector and properties:
        base_blocks.add((selector, properties))

# **common.css から base.css にあるセレクターのブロックを削除**
def remove_exact_css_blocks(css_text, blocks_to_remove):
    new_css_lines = []
    css_lines = css_text.split("\n")
    i = 0

    while i < len(css_lines):
        line = css_lines[i].strip()

        # ブロックの開始（例: "h1 {"）
        if "{" in line:
            selector = line.split("{")[0].strip()
            properties = ""

            # ブロックの中身を取得
            block_lines = []
            while i < len(css_lines) and "}" not in css_lines[i]:
                block_lines.append(css_lines[i].strip())
                i += 1
            
            if i < len(css_lines):  # "}" を含める
                block_lines.append(css_lines[i].strip())

            properties = " ".join(block_lines).replace(selector, "").replace("{", "").replace("}", "").strip()

            # 完全一致するブロックならスキップ（削除）
            if (selector, properties) in blocks_to_remove:
                i += 1  # 次の行へ（ブロック全体を飛ばす）
                continue

            # 削除しない場合はそのまま追加
            new_css_lines.extend(block_lines)
        else:
            new_css_lines.append(css_lines[i])

        i += 1

    return "\n".join(new_css_lines).strip()

# **新しい common.css を作成**
new_common_css = remove_exact_css_blocks(common_css, base_blocks)

# **@media ブロックを元に戻す**
for i, media_block in enumerate(media_blocks):
    new_common_css = new_common_css.replace(f"__MEDIA_BLOCK_{i}__", media_block)

# **更新された common.css を保存**
with open(common_css_path, "w", encoding="utf-8") as f:
    f.write(new_common_css)

print("common.css から base.css の内容を削除しました。（@media の内容は保持）")
