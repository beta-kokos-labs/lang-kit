'''import pypistats
from pprint import pprint

# Call the API
print(pypistats.recent("peerjs"))'''

import asyncio
from peerjs_py import Peer, PeerOptions

async def handle_message(data):
    print(f"Received: {data}")

async def main():
    peer_id = input("Enter your peer ID: ")
    
    peer = Peer(id=peer_id)

    def on_open(id):
        print(f"Connected with peer ID: {id}")
    
    peer.on('open', on_open)
    
    # Handle incoming connections
    @peer.on('connection')
    async def on_connection(conn):
        print(f"Incoming connection from {conn.peer}")
        conn.on('data', handle_message)
        await conn.send("Hello from Python!")

    # Connect to another peer
    target_id = input("Enter target peer ID (or press Enter to wait for connections): ")
    if target_id:
        conn = await peer.connect(target_id)
        print(f"Connected to {target_id}")
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            await conn.send(message)
    
    # Keep the connection alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        peer.destroy()

if __name__ == "__main__":
    asyncio.run(main())