def simple_list_md_load(p):
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        result = []
        for line in lines:
            item = line.strip('\n')
            result.append(item)
        return result


def simple_list_md_dump(p, lines):
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def emit_head(md):
    title = '{在此填写标题}'
    contents = ['{在此填写题目描述}']

    md.append(f'# {title}')
    md.append('')
    for content in contents:
        md.append(content)
    md.append('')


def emit_answer(md, language):
    md.append(f'## 答案')
    md.append('')
    if language:
        md.append(f'```{language}')
        md.append('')
        md.append('```')
    else:
        md.append('{在此填写答案}')
    md.append('')


def emit_options(md, language):
    md.append(f'## 选项')
    md.append('')

    for tag in ['A', 'B', 'C']:
        md.append(f'### {tag}')
        md.append('')
        if language:
            md.append(f'```{language}')
            md.append('')
            md.append('```')
        else:
            md.append('{在此填写选项'+f'{tag}'+'}')
        md.append('')
