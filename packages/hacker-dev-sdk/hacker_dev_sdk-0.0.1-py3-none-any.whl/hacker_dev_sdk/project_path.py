"""
处理项目路径
"""
from os.path import abspath, dirname,join
from hashlib import sha256


class ProjectPath:
    def __int__(self):
        pass

    def get_project_abs_path(self):
        """
        获取项目main所在绝对路径
        :return: String 项目绝对路径
        """
        return abspath(dirname(abspath(dirname(__file__))))

    def handle_path(self, str_path):
        """将相对路径处理成绝对路径"""
        return abspath(join(project_path.get_project_abs_path(), str_path))

    def hash_name(self, i_str: str):
        i_str += "CanUGuessMe?"
        return sha256(i_str.encode()).hexdigest()


project_path = ProjectPath()

if __name__ == '__main__':
    print(project_path.hash_name("tttkkk"))
