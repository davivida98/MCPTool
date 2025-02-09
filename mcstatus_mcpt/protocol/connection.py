    __slots__ = ()


class BaseAsyncConnection(BaseConnection, BaseReadAsync, BaseWriteAsync):
    """Base asynchronous read and write class"""

    __slots__ = ()


class Connection(BaseSyncConnection):
    """Base connection class."""

    __slots__ = ("sent", "received")

    def __init__(self) -> None:
        self.sent = bytearray()
        self.received = bytearray()

    def read(self, length: int) -> bytearray:
        """Return :attr:`.received` up to length bytes, then cut received up to that point."""
        if len(self.received) < length:
            raise IOError(f"Not enough data to read! {len(self.received)} < {length}")

        result = self.received[:length]
        self.received = self.received[length:]
        return result

    def write(self, data: Connection | str | bytearray | bytes) -> None:
        """Extend :attr:`.sent` from ``data``."""
        if isinstance(data, Connection):
            data = data.flush()
        if isinstance(data, str):
            data = bytearray(data, "utf-8")
        self.sent.extend(data)

    def receive(self, data: BytesConvertable | bytearray) -> None:
        """Extend :attr:`.received` with ``data``."""
        if not isinstance(data, bytearray):
            data = bytearray(data)
        self.received.extend(data)

    def remaining(self) -> int:
        """Return length of :attr:`.received`."""
        return len(self.received)

    def flush(self) -> bytearray:
        """Return :attr:`.sent`, also clears :attr:`.sent`."""
        result, self.sent = self.sent, bytearray()
        return result

    def copy(self) -> "Connection":
        """Return a copy of ``self``"""
        new = self.__class__()
        new.receive(self.received)
        new.write(self.sent)
        return new


class SocketConnection(BaseSyncConnection):
    """Socket connection."""

    __slots__ = ("socket",)

    def __init__(self) -> None:
        # These will only be None until connect is called, ignore the None type assignment
        self.socket: socket.socket = None  # type: ignore[assignment]

    def close(self) -> None:
        """Close :attr:`.socket`."""
        if self.socket is not None:  # If initialized
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError as exception:  # Socket wasn't connected (nothing to shut down)
                if exception.errno != errno.ENOTCONN:
                    raise

            self.socket.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        self.close()


class TCPSocketConnection(SocketConnection):
    """TCP Connection to address. Timeout defaults to 3 seconds."""

    __slots__ = ()

    def __init__(self, addr: tuple[str | None, int], timeout: float = 3):
        super().__init__()
        self.socket = socket.create_connection(addr, timeout=timeout)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def read(self, length: int) -> bytearray:
        """Return length bytes read from :attr:`.socket`. Raises :exc:`IOError` when server doesn't respond."""
        result = bytearray()
        while len(result) < length:
            new = self.socket.recv(length - len(result))
            if len(new) == 0:
