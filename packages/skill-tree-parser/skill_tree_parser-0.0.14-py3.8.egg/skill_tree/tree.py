import json
import logging
import os
import subprocess
import sys
import uuid
import re

from parsec import BasicState, ParsecError

from .exercises.markdown import parse
from .exercises.init_exercises import emit_head, emit_answer, emit_options, simple_list_md_dump

id_set = set()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def search_author(author_dict, username):
    for key in author_dict:
        names = author_dict[key]
        if username in names:
            return key
    return username


def user_name(md_file, author_dict):
    ret = subprocess.Popen([
        "git", "log", md_file
    ], stdout=subprocess.PIPE)
    lines = list(map(lambda l: l.decode(), ret.stdout.readlines()))
    author_lines = []
    for line in lines:
        if line.startswith('Author'):
            author_lines.append(line.split(' ')[1])
    if len(author_lines) == 0:
        return None
    author_nick_name = author_lines[-1]
    return search_author(author_dict, author_nick_name)


def load_json(p):
    with open(p, 'r', encoding="utf-8") as f:
        try:
            return json.loads(f.read())
        except UnicodeDecodeError:
            logger.info(
                "json 文件 [{p}] 编码错误，请确保其内容保存为 utf-8 或 base64 后的 ascii 格式。")


def dump_json(p, j, exist_ok=False, override=False):
    if os.path.exists(p):
        if exist_ok:
            if not override:
                return
        else:
            logger.error(f"{p} already exist")
            sys.exit(0)

    with open(p, 'w+', encoding="utf8") as f:
        f.write(json.dumps(j, indent=2, ensure_ascii=False))


def ensure_config(path):
    config_path = os.path.join(path, "config.json")
    if not os.path.exists(config_path):
        node = {"keywords": [],
                "keywords_must": [],
                "keywords_forbid": [],
                "group": 0,
                "subtree": ""}
        dump_json(config_path, node, exist_ok=True, override=False)
        return node
    else:
        return load_json(config_path)


def parse_no_name(d):
    p = r'(\d+)\.(.*)'
    m = re.search(p, d)

    try:
        no = int(m.group(1))
        dir_name = m.group(2)
    except:
        sys.exit(0)

    return no, dir_name


def check_export(base, cfg):
    flag = False
    exports = []
    for export in cfg.get('export', []):
        ecfg_path = os.path.join(base, export)
        if os.path.exists(ecfg_path):
            exports.append(export)
        else:
            flag = True
    if flag:
        cfg["export"] = exports
    return flag


