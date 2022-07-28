import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_nam
        )
        self.accept()


        #연결되었는지 확인하기 위해 보내는 가라 메시지
        self.send(text_data=json.dumps({
            'type':'connexction_extablished',
            'message':'You are now connected'
        }))

    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

        # print(message)
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))