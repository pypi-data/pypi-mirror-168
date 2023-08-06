import subprocess
from loguru import logger
"""
    desc: 命令执行相关sdk
    version: v0.1
"""



class CommandExecute:

    def __init__(self):
        pass

    def run_cmd(self, cmd):
        ex = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pipe, err = ex.communicate()
        status = ex.wait()
        logger.debug(f"status: {status}")
        output = pipe.decode('gbk')
        error = err.decode('gbk')
        if error or status != 0:
            logger.error(error)
            return False
        logger.debug(output)
        return output


command_execute = CommandExecute()

if __name__ == '__main__':
    command_execute.run_cmd("whoami")

