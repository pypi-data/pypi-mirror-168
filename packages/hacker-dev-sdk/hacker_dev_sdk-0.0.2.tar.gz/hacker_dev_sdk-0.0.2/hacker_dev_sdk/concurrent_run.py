from threading import Thread


class ConCurrent:
    def __init__(self):
        self.t_pool = []

    def run(self, func, args):
        t = Thread(target=func, args=args)
        print(f"线程状态：{t.getName()}-{t.is_alive()}")
        t.start()
        print(f"线程状态：{t.getName()}-{t.is_alive()}")
        self.t_pool.append(t)

    def join_all(self):
        for t in self.t_pool:
            t.join()

    def is_finish_all(self):
        for t in self.t_pool:
            print(f"线程状态：{t.getName()}-{t.is_alive()}")
            if t.is_alive():
                return False
        return True


con_current = ConCurrent()
