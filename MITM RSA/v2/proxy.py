
import asyncio


class ProxyDatagramProtocol(asyncio.DatagramProtocol):

    def __init__(self, remote_address):
        self.remote_address = remote_address
        self.remotes = {}
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
            return
        loop = asyncio.get_event_loop()
        self.remotes[addr] = RemoteDatagramProtocol(self, addr, data)
        print("sending from this ip")
        print(addr)
        print("sending data:")
        print(data)
        coro = loop.create_datagram_endpoint(
            lambda: self.remotes[addr], remote_addr=self.remote_address)
        asyncio.ensure_future(coro)


class RemoteDatagramProtocol(asyncio.DatagramProtocol):

    def __init__(self, proxy, addr, data):
        self.proxy = proxy
        self.addr = addr
        self.data = data
        #
        print("sending from client:")
        print(data)
        #
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.data)

    def datagram_received(self, data, _):
        #
        print("sending:")
        print(data)
        #
        self.proxy.transport.sendto(data, self.addr)

    def connection_lost(self, exc):
        self.proxy.remotes.pop(self.attr)


async def start_datagram_proxy(bind, port, remote_host, remote_port):
    loop = asyncio.get_event_loop()
    protocol = ProxyDatagramProtocol((remote_host, remote_port))
    return await loop.create_datagram_endpoint(
        lambda: protocol, local_addr=(bind, port))


def main(bind='0.0.0.0', port=12000,
        remote_host='127.0.0.1', remote_port=10000):
    loop = asyncio.get_event_loop()
    print("PROXY-PROXY-PROXY-PROXY-PROXY-PROXY-PROXY-PROXY-PROXY-PROXY")
    print("Starting datagram proxy...")
    coro = start_datagram_proxy(bind, port, remote_host, remote_port)
    transport, _ = loop.run_until_complete(coro)
    print("Datagram proxy is running...")
    print("*********************************")
    print("data will be sent to the port on:")
    print(remote_port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Closing transport...")
    transport.close()
    loop.close()


if __name__ == '__main__':
    main()
