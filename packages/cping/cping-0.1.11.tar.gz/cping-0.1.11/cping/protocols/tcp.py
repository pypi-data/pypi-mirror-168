'''TCP ping.'''
import socket
import time

import cping.protocols


class Ping(cping.protocols.Ping):
    '''TCP ping. The possible results:
        * latency=x, error=False: successful TCP handshake
        * latency=x, error=True: connection failure, like TCP-RST
        * latency=-1, error=False: timeout
    '''

    def __init__(self, port, *args, **kwargs):
        '''Constructor.

        Args:
            port (int): TCP port to ping.
            *args (...): Arguments passed to `cping.protocols.Ping`.
            **kwargs (x=y): Keyword arguments passed to `cping.protocols.Ping`.

        Raises:
            TypeError: If `port` is not a integer.
            ValueError: If `port` is not between 1 and 65535.
        '''
        self.port = port
        super().__init__(*args, **kwargs)

    @property
    def port(self):
        '''TCP port to ping.'''
        return self._port

    @port.setter
    def port(self, value):
        if not isinstance(value, int):
            raise TypeError('port must be an integer')

        if not 0 < value < 65536:
            raise ValueError('port outside of range 1-65535')

        self._port = value

    def ping_loop(self, host):
        addrinfo = self.resolve(host)

        while not host.stop_signal.is_set():
            # Update the port in the addrinfo in case it was changed
            location = addrinfo[4][:1] + (self.port, ) + addrinfo[4][2:]
            latency = None
            error = False

            with socket.socket(addrinfo[0], socket.SOCK_STREAM) as test_socket:
                checkpoint = time.perf_counter()

                try:
                    test_socket.settimeout(self.interval)
                    test_socket.connect(location)
                except ConnectionError:
                    # Got a response but it was an error (e.g. TCP-RST)
                    error = True
                except OSError as exception:
                    if exception.errno in cping.protocols.IGNORED_OS_ERRORS:
                        time.sleep(self.interval)
                    elif not isinstance(exception, socket.timeout):
                        raise

                    latency = -1

                if latency is None:
                    latency = time.perf_counter() - checkpoint

            host.add_result(latency, error)

            # Block until signaled to continue
            host.wait(latency)
