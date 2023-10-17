import websockets
import asyncio
import json
import my_llm
import time

PORT = 2023
ENGINE = "LOCAL"

# create a VideoCapture object
llm =  None if ENGINE == "API" else my_llm.get_llm() 
queryEngine = my_llm.openAI_queryEngine() if ENGINE == "API" else my_llm.get_query_engine(llm)

async def transmit(websocket, path):
    print("Client Connected !",path,'********************************************************')
    # print(query)
    try :
        query = ''
        # query.strip()
        
        while True:
            query = await websocket.recv()
            # print(query)
            # convert to dict
            query = json.loads(query)
            print(query)

            prompt = f"""Answer within context of {query["game"]}.
            Question : {query["question"]}
            Instructions : answer the question STRICTLY in the context of the game. You cannot invent any new information, but are allowed to draw conclusions from the existing knowledge base of {query["game"]}.csv.
            What is the sentiment score of the reviews out of 10? Mention it at the start of your answer.
            Use \n token to symbolize the number of newlines after each paragraph.
            Use \t token at the start of sentences to symbolize tab space wherever required.
            """

            # query.strip()
            
            # if query == "disconnect_server":
            #     await websocket.send("Bye !")
            #     break

            # -----------------------------------------------------------------
            
            myStreamResponse =queryEngine.query(prompt)
            for text in myStreamResponse.response_gen:
                print(text,end='')
                message = {
                    'event': 'text-generated',
                    'text': text
                }
                await websocket.send(json.dumps(message))
                await asyncio.sleep(0.05)
            
            # -----------------------------------------------------------------
            # TEST
            # for i in range(20):
            #     # print(text,end='')
            #     print("Sending to client")

            #     if i==19:
            #         message = {
            #             'event': 'dev-test-endpoint',
            #             'text': "ENDEND"
            #         }
            #         await websocket.send(json.dumps(message))
            #         await asyncio.sleep(0.5)
            #         break

            #     message = {
            #         'event': 'dev-test-endpoint',
            #         'text': "couldhavewouldhaveshouldhave\\n"
            #     }
            #     await websocket.send(json.dumps(message))
            #     await asyncio.sleep(0.5)

            # -----------------------------------------------------------------

                # response = response + text
                # await websocket.send('text-generated',text)
                # await websocket.send(str(text))  
            # await websocket.send(response)
            
            # -----------------------------------------------------------------
            # response_iter = llm.stream_complete(query)
            # for response in response_iter:
            #     print(response.delta, end="", flush=True)
            #     myResponse = myResponse + response.delta
            
                
    except websockets.exceptions.ConnectionClosedOK as e:
        # set authID to null when client disconnects to avoid authID conflict
        print("Client Disconnected !",path)
        
    except websockets.exceptions.ConnectionClosedError as e:
        print("Client Disconnected !",path)
    # handle 1000 error code i.e. normal closure
    except websockets.exceptions.ConnectionClosed as e:
        print("Client Disconnected !",path)

async def main():
    
    # start_server = await websockets.serve(transmit, "192.168.255.31", PORT)
    start_server = await websockets.serve(transmit, "localhost", PORT)
    print("Server Started with URL : ", start_server.server)
    print("Started server on port : ", PORT)
    await start_server.wait_closed()

asyncio.run(main())
