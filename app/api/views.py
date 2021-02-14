import json

from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .models import Users, Message


def user_message_info(request, user_id, message_id):

    # GET localhost:80/api/v1/user/34452/comment/456
    # Ответ сервиса: {"id":456, "id_user":34452, "txt":"My comment"}
    if request.method == 'GET':
        if Users.objects.filter(pk=user_id).exists():
            user_name = Users.objects.get(pk=user_id)
            result_message = 'Сообщения с таким id не существует'
            if Message.objects.filter(name=user_name, pk=message_id).exists():
                message = Message.objects.filter(name=user_name, pk=message_id)
                result_message = str(message[0])

            data = {"id": message_id, "id_user": user_id, "txt": result_message}

            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)
        else:
            data = {"error": "user not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)


@csrf_exempt
def all_user_message(request, user_id):

    # GET localhost:80/api/v1/user/34452/comment/
    # Ответ сервиса: [{"id":456, "id_user":34452, "txt":"My comment"},{"id":460, "id_user":34452, "txt":"Foo!"}]
    if request.method == 'GET':
        data_list = []

        if Users.objects.filter(pk=user_id).exists():
            user_name = Users.objects.get(pk=user_id)
            if Message.objects.filter(name=user_name).exists():
                messages = Message.objects.filter(name=user_name).all()
                for message in messages:
                    data_dicts = {'id': message.pk, 'id_user': user_id, 'txt': message.messages}
                    data_list.append(data_dicts)
                data = {"messages": str(data_list)}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
            else:
                data = {"error": "user don't have messages"}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
        else:
            data = {"error": "user not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)

    # POST localhost:80/api/v1/user/34452/comment/
    # Ответ сервиса: {"id": 470}
    if request.method == 'POST':
        if Users.objects.filter(pk=user_id).exists():
            if 'txt' in request.POST:
                user_name = Users.objects.get(pk=user_id)
                text = request.POST.get('txt')
                message = Message(name=user_name, messages=text)
                message.save()

                data = {"id": message.pk}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
            else:
                data = {"error": "please send a POST request with the key 'txt' - {'txt': 'any message'}"}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
        else:
            data = {"error": "user not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)


def user_info(request, user_id):

    # GET localhost:80/api/v1/user/34452
    # Ответ сервиса: {"id":34452, "name":"Vasya", "email":"vasya@google"}
    if request.method == 'GET':
        if Users.objects.filter(pk=user_id).exists():
            user_name = Users.objects.get(pk=user_id)
            data = {
                "id": user_id,
                "name": user_name.name,
                "email": user_name.email,
            }
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)
        else:
            data = {"error": "user not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)


@csrf_exempt
def comment_info(request, message_id):

    # GET localhost:80/api/v1/comment/456
    # Ответ сервиса: {"id":456, "id_user":34452, "txt":"My comment"}
    if request.method == 'GET':
        if Message.objects.filter(pk=message_id).exists():
            message = Message.objects.get(pk=message_id)

            data = {"id": message_id, "id_user": message.name.pk, "txt": message.messages}

            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)
        else:
            data = {"error": "message not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)

    # PUT localhost:80/api/v1/comment/460
    # Ответ сервиса: {"id":460}
    if request.method == 'PUT':
        if Message.objects.filter(pk=message_id).exists():
            if 'txt' in str(request.body):
                obj = Message.objects.get(pk=message_id)
                text = QueryDict(request.body)['txt']

                updated_message = Message(pk=message_id, name=obj.name, messages=text)
                updated_message.save()

                data = {"id": message_id}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
            else:
                data = {"error": "please send a PUT request with the key 'txt' - {'txt': 'any message'}"}
                json_string = json.loads(json.dumps(data))
                return JsonResponse(data=json_string)
        else:
            data = {"error": "message not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)

    # DELETE localhost:80/api/v1/comment/460
    # Ответ сервиса: {"id":460}
    if request.method == 'DELETE':
        if Message.objects.filter(pk=message_id).exists():
            message_to_remove = Message(pk=message_id)
            message_to_remove.delete()

            data = {"id": message_id}

            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)
        else:
            data = {"error": "message not found"}
            json_string = json.loads(json.dumps(data))
            return JsonResponse(data=json_string)
