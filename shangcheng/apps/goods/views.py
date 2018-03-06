from django.shortcuts import render
from django.views.generic import View


class GoodsView(View):
    def get(self,request):
        render(request, '../../static/index.html')
