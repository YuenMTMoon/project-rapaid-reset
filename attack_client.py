import argparse
import asyncio
import time
from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import ResponseReceived, SettingsAcknowledged
from h2.exceptions import ProtocolError
from h2.frame_buffer import FrameBuffer
from h2.errors import ErrorCodes
from hyperframe.frame import SettingsFrame, HeadersFrame, RstStreamFrame
import ssl

num_requests = 5
server_url = ''
wait_time = 0
delay_time = 0
concurrency_limit = 0

sent_headers = 0
sent_rsts = 0
recv_frames = 0
header_start = 0
header_end = 0

async def send_request(connection, stream_id, path, delay):
    global sent_headers, sent_rsts, recv_frames

    # Send headers
    headers = [
        (':method', 'GET'),
        (':path', path),
        (':scheme', 'https'),
        (':authority', server_url.split('://')[1]),
    ]

    connection.send_headers(stream_id, headers, end_stream=True)
    sent_headers += 1
    print(f"[{stream_id}] Sent HEADERS")

    # Sleep for delay time
    await asyncio.sleep(delay / 1000.0)

    # Send RST_STREAM
    connection.reset_stream(stream_id, ErrorCodes.CANCEL)
    sent_rsts += 1
    print(f"[{stream_id}] Sent RST_STREAM")

async def worker(session, path, delay, done_chan):
    try:
        connection = H2Connection(config=H2Configuration(client_side=True))
        connection.initiate_connection()
        await session.sendall(connection.data_to_send())

        stream_id = connection.get_next_available_stream_id()
        await send_request(connection, stream_id, path, delay)

        async for event in session:
            if isinstance(event, ResponseReceived):
                recv_frames += 1
                print(f"Received frame: {event}")

        done_chan.put_nowait(None)
    except ProtocolError as e:
        print(f"Protocol error: {e}")
        done_chan.put_nowait(None)

async def main():
    global header_start, header_end

    parser = argparse.ArgumentParser(description="HTTP/2 client")
    parser.add_argument('--requests', type=int, default=5, help='Number of requests to send')
    parser.add_argument('--url', type=str, default='https://localhost:8000', help='Server URL')
    parser.add_argument('--wait', type=int, default=0, help='Wait time in milliseconds between starting workers')
    parser.add_argument('--delay', type=int, default=0, help='Delay in milliseconds between sending HEADERS and RST_STREAM')
    parser.add_argument('--concurrency', type=int, default=0, help='Maximum number of concurrent worker routines')
    args = parser.parse_args()

    global num_requests, server_url, wait_time, delay_time, concurrency_limit
    num_requests = args.requests
    server_url = args.url
    wait_time = args.wait
    delay_time = args.delay
    concurrency_limit = args.concurrency

    header_start = time.time()

    path = '/'
    if server_url.endswith('/'):
        path = ''

    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    done_chan = asyncio.Queue()
    tasks = []

    for _ in range(num_requests):
        await asyncio.sleep(wait_time / 1000.0)
        connection = asyncio.open_connection(server_url.split('://')[1].split(':')[0], 443, ssl=ssl_context)
        tasks.append(worker(connection, path, delay_time, done_chan))

    await asyncio.gather(*tasks)

    for _ in range(num_requests):
        await done_chan.get()

    header_end = time.time()
    elapsed = header_end - header_start

    print("\n--- Summary ---")
    print(f"Frames sent: HEADERS = {sent_headers}, RST_STREAM = {sent_rsts}")
    print(f"Frames received: {recv_frames}")
    print(f"Total time: {elapsed:.2f} seconds ({int(round(sent_headers / elapsed))} rps)")

if __name__ == "__main__":
    asyncio.run(main())
