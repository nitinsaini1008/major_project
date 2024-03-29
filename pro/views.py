from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import products,items,cart,buyed,order_count,allorder,re_views
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import smtplib
from validate_email import validate_email
import random
import requests
import json
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.conf import settings
from .paytm import generate_checksum, verify_checksum

def home(request):
	return render(request,'home.html')

def main_page(request):
	f=products.objects.all()
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	return render(request,'main_page.html',{'d':f, "l": l})

@login_required
def save_reviews(request,id):
	point=request.POST['rate']
	msg=request.POST['msg']
	item=items.objects.get(id=id)
	try:
		point=int(point)
	except:
		point=1
	r=re_views(point=point,name=request.user,product=item,msg=msg)
	r.save()
	return redirect('/details/'+str(id))

def details(request,id):
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	try:
		i=items.objects.get(id=id)
		r=re_views.objects.all().filter(product=i).order_by('-datetime')
		return render(request,'details.html',{'i':i,'r':r, "l": l})
	except:
		return HttpResponse("No record found")
		
def sub_page(request):
	name=request.GET['search']
	d=products.objects.get(name=name)
	f=d.item.all()
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	return render(request,'sub_page.html',{'f':f, "l": l})

def search_name(request):
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	name=request.GET['search']
	ans = items.objects.filter(Q(name__icontains=name)| Q(desc__icontains=name) | Q(type_of_item__icontains=name))
	return render(request,'search_name.html',{'d':ans, "l": l})
	
@login_required
def buy(request):
	print(request.user.email)
	idd=request.GET['id']
	try:
		print("hello_1")
		d=items.objects.get(id=idd)
		b=buyed.objects.all().filter(item=d)[0]
		c=cart.objects.get(name=request.user)
		b=c.item.all().filter(item=d)[0]
		c.item.remove(b)
		c.save()
		c.cost-=(b.total_item)*d.price
		b.total_item+=1
		b.save()
		print("hello_1")
		c.item.add(b)

		c.cost+=(b.total_item)*d.price
		c.save()
		return redirect('my_cart')
	except:
		print("hello_2")
		d=items.objects.get(id=idd)
		b=buyed(item=d,total_item=1)
		b.save()
		c=cart.objects.get(name=request.user)
		c.item.add(b)
		c.cost+=(b.total_item)*d.price
		c.save()
		return redirect('my_cart')
	return HttpResponse("an error accupied")

def log_in(request):
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	if request.method=='POST':
		username=request.POST['username']
		passwd=request.POST['passwd']
		u=authenticate(username=username,password=passwd)
		if u is not None:
			auth.login(request,u)
			try:
				c=cart.objects.get(name=request.user)
			except:
				c=cart(name=request.user,cost=0)
				c.save()
			return redirect("main_page")
		else:
			return render(request,'log_in.html',{'msg':"invalid username and password", "l": l})

	return render(request,'log_in.html',{'msg':"", "l": l})

def sign_in(request):
	return render(request,'sign_in.html')

def post_sign(request):
	email_id = request.GET.get("email")
	username = request.GET.get("username")
	try:
		user = User.objects.get(Q(username = email_id)| Q(username=username))
		return HttpResponse("Username already exists")
	except:
		pass
	x = random.randint(1000,99999)
	text_content = "<h1>Dear User your One Time Password is {}</h1>".format(x)
	try:
		email=EmailMultiAlternatives(
	            "OTP",text_content,"coder.kolawat@gmail.com",[email_id]
	        )
		email.attach_alternative(text_content, "text/html")
		email.send()
	except:
		pass
	return HttpResponse(str(x))

def sign_2(request):
	username=request.GET['username']
	pass_1=request.GET['pass_1']
	pass_2=request.GET['pass_1']
	email=request.GET['email']
	first_name=request.GET['first_name']
	last_name=request.GET['last_name']
	u=User.objects.create_user(username=username,email=email,password=pass_2,first_name=first_name,last_name=last_name)
	u.set_password(pass_2)
	u.save()
	auth.login(request,u)
	try:
		c=cart.objects.get(name=request.user)
	except:
		c=cart(name=request.user,cost=0)
		c.save()
	return redirect('main_page')

@login_required
def log_out(request):
	auth.logout(request)
	return redirect('main_page')

@login_required
def my_cart(request):
	try:
		c=cart.objects.get(name=request.user)
		l=c.item.count()
		return render(request,'my_cart.html',{'c':c,'l':l})
	except:
		c=cart(name=request.user,cost=0)
		c.save()
	return render(request,'my_cart.html',{'c':c,'msg':'not modified'})

