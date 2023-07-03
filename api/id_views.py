from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
import idanalyzer
import datetime

id_key = "xNQa9B99ZEiQZV4PcScOjvjOTR34LdOp"

class IDVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        
        url = request.data.url
        coreapi = idanalyzer.CoreAPI(id_key, "US")
        coreapi.enable_authentication(True, 2)
        id_response = coreapi.scan(document_primary=url)
        try:
            id_result = id_response["result"]
            id_auth = id_response["authentication"]
            
            year = id_result["dob_year"]
            month = id_result["dob_month"]
            day = id_result["dob_day"]
            age = datetime.timedelta(year=year, month=month, day=day)

            auth_score = id_auth["score"]

            if age > datetime.timedelta(years=18) and auth_score >= 0.5:
                request.user.verified = True
                request.user.save()
                return Response(status=status.HTTP_200_OK)
            else :
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        


        return Response({'url' : url}, status=status.HTTP_200_OK)