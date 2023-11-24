import websockets
import asyncio
import json
import my_llm
import time

ENGINE = "CACHE"

llm = my_llm.get_llm()

async def transmit(websocket, path):

    print("Client Connected !",path,'********************************************************')

    try :
        query = ''
        # query.strip()
        
        while True:
            query = await websocket.recv()
            query = json.loads(query)
            filename = query['filename']

            queryEngine = my_llm.get_query_engine_from_cache(llm, filename) if ENGINE == "CACHE" else my_llm.get_query_engine(llm, filename)
        
            print(query)

            prompt = f"""Answer within context of {query["game"]}.
            Question : {query["question"]}
            Instructions : answer the question STRICTLY in the context of the game. You cannot invent any new information, but are allowed to draw conclusions from the existing knowledge base of {query["game"]}.csv.
            Use \n token to symbolize the number of newlines after each paragraph.
            Use \t token at the start of sentences to symbolize tab space wherever required.
            """

            # query.strip()
            
            # if query == "disconnect_server":
            #     await websocket.send("Bye !")
            #     break

            # -----------------------------------------------------------------

            print("-----LOGGING----- before queryEngine.query")
            myStreamResponse = queryEngine.query(prompt)
            print("-----LOGGING----- after queryEngine.query")
            
            for text in myStreamResponse.response_gen:
                print(text,end='')
                message = {
                    'event': 'text-generated',
                    'text': text
                }
                await websocket.send(json.dumps(message))
                await asyncio.sleep(0.05)
            
                
    except websockets.exceptions.ConnectionClosedOK as e:
        # set authID to null when client disconnects to avoid authID conflict
        print("Client Disconnected !",path)
        
    except websockets.exceptions.ConnectionClosedError as e:
        print("Client Disconnected !",path)
    # handle 1000 error code i.e. normal closure
    except websockets.exceptions.ConnectionClosed as e:
        print("Client Disconnected !",path)

async def main():

    ISDOCKER = False
    PORT = 2023

    SERVER_URL = "0.0.0.0" if ISDOCKER else "127.0.0.1"

    start_server = await websockets.serve(transmit, SERVER_URL, PORT)

    print("Server Started with URL : ", start_server.server)
    print("Started server on port : ", PORT)

    await start_server.wait_closed()

asyncio.run(main())