class TreeWalker:
    def __init__(
            self, root,
            tree_name,
            title=None,
            log=None,
            authors=None,
            enable_notebook=None,
            ignore_keywords=False
    ):
        self.ignore_keywords = ignore_keywords
        self.authors = authors if authors else {}
        self.enable_notebook = enable_notebook
        self.name = tree_name
        self.root = root
        self.title = tree_name if title is None else title
        self.tree = {}
        self.logger = logger if log is None else log

    def walk(self):
        root = self.load_root()
        root_node = {
            "node_id": root["node_id"],
            "keywords": root.get("keywords", []),
            "children": [],
            "keywords_must": root.get("keywords_must", []),
            "keywords_forbid": root.get("keywords_forbid", []),
            "group": root.get("group", 0),
            "subtree": root.get("subtree", "")
        }
        self.tree[root["tree_name"]] = root_node
        self.load_levels(root_node)
        self.load_chapters(self.root, root_node)
        for index, level in enumerate(root_node["children"]):
            level_title = list(level.keys())[0]
            level_node = list(level.values())[0]
            level_path = os.path.join(self.root, f"{index + 1}.{level_title}")
            self.load_chapters(level_path, level_node)
            for index, chapter in enumerate(level_node["children"]):
                chapter_title = list(chapter.keys())[0]
                chapter_node = list(chapter.values())[0]
                chapter_path = os.path.join(
                    level_path, f"{index + 1}.{chapter_title}")
                self.load_sections(chapter_path, chapter_node)
                for index, section_node in enumerate(chapter_node["children"]):
                    section_title = list(section_node.keys())[0]
                    full_path = os.path.join(
                        chapter_path, f"{index + 1}.{section_title}")
                    if os.path.isdir(full_path):
                        self.check_section_keywords(full_path)
                        self.ensure_exercises(full_path)

        tree_path = os.path.join(self.root, "tree.json")
        dump_json(tree_path, self.tree, exist_ok=True, override=True)
        return self.tree

    def auto(self):
        if os.path.exists(self.root) and os.listdir(self.root):
            self.walk()
        else:
            self.init()

    def sort_dir_list(self, dirs):
        result = [self.extract_node_env(dir) for dir in dirs]
        result.sort(key=lambda item: item[0])
        return result

    def load_levels(self, root_node):
        levels = []
        for level in os.listdir(self.root):
            if not os.path.isdir(level):
                continue
            level_path = os.path.join(self.root, level)
            num, config = self.load_level_node(level_path)
            levels.append((num, config))

        levels = self.resort_children(self.root, levels)
        root_node["children"] = [item[1] for item in levels]
        return root_node

    def load_level_node(self, level_path):
        config = self.ensure_level_config(level_path)
        num, name = self.extract_node_env(level_path)

        result = {
            name: {
                "node_id": config["node_id"],
                "keywords": config["keywords"],
                "children": [],
                "keywords_must": config.get("keywords_must", []),
                "keywords_forbid": config.get("keywords_forbid", []),
                "group": config.get("group", 0),
                "subtree": config.get("subtree", "")
            }
        }

        return num, result

    def load_chapters(self, base, level_node):
        chapters = []
        for name in os.listdir(base):
            full_name = os.path.join(base, name)
            if os.path.isdir(full_name):
                num, chapter = self.load_chapter_node(full_name)
                chapters.append((num, chapter))

        chapters = self.resort_children(base, chapters)
        level_node["children"] = [item[1] for item in chapters]
        return level_node

    def load_sections(self, base, chapter_node):
        sections = []
        for name in os.listdir(base):
            full_name = os.path.join(base, name)
            if os.path.isdir(full_name):
                num, section = self.load_section_node(full_name)
                sections.append((num, section))

        sections = self.resort_children(base, sections)
        chapter_node["children"] = [item[1] for item in sections]
        return chapter_node

    def resort_children(self, base, children):
        children.sort(key=lambda item: item[0])
        for index, [number, element] in enumerate(children):
            title = list(element.keys())[0]
            origin = os.path.join(base, f"{number}.{title}")
            posted = os.path.join(base, f"{index + 1}.{title}")
            if origin != posted:
                self.logger.info(f"rename [{origin}] to [{posted}]")
            os.rename(origin, posted)
        return children

    def ensure_chapters(self):
        for subdir in os.listdir(self.root):
            self.ensure_level_config(subdir)

    def load_root(self):
        config_path = os.path.join(self.root, "config.json")
        if not os.path.exists(config_path):
            config = {
                "tree_name": self.name,
                "keywords": [],
                "node_id": self.gen_node_id(),
                "keywords_must": [],
                "keywords_forbid": [],
                "group": 0,
                "subtree": ""
            }
            dump_json(config_path, config, exist_ok=True, override=True)
        else:
            config = load_json(config_path)
            flag, result = self.ensure_node_id(config)
            if flag:
                dump_json(config_path, result, exist_ok=True, override=True)

        return config

    def ensure_level_config(self, path):
        config_path = os.path.join(path, "config.json")
        if not os.path.exists(config_path):
            config = {
                "node_id": self.gen_node_id()
            }
            dump_json(config_path, config, exist_ok=True, override=True)
        else:
            config = load_json(config_path)
            flag, result = self.ensure_node_id(config)
            if flag:
                dump_json(config_path, config, exist_ok=True, override=True)
        return config

    def ensure_chapter_config(self, path):
        config_path = os.path.join(path, "config.json")
        if not os.path.exists(config_path):
            config = {
                "node_id": self.gen_node_id(),
                "keywords": [],
                "keywords_must": [],
                "keywords_forbid": [],
                "group": 0,
                "subtree": ""
            }
            dump_json(config_path, config, exist_ok=True, override=True)
        else:
            config = load_json(config_path)
            flag, result = self.ensure_node_id(config)
            if flag:
                dump_json(config_path, config, exist_ok=True, override=True)
        return config

    def ensure_section_config(self, path):
        config_path = os.path.join(path, "config.json")
        if not os.path.exists(config_path):
            config = {
                "node_id": self.gen_node_id(),
                "keywords": [],
                "children": [],
                "export": [],
                "keywords_must": [],
                "keywords_forbid": [],
                "group": 0,
                "subtree": ""
            }
            dump_json(config_path, config, exist_ok=True, override=True)
        else:
            config = load_json(config_path)
            flag, result = self.ensure_node_id(config)
            if flag:
                dump_json(config_path, result, exist_ok=True, override=True)
        return config

    def ensure_node_id(self, config):
        flag = False
        if "node_id" not in config or \
                not config["node_id"].startswith(f"{self.name}-") or \
                config["node_id"] in id_set:
            new_id = self.gen_node_id()
            id_set.add(new_id)
            config["node_id"] = new_id
            flag = True

        for child in config.get("children", []):
            child_node = list(child.values())[0]
            f, _ = self.ensure_node_id(child_node)
            flag = flag or f

        return flag, config

    def gen_node_id(self):
        return f"{self.name}-{uuid.uuid4().hex}"

    def extract_node_env(self, path):
        try:
            _, dir = os.path.split(path)
            self.logger.info(path)
            number, title = dir.split(".", 1)
            return int(number), title
        except Exception as error:
            self.logger.error(f"目录 [{path}] 解析失败，结构不合法，可能是缺少序号")
            # sys.exit(1)
            raise error

    def load_chapter_node(self, full_name):
        config = self.ensure_chapter_config(full_name)
        num, name = self.extract_node_env(full_name)
        result = {
            name: {
                "node_id": config["node_id"],
                "keywords": config["keywords"],
                "children": [],
                "keywords_must": config.get("keywords_must", []),
                "keywords_forbid": config.get("keywords_forbid", []),
                "group": config.get("group", 0),
                "subtree": config.get("subtree", "")
            }
        }
        return num, result

    def load_section_node(self, full_name):
        config = self.ensure_section_config(full_name)
        num, name = self.extract_node_env(full_name)
        result = {
            name: {
                "node_id": config["node_id"],
                "keywords": config.get("keywords", []),
                "children": config.get("children", []),
                "keywords_must": config.get("keywords_must", []),
                "keywords_forbid": config.get("keywords_forbid", []),
                "group": config.get("group", 0),
                "subtree": config.get("subtree", "")
            }
        }
        # if "children" in config:
        #     result["children"] = config["children"]
        return num, result

    def ensure_exercises(self, section_path):
        config = self.ensure_section_config(section_path)
        flag = False
        for e in os.listdir(section_path):
            base, ext = os.path.splitext(e)
            _, source = os.path.split(e)
            if ext != ".md":
                continue
            mfile = base + ".json"
            meta_path = os.path.join(section_path, mfile)
            md_file = os.path.join(section_path, e)
            self.ensure_exercises_meta(meta_path, source, md_file)
            export = config.get("export", [])
            if mfile not in export and self.name != "algorithm":
                export.append(mfile)
                flag = True
                config["export"] = export

            data = None
            with open(md_file, "r", encoding="utf-8") as efile:
                try:
                    data = efile.read()
                except UnicodeDecodeError:
                    logger.error(f"习题 [{md_file}] 编码错误，请确保其保存为 utf-8 编码")
                    sys.exit(1)

            if data.strip() == '':
                md = []
                emit_head(md)
                emit_answer(md, None)
                emit_options(md, None)
                simple_list_md_dump(md_file, md)

            data = None
            with open(md_file, "r", encoding="utf-8") as efile:
                try:
                    data = efile.read()
                except UnicodeDecodeError:
                    logger.error(f"习题 [{md_file}] 编码错误，请确保其保存为 utf-8 编码")
                    sys.exit(1)

            state = BasicState(data)
            try:
                doc = parse(state)
            except ParsecError as err:
                index = state.index
                context = state.data[index - 15:index + 15]
                logger.error(
                    f"习题 [{md_file}] 解析失败，在位置 {index} [{context}] 附近有格式: [{err}]")

        if flag:
            dump_json(os.path.join(section_path, "config.json"),
                      config, True, True)

        for e in config.get("export", []):
            full_name = os.path.join(section_path, e)
            exercise = load_json(full_name)
            if "exercise_id" not in exercise or exercise.get("exercise_id") in id_set:
                eid = uuid.uuid4().hex
                exercise["exercise_id"] = eid
                dump_json(full_name, exercise, True, True)
            else:
                id_set.add(exercise["exercise_id"])

    def ensure_exercises_meta(self, meta_path, source, md_file):
        _, mfile = os.path.split(meta_path)
        meta = None
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                content = f.read()
            if content:
                meta = json.loads(content)
                if "exercise_id" not in meta:
                    meta["exercise_id"] = uuid.uuid4().hex
                if "notebook_enable" not in meta:
                    meta["notebook_enable"] = self.default_notebook()
                if "source" not in meta:
                    meta["source"] = source
                if "author" not in meta:
                    meta["author"] = user_name(md_file, self.authors)
                elif meta['author'] is None:
                    meta["author"] = user_name(md_file, self.authors)
                if "type" not in meta:
                    meta["type"] = "code_options"

        if meta is None:
            meta = {
                "type": "code_options",
                "author": user_name(md_file, self.authors),
                "source": source,
                "notebook_enable": self.default_notebook(),
                "exercise_id": uuid.uuid4().hex
            }
        dump_json(meta_path, meta, True, True)

    def default_notebook(self):
        if self.enable_notebook is not None:
            return self.enable_notebook
        if self.name in ["python", "java", "c"]:
            return True
        else:
            return False

    def check_section_keywords(self, full_path):
        if self.ignore_keywords:
            return
        config = self.ensure_section_config(full_path)
        if not config.get("keywords", []):
            self.logger.error(f"节点 [{full_path}] 的关键字为空，请修改配置文件写入关键字")
            sys.exit(1)

    def init(self):
        data_root = self.root
        os.makedirs(data_root, exist_ok=True)

        node_dirs = [
            os.path.join(data_root, f'1.{self.title}初阶'),
            os.path.join(data_root, f'2.{self.title}中阶'),
            os.path.join(data_root, f'3.{self.title}高阶'),
            os.path.join(data_root, f'1.{self.title}初阶',
                         f"1.{self.title}入门", f"1.HelloWorld"),
        ]

        for node_dir in node_dirs:
            os.makedirs(node_dir, exist_ok=True)

        md = []
        emit_head(md)
        emit_answer(md, None)
        emit_options(md, None)
        simple_list_md_dump(os.path.join(
            node_dirs[len(node_dirs) - 1], 'helloworld.md'), md)

        self.walk()
        self.init_readme()

        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write('\n'.join([
                ".vscode",
                ".idea",
                ".DS_Store",
                "__pycache__",
                "*.pyc",
                "*.zip",
                "*.out",
                "bin/",
                "debug/",
                "release/",
            ]))

        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join([
                "pre_commit",
                "skill-tree-parser",
            ]))

    def init_readme(self):

        md = [
            f'# skill_tree_{self.name}',
            f'',
            f'`{self.title}技能树`是[技能森林](https://gitcode.net/csdn/skill_tree)的一部分。',
            f'',
            f'## 编辑环境初始化',
            f'',
            f'```',
            f'pip install -r requirements.txt',
            f'```',
            f'',
            f'## 目录结构说明',
            f'技能树编辑仓库的 data 目录是主要的编辑目录，目录的结构是固定的',
            f'',
            f'* 技能树`骨架文件`：',
            f'    * 位置：`data/tree.json`',
            f'    * 说明：该文件是执行 `python main.py` 生成的，请勿人工编辑',
            f'* 技能树`根节点`配置文件：',
            f'    * 位置：`data/config.json`',
            f'    * 说明：可编辑配置关键词等字段，其中 `node_id` 字段是生成的，请勿编辑',
            f'* 技能树`难度节点`：',
            f'    * 位置：`data/xxx`，例如: `data/1.{self.title}初阶`',
            f'    * 说明：',
            f'        * 每个技能树有 3 个等级，目录前的序号是必要的，用来保持文件夹目录的顺序',
            f'        * 每个目录下有一个 `config.json` 可配置关键词信息，其中 `node_id` 字段是生成的，请勿编辑',
            f'* 技能树`章节点`：',
            f'    * 位置：`data/xxx/xxx`，例如：`data/1.{self.title}初阶/1.{self.title}简介`',
            f'    * 说明：',
            f'        * 每个技能树的每个难度等级有 n 个章节，目录前的序号是必要的，用来保持文件夹目录的顺序',
            f'        * 每个目录下有一个 `config.json` 可配置关键词信息，其中 `node_id` 字段是生成的，请勿编辑',
            f'* 技能树`知识节点`：',
            f'    * 位置：`data/xxx/xxx`，例如：`data/1.{self.title}初阶/1.{self.title}简介`',
            f'    * 说明：',
            f'        * 每个技能树的每章有 n 个知识节点，目录前的序号是必要的，用来保持文件夹目录的顺序',
            f'        * 每个目录下有一个 `config.json`',
            f'            * 其中 `node_id` 字段是生成的，请勿编辑',
            f'            * 其中 `keywords` 可配置关键字字段',
            f'            * 其中 `children` 可配置该`知识节点`下的子树结构信息，参考后面描述',
            f'            * 其中 `export` 可配置该`知识节点`下的导出习题信息，参考后面描述',
            f'',
            f'## `知识节点` 子树信息结构',
            f'',
            f'例如 `data/1.{self.title}初阶/1.{self.title}简介/1.HelloWorld/config.json` 里配置对该知识节点子树信息结构，这个配置是可选的：',
            f'```json',
            f'{{',
            f'    // ...',
            f'',
            f'    "children": [',
            f'    {{',
            f'        "XX开发入门": {{',
            f'          "keywords": [',
            f'            "XX开发",',
            f'          ],',
            f'          "children": [],',
            f'          "keywords_must": [',
            f'            "XX"',
            f'          ],',
            f'          "keywords_forbid": []',
            f'        }}',
            f'    }}',
            f'  ],',
            f'}}',
            f'```',
            f'',
            f'## `知识节点` 的导出习题编辑',
            f'',
            f'例如 `data/1.{self.title}初阶/1.{self.title}简介/1.HelloWorld/config.json` 里配置对该知识节点导出的习题',
            f'',
            f'```json',
            f'{{',
            f'    // ...',
            f'    "export": [',
            f'        "helloworld.json"',
            f'    ]',
            f'}}',
            f'```',
            f'',
            f'helloworld.json 的格式如下：',
            f'```bash',
            f'{{',
            f'  "type": "code_options",',
            f'  "author": "xxx",',
            f'  "source": "helloworld.md",',
            f'  "notebook_enable": false,',
            f'  "exercise_id": "xxx"',
            f'}}',
            f'```',
            f'',
            f'其中 ',
            f'* "type": "code_options" 表示是一个选择题',
            f'* "author" 可以放作者的 CSDN id，',
            f'* "source" 指向了习题 MarkDown文件',
            f'* "notebook_enable" 目前都是false',
            f'* "exercise_id" 是工具生成的，不填',
            f'',
            f'',
            f'习题格式模版如下：',
            f'',
            f'````mardown',
            f'# {{标题}}',
            f'',
            f'{{习题描述}}',
            f'',
            f'以下关于上述游戏代码说法[正确/错误]的是？',
            f'',
            f'## 答案',
            f'',
            f'{{目标选项}}',
            f'',
            f'## 选项',
            f'',
            f'### A',
            f'',
            f'{{混淆选项1}}',
            f'',
            f'### B',
            f'',
            f'{{混淆选项2}}',
            f'',
            f'### C',
            f'',
            f'{{混淆选项3}}',
            f'',
            f'````',
            f'',
            f'## 技能树合成',
            f'',
            f'在根目录下执行 `python main.py` 会合成技能树文件，合成的技能树文件: `data/tree.json`',
            f'* 合成过程中，会自动检查每个目录下 `config.json` 里的 `node_id` 是否存在，不存在则生成',
            f'* 合成过程中，会自动检查每个知识点目录下 `config.json` 里的 `export` 里导出的习题配置，检查是否存在`exercise_id` 字段，如果不存在则生成',
            f'* 在 节 目录下根据需要，可以添加一些子目录用来测试代码。',
            f'* 开始游戏入门技能树构建之旅，GoodLuck! ',
            f'',
            f'## FAQ',
            f'',
            f'**难度目录是固定的么？**',
            f'',
            f'1. data/xxx 目录下的子目录是固定的初/中/高三个难度等级目录',
            f'',
            f'**如何增加章目录？**',
            f'',
            f'1. 在VSCode里打开项目仓库',
            f'2. 在对应的难度等级目录新建章目录，例如在 data/1.xxx初阶/ 下新建章文件夹，data/1.xxx初阶/1.yyy',
            f'3. 在项目根目录下执行 python main.py 脚本，会自动生成章的配置文件 data/1.xxx初阶/1.yyy/config.json',
            f'',
            f'**如何增加节目录?**:',
            f'1. 直接在VSCode里创建文件夹，例如 "data/1.xxx初阶/1.yyy/2.zzz"',
            f'2. 项目根目录下执行 python main.py 会自动为新增节创建配置文件 data/1.xxx初阶/1.yyy/2.zzz/config.json',
            f'',
            f'**如何在节下新增一个习题**:',
            f'3. 在"data/1.xxx初阶/1.yyy/2.zzz" 目录下添加一个 markdown 文件编辑，例如 yyy.md，按照习题markdown格式编辑习题。',
            f'4. md编辑完后，可以再次执行  python main.py 会自动生成同名的 yyy.json，并将 yyy.json 添加到config.json 的export数组里。',
            f'5. yyy.json里的author信息放作者 CSDN ID。',
        ]

        simple_list_md_dump('README.md', md)
