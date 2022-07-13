import asyncio
import json

ADDRESS = "127.0.0.1"
PORT = 8080

Users = {}


async def handle_client(reader, writer):
    while True:
        data = json.loads((await reader.read(8192)).decode())
        if data["code"] == "nick":
            nickname = data["message"]
            Users[nickname] = [reader, writer]
        if data["code"] == "exit":
            writer.close()
            Users.pop(data["from"])
            break
        if data["code"] == "send":
            dict_send = {"code": "receive",
                         "from": data["from"],
                         "to": data["to"],
                         "message": data["message"]}
            await send(dict_send)
        if data["code"] == "find":
            test = Users.get(data["message"])
            if test is not None:
                dict_send = {"code": "user",
                             "from": "server",
                             "to": data["from"],
                             "message": data["message"]}
            else:
                dict_send = {"code": "error",
                             "from": "server",
                             "to": data["from"],
                             "message": f"No user with name {data['message']}"}
            await send(dict_send)


async def send(data: dict) -> None:
    receiver = Users[data["to"]][1]
    receiver.write(json.dumps(data).encode())
    await receiver.drain()


async def run_server():
    server = await asyncio.start_server(handle_client, ADDRESS, PORT)
    print("Server started")
    async with server:
        await server.serve_forever()
