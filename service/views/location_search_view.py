from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.services import LocationService

from service.serializers.location_serializer import LocationSerializer 

class LocationSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        result = LocationService.get_or_fetch_location(query)
        
        if result['status'] == "SUCCESS":
            serializer = LocationSerializer(result['data'])
            return Response({"data": serializer.data, "status": "SUCCESS"}, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_202_ACCEPTED)