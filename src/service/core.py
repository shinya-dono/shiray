import atexit
import logging
import subprocess
import threading


class Core:
    def __init__(self,
                 executable_path: str = "/code/bin/xray",
                 assets_path: str = "/code/bin"):
        self.executable_path = executable_path
        self.assets_path = assets_path
        self.started = False
        self._process = None
        self._on_start_funcs = []
        self._on_stop_funcs = []
        self._env = {
            "XRAY_LOCATION_ASSET": assets_path
        }
        self.logger = logging.getLogger('shinya')
        atexit.register(lambda: self.stop() if self.started else None)

    @property
    def process(self):
        if self._process is None:
            raise ProcessLookupError("Xray has not been started")
        return self._process

    def _read_process_stdout(self):
        def reader():
            while True:
                try:
                    output = self._process.stdout.readline().strip('\n')
                    if output == '' and self._process.poll() is not None:
                        break
                except AttributeError:
                    break

                # if output:
                #     logger.info(output)

        threading.Thread(target=reader).start()

    def start(self):
        if self.started is True:
            raise RuntimeError("Xray is started already")

        cmd = [
            self.executable_path,
            "run",
            '-config',
            'xray.json'
        ]
        self._process = subprocess.Popen(
            cmd,
            env=self._env,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        # Wait for XRay to get started
        log = ''
        while True:
            output = self._process.stdout.readline()
            print(output)
            if output == '' and self._process.poll() is not None:
                break

            if output:
                log = output.strip('\n')
                self.logger.debug(log)

                if log.endswith('xray.json'):
                    self.logger.info(log)
                    self.started = True
                    break

        if not self.started:
            raise RuntimeError("Failed to run XRay", log)

        self._read_process_stdout()

        # execute on start functions
        for func in self._on_start_funcs:
            threading.Thread(target=func).start()

    def stop(self):
        self.process.terminate()
        self.started = False
        self._process = None
        self.logger.info("Xray stopped")

        # execute on stop functions
        for func in self._on_stop_funcs:
            threading.Thread(target=func).start()

    def restart(self):
        self.stop()
        self.start()

    def on_start(self, func: callable):
        self._on_start_funcs.append(func)
        return func

    def on_stop(self, func: callable):
        self._on_stop_funcs.append(func)
        return func
