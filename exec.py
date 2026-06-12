import threading
import gc

class AsyncExec(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self.result = "timeout"

    def run(self):
        # Sobrescrevemos o método run para capturar o retorno
        if self._target:
            self.result = self._target(*self._args)

def exec(f, args, timeout):
    stop = threading.Event()
    args.append(stop)
    e = AsyncExec(f, args)
    e.start()
    e.join(timeout=timeout)
    r = e.result
    stop.set()
    if r is None:
        r = "timeout"
    f = None
    gc.collect()
    return r