@login_required
def delete_cart(request):
	idd=request.GET['id']
	t=items.objects.get(id=idd)
	c=cart.objects.get(name=request.user)
	b=c.item.all().filter(item=t)[0]
	#b=buyed.objects.all().filter(item=t)[0]
	if b.total_item==1:
		b.delete()
		c.item.remove(b)
		c.cost-=t.price
		c.save()
		return redirect('my_cart')
	else:
		b.total_item-=1
		c.item.remove(b)
		b.save()
		c.item.add(b)
		c.cost-=t.price
		c.save()
		return redirect("my_cart")

def about(request):
	return HttpResponse("about page")

@login_required
def account(request):
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	d=allorder.objects.filter(name=request.user).order_by('-datetime')
	return render(request,'account.html',{'d':d, "l": l})

def send_mail(to, subject, text_content):
	email=EmailMultiAlternatives(
            subject,text_content,"coder.kolawat@gmail.com",to
        )
	email.attach_alternative(text_content, "text/html")
	email.send()
	return True

@login_required
def clear_cart(request):
	c = cart.objects.get(name=request.user)
	c.item.clear()
	c.cost = 0
	c.save()
	return redirect("my_cart")

@login_required
def pre_buy(request):
	l = 0
	if(request.user.is_authenticated):
		l=cart.objects.get(name=request.user).item.count()
	c=cart.objects.get(name=request.user)
	if request.method=='POST':
		payment_mode = request.POST['payment-option']
		country=request.POST['country']
		state=request.POST['state']
		city=request.POST['city']
		address=request.POST['address']
		mobile = request.POST['mobile']
		ad=address+','+city+','+state+','+country
		a=allorder(name=request.user,cost=0,address=ad, mobile=str(mobile))
		a.save()
		xx=0
		for i in c.item.all():
			x=i.item
			y=i.total_item
			xx+=(y*x.price)
			z=order_count(item=x,item_count=y)
			z.save()
			a.item.add(z)
		a.cost=xx
		a.save()
		c.item.clear()
		c.cost = 0
		c.save()
		try:
			text_content = "<h1>Dear user your order has been placed and total cost is {}</h1>".format(str(xx))
			# send_mail([request.user.email], "Order has been placed!", text_content)
		except:
			print("Mail send failed--------\n\n")
		#Start-----------------
		if payment_mode == "COD":
			return redirect('account')
		merchant_key = settings.PAYTM_SECRET_KEY
		params = (
			('MID', settings.PAYTM_MERCHANT_ID),
			('ORDER_ID', str(123847987)+str(a.id)),
			('CUST_ID', str(request.user.email)),
			('TXN_AMOUNT', str(xx)),
			('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
			('WEBSITE', settings.PAYTM_WEBSITE),
			# ('EMAIL', request.user.email),
			# ('MOBILE_N0', '9911223388'),
			('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
			('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
			# ('PAYMENT_MODE_ONLY', 'NO'),
		)

		paytm_params = dict(params)
		checksum = str("".join([str(1) for i in range(0, 108)]))
		checksum = generate_checksum(paytm_params, merchant_key)

		paytm_params['CHECKSUMHASH'] = checksum
		return render(request, 'payment.html', context=paytm_params)

		# return redirect('account')
	return render(request,'pre_buy.html',{'c':c, "l": l})

def result(request):
	code=request.GET['code']
	state=request.GET['state']

	url='https://oauth2.googleapis.com/token'
	data = {'grant_type':'authorization_code',
			'code':code,
            'redirect_uri':'http://127.0.0.1:8000/result',
            'client_id':'296287171867-ioqtsh35387i6tsv37dbo0te2d965tbt.apps.googleusercontent.com',
            'client_secret':'eZTrFIn6pADFyxpxeD3vqRxz'
            }
	r=requests.post(url,data=data)
	token=r.json()['access_token']
	id_token=r.json()['id_token']
	url='https://oauth2.googleapis.com/tokeninfo?id_token='+id_token
	url = "https://www.googleapis.com/oauth2/v2/userinfo?access_token="+token
	r = requests.get(url)
	data = r.json()
	# print( data['email'], data['name'], data['id'])

	try:
		u = User.objects.get(username=data['email'])
		u = User.objects.filter(email = data['email']).first()
	except:
		u=User.objects.create_user(username=data['email'],email=data['email'],password=data['id'],first_name=data['email'].split("@")[0],last_name="")
		u.set_password(data['id'])
		u.save()
	auth.login(request,u)
	try:
		c=cart.objects.get(name=request.user)
	except:
		c=cart(name=request.user,cost=0)
		c.save()
	return redirect('main_page')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		id = str(received_data['ORDERID'][0])[9:]
		order = allorder.objects.get(id=id)
		order.paid=True
		order.save()
		print(received_data['ORDERID'][0], "---------")
		return redirect("account")
