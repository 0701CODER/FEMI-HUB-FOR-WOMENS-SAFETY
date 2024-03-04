from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime
from django.conf import settings
from django.http import JsonResponse
def home(request):
	return render(request,'index.html',{})
def register(request):
	if request.method == 'POST':
		name = request.POST.get('username')
		address = request.POST.get('address')
		mobile= request.POST.get('mobile')
		email = request.POST.get('email')
		password = request.POST.get('password')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		country = request.POST.get('country')
		city = request.POST.get('city')
		zip = request.POST.get('zip')
		crt = Register_Detail.objects.create(name=name,
		address=address,mobile=mobile,password=password,email=email,fname=fname,lname=lname,
		city=city,country=country,zip=zip)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def dashboard(request):
	return render(request,'dashboard.html',{})
def user_login(request):
	if request.session.has_key('username'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Register_Detail.objects.filter(email=username,password=password)
			if post:
				username = request.POST.get('username')
				request.session['username'] = username
				a = request.session['username']
				sess = Register_Detail.objects.only('id').get(email=a).id
				request.session['user_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'login.html',{})
def logout(request):
	try:
		del request.session['username']
		del request.session['user_id']
	except:
		pass
	return render(request, 'login.html', {})
def add_post(request):
	user_id=request.session['user_id']
	if request.method == 'POST':
		title=request.POST.get('title')
		description=request.POST.get('description')
		image =request.FILES['image']
		uid=Register_Detail.objects.get(id=int(user_id))
		prt = Post.objects.create(title=title,description=description,
		image=image,user_id=uid)
		if prt:
			messages.success(request,'Post Added Successfully')
	return render(request,'add_post.html',{})
def post(request):
	user_id=request.session['user_id']
	if request.session.has_key('username'):
		detail=Post.objects.filter(user_id=int(user_id))
		return render(request,'post.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def delete(request,pk):
	a=Post.objects.filter(id=pk).delete()
	return redirect('post')
def all_post(request):
	if request.session.has_key('username'):
		detail=Post.objects.all()
		cursor = connection.cursor()
		post = ''' SELECT Count(app_feedback.comment) from app_feedback 
		GROUP BY app_feedback.post_id_id '''
		sub = cursor.execute(post)
		row = cursor.fetchall()
		post1 = ''' SELECT Count(app_post_feedback.like_post) from app_post_feedback 
		where app_post_feedback.like_post='Yes' GROUP BY app_post_feedback.post_id_id '''
		sub1 = cursor.execute(post1)
		row1 = cursor.fetchall()
		post2 = ''' SELECT Count(app_post_feedback.report_post) from app_post_feedback 
		where app_post_feedback.report_post='Yes' GROUP BY app_post_feedback.post_id_id '''
		sub2 = cursor.execute(post2)
		row2 = cursor.fetchall()
		return render(request,'all_post.html',{'row2':row2,'detail':detail,'row':row,'row1':row1})
	else:
		return render(request,'login.html',{})
def post_comment(request,pk):
	if request.session.has_key('user_id'):
		user_id = request.session['user_id']
		if request.method == 'POST':
			food_id = Post.objects.get(id=pk)
			uid = Register_Detail.objects.get(id=int(user_id))
			comment = request.POST.get('comment')
			already_exist = Feedback.objects.filter(post_id=pk,user_id=int(user_id))
			if already_exist:
				messages.success(request,'You Already Comment.')
			else:
				crt = Feedback.objects.create(post_id=food_id,user_id=uid,comment=comment)
		comment_detail = Feedback.objects.filter(post_id=pk)
		tot = Feedback.objects.filter(post_id=pk).aggregate(Count('comment'))
		
		return render(request,'comment.html',{'comment_detail':comment_detail,'tot':tot})
	else:
		return render(request,'login.html',{})	
def like_post(request,pk):
	user_id=request.session['user_id']
	post_id=Post.objects.get(id=pk)
	uid=Register_Detail.objects.get(id=int(user_id))
	prt = Post_Feedback.objects.create(post_id=post_id,like_post='Yes',
	user_id=uid)
	return redirect('all_post')
def report_post(request,pk):
	user_id=request.session['user_id']
	post_id=Post.objects.get(id=pk)
	uid=Register_Detail.objects.get(id=int(user_id))
	prt = Post_Feedback.objects.create(post_id=post_id,report_post='Yes',
	user_id=uid)
	return redirect('all_post')
def women_rights(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail=Women_Right.objects.all()
		return render(request,'women_right.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def ngo(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail=NGO.objects.all()
		return render(request,'ngo.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def all_users(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		cursor = connection.cursor()
		post = ''' SELECT r.name,f.status,f.user_id_id,r.id,f.id from app_register_detail as r LEFT JOIN app_followuser as f
		ON r.id=f.follow_id  where r.id!='%d' ''' %(int(user_id)) 
		sub = cursor.execute(post)
		row = cursor.fetchall()
		return render(request,'all_users.html',{'row':row})
	else:
		return render(request,'login.html',{})
def follow(request,pk):
	user_id=request.session['user_id']
	uid = Register_Detail.objects.get(id=int(user_id))
	FollowUser.objects.create(user_id=uid,follow_id=pk,status='Follow')
	return redirect('all_users')
def unfollow(request,pk):
	user_id=request.session['user_id']
	exist = FollowUser.objects.filter(follow_id=pk,user_id=int(user_id),status='Follow')
	if exist:
		FollowUser.objects.filter(follow_id=pk,user_id=int(user_id),status='Follow').delete()
	
	return redirect('all_users')
def profile(request,pk):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		detail = Post.objects.filter(user_id=pk)
		user = Register_Detail.objects.filter(id=pk)
		return render(request,'profile.html',{'detail':detail,'user':user})
	else:
		return render(request,'login.html',{})
def friends_list(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		cursor = connection.cursor()
		post = ''' SELECT r.name,f.status,f.follow_id,r.id,f.id from app_register_detail as r INNER JOIN app_followuser as f
		ON r.id=f.follow_id  where f.status='Follow' ''' 
		sub = cursor.execute(post)
		row = cursor.fetchall()
		return render(request,'friends_list.html',{'row':row})
	else:
		return render(request,'login.html',{})
def edit_profile(request):
	if request.session.has_key('username'):
		user_id=request.session['user_id']
		user = Register_Detail.objects.filter(id=int(user_id))
		if request.method == 'POST':
			address = request.POST.get('address')
			mobile= request.POST.get('mobile')
			email = request.POST.get('email')
			fname = request.POST.get('fname')
			lname = request.POST.get('lname')
			country = request.POST.get('country')
			city = request.POST.get('city')
			zip = request.POST.get('zip')
			crt = Register_Detail.objects.filter(id=int(user_id)).update(
			address=address,mobile=mobile,email=email,fname=fname,lname=lname,
			city=city,country=country,zip=zip)
			if crt:
				messages.success(request,'Profile Updated Successfully')
		return render(request,'edit_profile.html',{'user':user})
	else:
		return render(request,'login.html',{})