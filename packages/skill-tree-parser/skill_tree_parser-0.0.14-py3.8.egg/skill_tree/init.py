import os
from .tree import load_json, dump_json


def init_dir(tree_name):
    tree = load_json('data/tree_simple.json')

    level_0 = tree['level']['level_0']
    level_1 = tree['level']['level_1']
    level_2 = tree['level']['level_2']
    tree = tree['tree']

    init_level(tree, level_0, f'data/1.{tree_name}初阶')
    init_level(tree, level_1, f'data/2.{tree_name}中阶')
    init_level(tree, level_2, f'data/3.{tree_name}高阶')


def init_level(tree, level, root):
    chapter_i = 1
    for chapter in level:
        sections = tree[chapter]

        chapter_dir = os.path.join(root, f'{chapter_i}.{chapter}')
        os.makedirs(chapter_dir, exist_ok=True)

        section_i = 1
        for section in sections:
            section_dir = os.path.join(chapter_dir, f'{section_i}.{section}')
            os.makedirs(section_dir, exist_ok=True)
            section_i += 1

        chapter_i += 1
