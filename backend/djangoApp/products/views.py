from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings


class StreamView(APIView):

	def post(self, request):
		# Запись данных в поток
		data = request.data
		stream_name = 'mystream'

		if not data:
			return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)

		# Добавляем запись в поток
		record_id = settings.redis_client.xadd(stream_name, data)
		return Response({'message': 'Record added', 'id': record_id}, status=status.HTTP_201_CREATED)

	def get(self, request):
		# Чтение из потока
		stream_name = 'mystream'
		# Читаем последние 10 записей
		records = settings.redis_client.xrevrange(stream_name, count=10)

		# Форматируем данные для ответа
		formatted_records = []
		for record in records:
			formatted_records.append({
				'id': record[0],
				'data': dict(record[1])
			})

		return Response({'records': formatted_records}, status=status.HTTP_200_OK)
