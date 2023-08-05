import socketio

sio = socketio.AsyncClient()

# expose those as ploupy functions
sleep = sio.sleep
start_background_task = sio.start_background_task
