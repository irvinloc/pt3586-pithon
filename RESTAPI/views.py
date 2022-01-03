from django.views import View
from .models import User, UserDetail
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import requests
from django.utils.decorators import method_decorator
import json

class UserListView(View):
    def get(self, request):
        clist = User.objects.all()
        return JsonResponse(list(clist.values()), safe=False) #

    @csrf_exempt
    def dispatch(self,request, *args, **kwargs):
        return super(UserListView,self).dispatch(request,*args, **kwargs)

    # @method_decorator(csrf_protect)
    def post(self, request):
        user_data=request.body.decode("utf8")
        user_data=json.loads(user_data)

        try:
            new_user=User(name=user_data["name"])
            new_zip = user_data["zip"]
            if not new_user or not new_zip:
                res = {
                    "success": False,
                    "message": "invalid data",
                    "status": "400"
                }
                return JsonResponse(res)


            r = requests.get("http://api.geonames.org/postalCodeSearchJSON?postalcode=" + new_zip + "&country=ES&maxRows=1&username=irvinloc", timeout=10)
            print('request code', r.status_code)
            if r.status_code == 200:
                data = r.json()
                # print("second data,",data)
                if len(data["postalCodes"])==0:
                    res = {
                        "success": False,
                        "message": "Zip not found," + new_zip,
                        "status": "400"
                    }
                    return JsonResponse(res)
                city = data["postalCodes"][0]["placeName"]
                new_user_detail = UserDetail(user=new_user, zip=new_zip, city=city)

                new_user.save()
                new_user_detail.save()
                # print("city,", city)
                res = {
                    "success": True,
                    "message": "user data saved successfully",
                    "city": city,
                    "status" : "201"
                }
                return JsonResponse(res, safe=False)
            else:
                res = {
                    "success": False,
                    "message":"invalid data",
                    "status": "400"
                }
                return JsonResponse(res)
        except Exception as e:
            print(e)
            return JsonResponse({"error":"something went wrong, " + str(e) },safe=False)


    # def put(self, request):
    #     # put
    # def delete(self, request):
    #     # delete

class UserDetailView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return JsonResponse(model_to_dict(user), safe=False)

class UserDetailListView(View):
    def get(self, request):
        clist = UserDetail.objects.all()
        return JsonResponse(list(clist.values()), safe=False)  #
    # def post(self, request):
    #     # post
    # def put(self, request):
    #     # put
    # def delete(selfself, request):
    #     # delete

class UserDetailDetailView(View):
    def get(self, request, pk):
        user_detail = UserDetail.objects.get(pk=pk)
        return JsonResponse(model_to_dict(user_detail), safe=False)

                # def post(self, request):
    #
    # # post
    # def put(self, request):
    #
    # # put
    # def delete(selfself, request):
# delete