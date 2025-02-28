from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse
from django.db.models import Sum
import datetime
def home(request):
	return render(request,'index.html',{})
def dashboard(request):
	today = datetime.datetime.now()
	a = today.day
	b = today.year
	c = today.month
	detail = Disease_Detail.objects.filter(date=datetime.date(b, c, a))
	return render(request,'dashboard.html',{'detail':detail})
def admin_dashboard(request):
	return render(request,'admin_dashboard.html',{})
def disease_alert(request):
	detail = Disease_Detail.objects.all().order_by('-id')
	return render(request,'disease_alert.html',{'detail':detail})
def cdisease_alert(request):
	detail = Disease_Detail.objects.all().order_by('-id')
	return render(request,'cdisease_alert.html',{'detail':detail})
def doctor_register(request):
	if request.method == 'POST':
		h__name = request.POST.get('hname')
		d_name = request.POST.get('dname')
		email = request.POST.get('email')
		uname = request.POST.get('uname')
		psw = request.POST.get('psw')
		degree = request.POST.get('degree')
		spec = request.POST.get('spec')
		pnum = request.POST.get('pnum')
		dlnum = request.POST.get('dlnum')
		hlnum = request.POST.get('hlnum')
		country = request.POST.get('country')
		state = request.POST.get('state')
		city = request.POST.get('city')
		addr = request.POST.get('addr')
		doc_type = request.POST.get('doc_type')
		lic = Doctor_Detail.objects.filter(doc_license_no=dlnum,hospital_license_no=hlnum)
		if lic:
			crt = Doctor_Register.objects.create(hospital_name=h__name,doctor_name=d_name,mail=email,mobile=pnum,doc_license_no=dlnum,
			hospital_license_no=hlnum,degree=degree,specialist=spec,username=uname,password=psw,
			country=country,state=state,city=city,hospital_address=addr,doctor_type=doc_type)
			if crt:
				messages.success(request,'Registered Successfully')
		else:
			messages.success(request,'Invalid License Number')

	return render(request,'doctor_register.html',{})
def customer_register(request):
	if request.method == 'POST':
		cname = request.POST.get('cname')
		mail = request.POST.get('mail')
		num = request.POST.get('num')
		uname = request.POST.get('uname')
		psw = request.POST.get('psw')
		country = request.POST.get('country')
		state = request.POST.get('state')
		city = request.POST.get('city')
		addr = request.POST.get('addr')
		lic = Customer_Detail.objects.filter(username=uname)
		if lic:
			messages.success(request,'User Alredy Exist')
		else:
			crt = Customer_Detail.objects.create(name=cname,email=mail,username=uname,
			phone_number=num,country=country,state=state,city=city,address=addr,password=psw)
			if crt:
				messages.success(request,'Registered Successfully')
	return render(request,'customer_register.html',{})
