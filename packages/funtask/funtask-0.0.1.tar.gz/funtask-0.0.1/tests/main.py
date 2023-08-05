import asyncio

from funtask import LocalFunTaskManager, StdLogger


def ff1(x, y: StdLogger):
    ffff()
    x.append("success")
    y.log("2333333333")
    return x


if __name__ == '__main__':
    lft = LocalFunTaskManager(StdLogger())
    workers = lft.increase_workers((lambda x: [123], "tests.test"), 10)
    task1 = workers[0].dispatch_fun_task(ff1)
    workers[0].regenerate_scope(lambda origin: origin + ["again"])
    task = workers[0].dispatch_fun_task(lambda x, y, a: print(3123, a, x), 45555)
    print(asyncio.run(task.get_result()))
    print(asyncio.run(task1.get_result()))
    print(task1.status)
