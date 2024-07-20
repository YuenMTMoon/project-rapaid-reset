Introduction 
• HTTP/2 is an application layer protocol built upon TCP/IP. 
• Inherits resources from HTTP 1.1, including URLs, ports, etc. 
• Transition requires client-server communication and protocol agreement. 
2. Transition Process 
• Clear text TCP connections: 
• Clients indicate HTTP/2 support with "Upgrade" field ("h2c" value) 
in request. 
• Servers respond with "101 Switching Protocols" if supporting 
HTTP/2. 
• Over TLS: 
• Use of Application Layer Protocol Negotiation (ALPN) extension 
during TLS handshake. 
• Client sends Connection preface and settings frame to confirm 
HTTP/2. 
3. Frame Structure 
• HTTP/2 operates through frames. 
• Each frame has a fixed 9-byte header including length, type, flags, 
reserved bits, and stream ID. 
• Various frame types for different purposes: 
• Data Frame (0x0): Carries data to and from the server. 
• Header Frame (0x1): Transmits HTTP request headers. 
• Priority Frame (0x2): Sets priority for a stream. 
• Reset Frame (0x3): Immediately terminates a frame. 
• Setting Frame (0x4): Transmits connection-level settings. 
• Push Promise Frame (0x5): Used by the server to push resources to 
the client. 
• Ping Frame (0x6): Checks connection activity. 
• Go away Frame (0x7): Closes the connection. 
• Window Update (0x8): Implements flow control. 
• Continuation Frame (0x9): Carries data when payload exceeds 
frame size. 
Stream Communication 
• Communication occurs over streams, defined as a sequence of frames. 
• Each stream corresponds to a single request-response. 
• Frames exchanged between client and server form the basis of 
communication. 
• Client sends HTTP headers in Header frames, server responds with 
headers and content in Data frames. 
Key Features and Optimization in HTTP/2 
1. Multiplexing 
• Allows concurrent access to multiple resources over a single connection. 
• Streams enable asynchronous request-response communication. 
• Facilitates efficient resource retrieval without blocking other streams. 
2. HPACK Header Compression 
• Reduces bandwidth requirements by compressing header fields into 
name-value pairs. 
• Utilizes a mapping table to convert headers, optimizing data transfer 
efficiency. 
3. Features of HTTP/2 
• Multiplexing: Streams enable asynchronous request-response 
communication, facilitating efficient resource retrieval for web pages with 
multiple components. 
• Resource Prioritization: Ensures prompt delivery of critical components 
like HTML, JavaScript, and CSS to enhance page loading speed. 
• Server Push: Allows servers to proactively push required resources to 
clients during idle time, reducing latency and enhancing protocol 
efficiency. 
Introduction to HTTP/2 Rapid Reset Attack: The HTTP/2 Rapid Reset attack 
exploits vulnerabilities within the HTTP/2 protocol to overwhelm target servers. 
By leveraging features like stream multiplexing and certain frame types, attackers 
can flood servers with a barrage of requests, rapidly resetting them and leading 
to denial of service. Below are the key points illustrating how this attack works: 
Key Points: 
1. Stream Multiplexing: 
• HTTP/2 enables the simultaneous transmission of multiple 
streams over a single TCP connection, enhancing efficiency by 
allowing parallel processing of requests and responses. 
2. Concurrency: 
• Unlike HTTP/1.1, HTTP/2 permits clients to initiate multiple 
concurrent streams, improving throughput and reducing latency. 
However, this also makes DDoS attacks more efficient. 
3. RST_STREAM Frame: 
• HTTP/2 includes the RST_STREAM frame, allowing clients to cancel 
requests immediately after initiation. Attackers exploit this feature 
to rapidly reset requests, leading to resource exhaustion on the 
server. 
4. Cost Asymmetry: 
• In HTTP/2, canceling requests primarily burdens the server, as it 
must allocate resources before requests are canceled. This 
asymmetry in cost favors attackers, who can cancel requests with 
minimal effort. 
5. Bandwidth Reduction: 
• Attackers can minimize downlink bandwidth consumption by 
canceling requests before receiving responses, exacerbating the 
impact of the attack on server resources. 
HTTP/2 Rapid Reset Attack demo functionalities: 
1. Command Line Arguments Handling: 
• The program accepts command-line arguments such as the 
number of requests to send, server URL, concurrency limit, wait 
time, and delay time between sending requests. 
2. Sending Requests: 
• The sendRequest function constructs HTTP/2 HEADERS frames 
with encoded headers and sends them to the server. It then sends 
RST_STREAM frames to cancel the requests immediately after 
sending HEADERS frames. 
• Each request is sent in a separate goroutine to achieve concurrent 
execution. 
3. Frame Handling: 
• The code establishes a TLS connection with the server and 
initializes an HTTP/2 framer to handle frame transmission. 
• It reads incoming frames from the server in a separate goroutine 
and counts the number of received frames. 
4. Settings Frame Initialization: 
• The program sends an initial SETTINGS frame to the server to 
negotiate connection parameters. 
5. Concurrency Control: 
• The program utilizes a buffered channel to control the concurrency 
of worker goroutines. Each worker signals its completion by 
sending a value to this channel. 
6. Summary Printing: 
• Upon completion of all requests, the program prints a summary 
that includes the number of sent and received frames, total 
execution time, and requests per second metric.