def customer_login(request):
	if request.session.has_key('customer'):
		return redirect("customer_dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('uname')
			password =  request.POST.get('psw')
			post = Customer_Detail.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('uname')
				request.session['customer'] = username
				a = request.session['customer']
				sess = Customer_Detail.objects.only('id').get(username=a).id
				request.session['cus_id']=sess
				return redirect("customer_dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'customer_login.html',{})
def doctor_login(request):
	if request.session.has_key('username'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('uname')
			password =  request.POST.get('psw')
			post = Doctor_Register.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('uname')
				request.session['username'] = username
				a = request.session['username']
				sess = Doctor_Register.objects.only('id').get(username=a).id
				request.session['doc_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'doctor_login.html',{})
def add_visiting_hour(request):
	if request.session.has_key('username'):
		if request.method == 'POST':
			hospital_id = request.POST.get('hospital_id')
			ids = Doctor_Register.objects.get(id=int(hospital_id))
			vh = request.POST.get('vweekday')
			vw = request.POST.get('vweekend')
			ow = request.POST.get('onweekday')
			oe = request.POST.get('onweekend')
			crt = Visiting_Detail.objects.create(hospital_id=ids,visiting_hour_weekdays=vh,visiting_hour_weekend=vw,
			visiting_hour_online_weekdays=ow,visiting_hour_online_weekend=oe)
			if crt:
				messages.success(request,'Visiting Hours Added Successfully')
		return render(request,'add_visiting_hour.html',{})
	else:
		return render(request,'doctor_login.html',{})
def view_visiting_hours(request):
	if request.session.has_key('username'):
		hospital_id = request.session['doc_id']
		visiting_hours = Visiting_Detail.objects.filter(hospital_id=hospital_id)
		return render(request,'view_visiting_hours.html',{'visiting_hours':visiting_hours})
	else:
		return render(request,'doctor_login.html',{})
def edit_visiting(request,pk):
	if request.session.has_key('username'):
		Visiting = Visiting_Detail.objects.filter(id=pk)
		if request.method == 'POST':
			vh = request.POST.get('vweekday')
			vw = request.POST.get('vweekend')
			ow = request.POST.get('onweekday')
			oe = request.POST.get('onweekend')
			crt = Visiting_Detail.objects.filter(id=pk).update(visiting_hour_weekdays=vh,visiting_hour_weekend=vw,
			visiting_hour_online_weekdays=ow,visiting_hour_online_weekend=oe)
			if crt:
				messages.success(request,'Visiting Hours Updated Successfully')
		return render(request,'edit_visiting.html',{'Visiting':Visiting})
	else:
		return render(request,'doctor_login.html',{})
def delete_visiting(request,pk):
	if request.session.has_key('username'):
		Visiting = Visiting_Detail.objects.filter(id=pk).delete()
		return redirect('view_visiting_hours')
	else:
		return render(request,'doctor_login.html',{})
def appointment(request):
	hospital_id = request.session['doc_id']
	v_hr = Appointment.objects.filter(hospital_id=int(hospital_id))
	return render(request,'appointment.html',{'v_hr':v_hr})
def customer_dashboard(request):
	today = datetime.datetime.now()
	a = today.day
	b = today.year
	c = today.month
	detail = Disease_Detail.objects.filter(date=datetime.date(b, c, a))
	return render(request,'customer_dashboard.html',{'detail':detail})
def search_doctor(request):
	if request.GET.get('search'):
		a = request.GET.get('search')
		doctor_details = Doctor_Register.objects.filter(city=a) 
		visting_hour = Visiting_Detail.objects.filter(hospital_id__in=Doctor_Register.objects.filter(city=a))
		return render(request,'search_doctor.html',{'doctor_details':doctor_details,'a':visting_hour})
	else:
		return render(request,'search_doctor.html',{})
def logout(request):
    try:
        del request.session['username']
    except:
     pass
    return render(request, 'doctor_login.html', {})
def customer_logout(request):
    try:
        del request.session['customer']
    except:
     pass
    return render(request, 'customer_login.html', {})

def appoint(request):
	if request.GET.get('id'):
		ids = request.GET.get('id')
		cus_id = request.session['cus_id']
		cid = Customer_Detail.objects.get(id=int(cus_id))
		host_id = Doctor_Register.objects.get(id=int(ids))
		if request.method == 'POST':
			a = request.POST.get('pname')
			b = request.POST.get('proble')
			c = request.POST.get('vdate')
			d = request.POST.get('vtime')
			ins =  Appointment.objects.create(hospital_id=host_id,customer_id=cid,pet_name=a,problem=b,
			visiting_date=c,visiting_time=d,status='')
			if ins:
				messages.success(request,'Appointment Booked')
		return render(request, 'appoint.html', {})
	else:
		return render(request,'search_doctor',{})
def customer_appointments(request):
	if request.session.has_key('customer'):
		cus_id = request.session['cus_id']
		appointment = Appointment.objects.filter(customer_id=cus_id)
		return render(request,'customer_appointments.html',{'appointment':appointment})
	else:
		return render(request,'customer_login.html',{})

def update_status(request,pk):
	upd = Appointment.objects.filter(id=pk).update(status='book')
	return redirect('appointment')
def cancel_app(request,pk):
	upd = Appointment.objects.filter(id=pk).update(status='cancel')
	return redirect('appointment')
def customer_appointments(request):
	if request.session.has_key('customer'):
		cus_id = request.session['cus_id']
		appointment = Appointment.objects.filter(customer_id=cus_id)
		return render(request,'customer_appointments.html',{'appointment':appointment})
	else:
		return render(request,'customer_login.html',{})
def search_patient(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Patient_Detail.objects.all()
		if request.method == 'GET':
			ids = request.GET.get('search')
			row = Patient_Detail.objects.filter(patient_id=ids)
		return render(request,'search_patient.html',{'detail':detail,'row':row})
	else:
		return render(request,'doctor_login.html',{})
def add_patient(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		pat_id = Customer_Detail.objects.all()
		if request.method == 'POST':
			patient_name = request.POST.get('patient_name')
			user_id = Customer_Detail.objects.get(id=int(patient_name))
			mobile = request.POST.get('mobile')
			address = request.POST.get('address')
			image = request.FILES['img']
			crt = Patient_Detail.objects.create(patient_name=user_id,mobile=mobile,address=address,image=image)
			if crt:
				messages.success(request,'Patient Detail Added Successfully')
		return render(request,'add_patient.html',{'pat_id':pat_id})
	else:
		return render(request,'doctor_login.html',{})
def add_report(request,pk,pid):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		pat_id = Doctor_Register.objects.get(id=int(doc_id))
		patient_id=Customer_Detail.objects.get(id=pk)
		p_id=Patient_Detail.objects.get(id=pid)
		if request.method == 'POST':
			disease_name = request.POST.get('disease_name')
			problem = request.POST.get('problem')
			visiting_date = request.POST.get('visiting_date')
			follow_up_date = request.POST.get('follow_up_date')
			report = request.FILES['report']
			prescription = request.FILES['prescription']
			crt = Report_Detail.objects.create(problem=problem,disease_name=disease_name,visiting_date=visiting_date,
			follow_up_date=follow_up_date,report=report,prescription=prescription,Pid=p_id,patient_id=patient_id,doctor_id=pat_id)
			if crt:
				messages.success(request,'Patient Report Detail Added Successfully')
		return render(request,'add_report.html',{})
	else:
		return render(request,'doctor_login.html',{})
def view_report(request,pk):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Report_Detail.objects.filter(Pid=pk)
		if request.method == 'GET':
			ids = request.GET.get('search')
			row = Report_Detail.objects.filter(visiting_date=ids)
		return render(request,'view_report.html',{'detail':detail,'row':row})
	else:
		return render(request,'doctor_login.html',{})
def patient_report(request):
	if request.session.has_key('customer'):
		doc_id = request.session['cus_id']
		detail = Report_Detail.objects.filter(patient_id=int(doc_id))
		if request.method == 'GET':
			ids = request.GET.get('search')
			row = Report_Detail.objects.filter(visiting_date=ids)
		return render(request,'patient_report.html',{'detail':detail,'row':row})
	else:
		return render(request,'customer_login.html',{})
def chart(request):
	detail = Disease_Category.objects.all()
	return render(request,'chart.html',{'detail':detail})
def ajax_disease_spread(request):
    exam_id = request.POST.get('cat_id')
    cursor = connection.cursor()
    sql= ''' SELECT app_disease_spread.area,app_disease_spread.count from app_disease_category  INNER JOIN app_disease_spread ON 
    app_disease_category.id=app_disease_spread.disease_name_id where app_disease_category.id='%d' ''' % (int(exam_id))
    res = cursor.execute(sql)
    detail = cursor.fetchall()
    data = {
    'row':detail
    }
    return JsonResponse(data)
def disease_count(request):
	detail = Disease_Category.objects.all()
	if request.method == 'POST':
		ids = request.POST.get('search')
		row = Disease_Spread.objects.filter(disease_name=int(ids))
		return render(request,'disease_count.html',{'row':row,'detail':detail})
	return render(request,'disease_count.html',{'detail':detail})
def add_disease(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Disease_Category.objects.all()
		if request.method == 'POST':
			ids = Doctor_Register.objects.get(id=int(doc_id))
			disease_name = request.POST.get('disease_name')
			dname = Disease_Category.objects.get(id=int(disease_name))
			area = request.POST.get('area')
			hospital_name = request.POST.get('hospital_name')
			state = request.POST.get('state')
			count = request.POST.get('count')
			cured_count = request.POST.get('cured_count')
			current_count = request.POST.get('current_count')
			crt = Disease_Update.objects.create(disease_name=dname,hospital_name=hospital_name,area=area,state=state,
			count=count,current_count=current_count,cured_count=cured_count,doctor_id=ids)
			if crt:
				messages.success(request,'Added Successfully')
		return render(request,'add_disease.html',{'detail':detail})
	else:
		return render(request,'doctor_login.html',{})		
def disease(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Disease_Update.objects.filter(doctor_id=int(doc_id))
		return render(request,'disease.html',{'detail':detail})
	else:
		return render(request,'doctor_login.html',{})
def update_disease(request,pk):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Disease_Update.objects.filter(id=pk)
		if request.method == 'POST':
			disease_name = request.POST.get('disease_name')
			area = request.POST.get('area')
			hospital_name = request.POST.get('hospital_name')
			state = request.POST.get('state')
			count = request.POST.get('count')
			cured_count = request.POST.get('cured_count')
			current_count = request.POST.get('current_count')
			crt = Disease_Update.objects.filter(id=pk).update(hospital_name=hospital_name,area=area,state=state,
			count=count,current_count=current_count,cured_count=cured_count)
			if crt:
				messages.success(request,'Updated Successfully')
		return render(request,'update_disease.html',{'detail':detail})
	else:
		return render(request,'doctor_login.html',{})			
def delete_disease(request,pk):
	if request.session.has_key('username'):
		Visiting = Disease_Update.objects.filter(id=pk).delete()
		return redirect('disease')
	else:
		return render(request,'doctor_login.html',{})	
def admin_disease(request):
	detail = Disease_Update.objects.all()
	return render(request,'admin_disease.html',{'detail':detail})
def hospital_search(request):
	cursor = connection.cursor()
	tt = ''' SELECT app_disease_update.hospital_name from app_disease_update GROUP BY app_disease_update.hospital_name'''
	post = cursor.execute(tt)
	row = cursor.fetchall()
	if request.method == 'POST':
		exam_id = request.POST.get('cat_id')
		sql= ''' SELECT c.name,d.hospital_name,d.state,d.area,d.count,d.cured_count,d.current_count from 
		app_disease_update as d INNER JOIN app_disease_category as c ON d.disease_name_id=c.id where d.hospital_name='%s' ''' % (exam_id)
		res = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'hospital_search.html',{'detail':detail,'row':row})
	return render(request,'hospital_search.html',{'row':row})
def area_disease(request):
	cursor = connection.cursor()
	tt = ''' SELECT app_disease_update.area from app_disease_update GROUP BY app_disease_update.area'''
	post = cursor.execute(tt)
	row = cursor.fetchall()
	ids = Disease_Category.objects.all()
	if request.method == 'POST':
		exam_id = request.POST.get('cat_id')
		disease = request.POST.get('disease')
		sql= ''' SELECT c.name,d.hospital_name,d.state,d.area,Sum(d.count),Sum(d.cured_count),Sum(d.current_count) from 
		app_disease_update as d INNER JOIN app_disease_category as c ON d.disease_name_id=c.id where d.area='%s' AND c.id='%d' 
		GROUP BY c.id''' % (exam_id,int(disease))
		res = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'area_disease.html',{'detail':detail,'row':row,'ids':ids})
	return render(request,'area_disease.html',{'row':row,'ids':ids})
def new_disease(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		if request.method == 'POST':
			ids = Doctor_Register.objects.get(id=int(doc_id))
			disease_name = request.POST.get('disease_name')
			problem = request.POST.get('problem')
			symtoms = request.POST.get('symtoms')
			precautions = request.POST.get('precautions')
			crt = Unauthorised_Disease.objects.create(disease_name=disease_name,problem=problem,symtoms=symtoms,precautions=precautions,doctor_id=ids)
			if crt:
				messages.success(request,'Added Successfully')
		return render(request,'new_disease.html',{})
	else:
		return render(request,'doctor_login.html',{})	
def new(request):
	if request.session.has_key('username'):
		doc_id = request.session['doc_id']
		detail = Unauthorised_Disease.objects.filter(doctor_id=int(doc_id))
		return render(request,'new.html',{'detail':detail})
	else:
		return render(request,'doctor_login.html',{})	
def admin_new(request):
	detail = Unauthorised_Disease.objects.all()
	return render(request,'admin_new.html',{'detail':detail})
def search_state(request):
	cursor = connection.cursor()
	tt = ''' SELECT app_disease_update.state from app_disease_update GROUP BY app_disease_update.state'''
	post = cursor.execute(tt)
	row = cursor.fetchall()
	if request.method == 'POST':
		exam_id = request.POST.get('cat_id')
		sql= ''' SELECT c.name,d.hospital_name,d.state,d.area,Sum(d.count),Sum(d.cured_count),Sum(d.current_count) from 
		app_disease_update as d INNER JOIN app_disease_category as c ON d.disease_name_id=c.id where d.state='%s' GROUP BY c.name''' % (exam_id)
		res = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'search_state.html',{'detail':detail,'row':row})
	return render(request,'search_state.html',{'row':row})