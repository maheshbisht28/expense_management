from django.views import generic, View

#from .models import attendance1 , new1, new2
#from operator import attrgetter
from django.shortcuts import render
import numpy as np
from .forms import Registrationform ,Add_expense_form,show_expense_form,date_form
import  time
from django.http import HttpResponse
# from imutils.video import VideoStream
import base64
from .models import User, Category, Expense
import os
from datetime import date, timedelta

startdate = date.today()
# import face_recognition
# import argparse
# import pickle
# import cv2
# import numpy as np
# from PIL import Image
# import io
# import pandas as pd
# from django.contrib import messages
# import datetime
from django.db.models import Sum, Count
from itertools import chain
from django.core.files import File
from django.http import QueryDict
from django.contrib import messages
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT  = os.path.join(module_dir, 'media')


class index(View):
	#model=Post
	def get(self,request):
		#sset = Post.objects.filter(category='travel').order_by('-created_on')
		#posts=Post.objects.all()[0:3]
		#freqs=Post.objects.values('category').order_by().annotate(Count('category'))
		return render(request,'index.html') #,{'sset':sset,'freqs':freqs,'posts':posts,})


def Register(request):
	new_stud=Registrationform()
	return render(request,"Register.html",{"form":new_stud})
		

def User_dashboard(request):
	return render(request, "User_dashboard.html")	

def add_user(request):
	if request.method =='POST':

		new_stud=Registrationform(request.POST)
		
		print("vvdvd ",new_stud.is_valid())
		
		if new_stud.is_valid():
			print("in ",new_stud)
			new_stud.save(True)
			
			return render(request, "User_dashboard.html") 

		else:
			return render(request,'Register.html',{'form':new_stud} ) 
	else:

		new_stud=Registrationform()
		return render(request,'Register.html',{'form':new_stud} )		

def Add_Expenses(request):
	print(request.POST)
	if request.method =='POST':
		
		expense_obj=Add_expense_form(request.POST)
		if expense_obj.is_valid():
			obj=expense_obj.save(True)
			print(obj.id)
			messages.success(request,"Expense Successfully Created ")
			form=Add_expense_form()
			return render(request, "add_expenses.html",{'form':form}) 

		else:
			return render(request,'add_expenses.html',{'form':expense_obj} ) 
	else:

		expense_obj=Add_expense_form()
		return render(request,'add_expenses.html',{'form':expense_obj} )

 

def Show_Expenses(request):
	if request.method =='POST':
		print(request.user.id) 
		print(request.POST)
		qdict=dict(request.POST)
		us=User.objects.filter(id=request.user.id).values("id")[0]
		# print("request.course_id ",request.course_id)
		# print("us ",dict(request.POST))
		
		# print("cat ",qdict["category"])
		if 'category' in qdict:
				
			if qdict["category"]==['0000']:
				form1=Expense.objects.filter(user=us["id"]).all()
				lables=set()
				data=[]
				dc=dict()
				sum=0
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money	
				print(list(dc.keys())," ",list(dc.values()))
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum, 'labels': list(dc.keys()),
        'data': list(dc.values())})
			else:
				cat=(Category.objects.filter(id__in=qdict["category"]).values("id"))[0]
				form1=Expense.objects.filter(user=us["id"],category=cat["id"]).all()
				sum=0
				lables=set()
				data=[]
				dc=dict()
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum,'labels': list(dc.keys()),
        'data': list(dc.values())})
		else:
			dte_s=qdict['date_start']
			dte_e=qdict['date_end']
			# form=[]
			if dte_s[0]!='' and dte_e[0]!='':
				form1=Expense.objects.filter(user=us["id"],date__range=[dte_s[0], dte_e[0]]).all()
				sum=0;	
				lables=set()
				data=[]
				dc=dict()
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money				
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum,'labels': list(dc.keys()),
        'data': list(dc.values())})
			elif dte_s[0]!='' and dte_e[0]=='':
				enddate = date.today()
				form1=Expense.objects.filter(user=us["id"],date__range=[dte_s[0],enddate]).all()
				sum=0;	
				lables=set()
				data=[]
				dc=dict()
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money				
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum,'labels': list(dc.keys()),
        'data': list(dc.values())})
			elif dte_s[0]=='' and dte_e[0]!='':
				start = date(2012, 12, 11)
				form1=Expense.objects.filter(user=us["id"],date__range=[start,dte_e[0]]).all()
				sum=0;	
				lables=set()
				data=[]
				dc=dict()
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money				
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum,'labels': list(dc.keys()),
        'data': list(dc.values())})
			else:	
				form1=Expense.objects.filter(user=us["id"]).all()
				sum=0;	
				lables=set()
				data=[]
				dc=dict()
				for i in form1:
					# labels=i.category.c_name
					ls=i.category.c_name
					if ls in dc:
						dc[ls]+=i.money
					else:
						dc[ls]=i.money
					sum+=i.money				
				return render(request,"show_exp_by_categ.html",{"form":form1,"sum":sum,'labels': list(dc.keys()),
        'data': list(dc.values())})

		# form=Expense.objects.filter(user=us["id"],category=cat["id"]).all()
		
	else:
		form_cat=Category.objects.all()
		form_date=date_form();	
		return render(request,"show_filter_expense.html",{"form_cat":form_cat,"form_date":form_date})		


def edit_expense(request,pk):
	if request.method =='POST':
		print(request.POST)
		form =Add_expense_form(request.POST,instance=Expense.objects.get(pk=pk))
		print("pk ",pk)
		print("form ",form)

		if "Submit" in request.POST:
			if form.is_valid():
				form.save()
				print("form.save()")
				obj=Expense.objects.filter(id=pk).all()[0];
				ex_obj=Add_expense_form(initial={'user':obj.id,
					'category':obj.category,'ex_name':obj.ex_name,
					'date':obj.date,'money':obj.money,'desc':obj.desc})
				messages.success(request,"Expense Successfully Updated ")				
				return render(request,"edit_expen.html",{"form":form,'id':pk})
		else:
			Expense.objects.filter(id=pk).delete()
			messages.success(request,"Record Successfully Deleted ")				
			return render(request,"User_dashboard.html")			

				
	else:
		# print("request.POST.get('id') ",pk)
		obj=Expense.objects.filter(id=pk).all()[0];
		ex_obj=Add_expense_form(initial={'user':obj.id,
			'category':obj.category,'ex_name':obj.ex_name,
			'date':obj.date,'money':obj.money,'desc':obj.desc})
		print(obj.money)
		# print("ex_obj ",ex_obj)
		# print("ex_obj ",ex_obj["id"])
		return render(request,"edit_expen.html",{"form":ex_obj,'id':pk})
