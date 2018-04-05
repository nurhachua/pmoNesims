from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from pmoApp.serializers import JustificationReportSerializer, AuthorizationReportSerializer
from .models import *
from rest_framework import viewsets
from pmoSystem import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db.models.query import QuerySet
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from random import randint
import pyrebase


config = {
    'apiKey': "AIzaSyB6Krmsq2qeDj2G7rNJZkFsiGZmYytDQnM",
    'authDomain': "pmonesims.firebaseapp.com",
    'databaseURL': "https://pmonesims.firebaseio.com",
    'projectId': "pmonesims",
    'storageBucket': "pmonesims.appspot.com",
    'messagingSenderId': "1024527895183"
  }
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()

class JustificationReportViewSet(viewsets.ModelViewSet):
	queryset = justificationReport.objects.all()
	serializer_class = JustificationReportSerializer
	http_method_names = ['get','head','post','options']

class AuthorizationReportViewSet(viewsets.ModelViewSet):
	queryset = authorizationReport.objects.all()
	serializer_class = AuthorizationReportSerializer
	http_method_names = ['get','head','post','options']


def otp(request):
    if request.session.has_key('email'):
        email1 = request.session['email']
        passw = request.session['passw']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')

    else:
        email1 = request.POST.get('email')
        passw = request.POST.get('pass')
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
        try:
            user1 = authe.sign_in_with_email_and_password(email1, passw)
        except:
            message = "Invalid Credentials"
            return render(request, "login.html", {"messg": message})

        request.session['email'] = email1
        request.session['passw'] = passw
        subject = 'OTP'
        from_email = settings.EMAIL_HOST_USER
        to_email = request.session['email']
        OTP = randint(10000000, 99999999)
        request.session['OTP'] = OTP
        send_mail(subject, str(OTP), from_email, [to_email], fail_silently=False)
        print(str(OTP))

    return render(request, 'otp.html', {'minName': ministerName, 'email': email1, 'passw': passw})


def resendOTP(request):
    if request.method in ('POST'):
        del request.session['OTP']
        subject = 'OTP'
        from_email = settings.EMAIL_HOST_USER
        to_email = request.session['email']
        OTP = request.session['OTP'] = randint(10000000, 99999999)
        send_mail(subject, str(OTP), from_email, [to_email], fail_silently=False)
        print(str(OTP))
    return render(request, 'otp.html', {})


def otpAuthentication(request):
    if request.POST:
        otp = request.POST['otp']
        if (otp == str(request.session['OTP'])):
            return render(request, 'home.html')
    return HttpResponse('', status=401)


def home(request):
    if request.session.has_key('email'):
        email1 = request.session['email']
        passw=request.session['passw']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
    return render(request, 'home.html', {'MinName':ministerName, 'email':email1,'passw':passw})

def login(request):
    return render(request, 'login.html', {})

def logout(request):
    try :
        del request.session['email']
        del request.session['passw']
    except:
        pass
    return render(request, 'login.html', {})

def liveUpdate(request):
    #print("Minister Name = "+request.session())
    #if request.session.get('ministerName'):
    #if request.session.has_key('ministerName'):
    if request.session.has_key('email'):
        email1 = request.session['email']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
    return render(request,'liveUpdate.html',{'MinName':ministerName})

def currentCrisis(request):
    if request.session.has_key('email'):
        email1 = request.session['email']
        passw=request.session['passw']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
    caseIds = list(CMOPlanReport.objects.values_list('caseID')) #this is a tuple
    caseIdsNoDup=list(sorted(list(set(caseIds)))) #since each crisis can have multiple plans, crisis records will have duplicate. this is to remove
    crisisList=list(CMOPlanReport.objects.all()) #to store all crisis into a list
    querylist1=[] #list to store latest status report for each crisis (for crisis status)
    querylist2=[]#list to store planEvaluation obj (for auth status)
    querylist3=[] #list to store CMOPlanReport with no duplicates (for emergency level, case id, case name, datetime reported)
    latestPlan=[] #to store the list of the latest plans for each crisis
    crisisList2=[] #to store crises of same case id (duplicates)
    crisisList3=[] #to store one crisis record for each of the caseid

    for i in range(len(caseIdsNoDup)):
        for j in range(len(caseIds)):
            if(caseIds[j]==caseIdsNoDup[i]):
                crisisList2.append(crisisList[j])
                #take out last record in trylist2 and append it into try3 to remove the duplicates for each crisis (one crisis can have many plans but crisis details is the same, so get the latest one to get the latest plan)
        crisisAppend=crisisList2[-1]
        querylist3.append(crisisAppend) #contains the crisis with no duplicates (by picking out the latest plan)
        latestPlan.append(crisisAppend.planID)
    for m in range(len(caseIdsNoDup)):
        qs1=statusReport.objects.filter(caseID_id=caseIdsNoDup[m]).last()
        if qs1:
            querylist1.append(qs1)
    for n in range(len(latestPlan)):
        qs2=Plan_Evaluation.objects.filter(planID=latestPlan[n], user_type_id="pm").last()
        if qs2:
            querylist2.append(qs2)
    return render(request,'currentCrisis.html', {'statusRep':querylist1, 'planEval':querylist2, 'cCrisis':querylist3, 'MinName':ministerName,'email':email1,'passw':passw})
	

def historicalCrisis(request):
    if request.session.has_key('email'):
        email1 = request.session['email']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
    caseIds = CMOPlanReport.objects.values_list('caseID')
    caseIdsNoDup=list(sorted(list(set(caseIds))))
    crisisList2=[] #to store crises of same case id (duplicates)
    querylist3=[]
    crisisList=list(CMOPlanReport.objects.all()) #to store all crisis into a list
	
    for i in range(len(caseIdsNoDup)):
        for j in range(len(caseIds)):
            if(caseIds[j]==caseIdsNoDup[i]):
                crisisList2.append(crisisList[j])
        crisisAppend = crisisList2[-1]
        querylist3.append(crisisAppend)  # to store CMOreports
        #take out last record in trylist2 and append it into trylist3
    statusRep=[]#list to store all status reports
	
    for i in range(len(caseIdsNoDup)):
        qs1=statusReport.objects.filter(caseID_id=caseIdsNoDup[i]).last()
        if qs1:
            statusRep.append(qs1)

    return render(request,'historicalCrisis.html', {'hCrisis':querylist3, 'statusRep':statusRep,'MinName':ministerName})
	

def broadcast(request):
    if request.session.has_key('email'):
        email1 = request.session['email']
        username2 = User.objects.filter(email=email1)
        username3 = username2[0].username
        ministerName = Account.objects.filter(username=username3).values('minister_name')
    return render(request,'broadcast.html',{'MinName':ministerName})

def crisis(request):
    if request.method=='GET':
        caseID = request.GET.get('caseID')
        if not caseID:
            return render(request, 'currentCrisis.html')
        else:
            if request.session.has_key('email'):
                email1 = request.session['email']
                passw = request.session['passw']
                username2 = User.objects.filter(email=email1)
                username3 = username2[0].username
                ministerName = Account.objects.filter(username=username3).values('minister_name')
                decisionTable = Account.objects.filter(username=username3).values('decisionTable')
                currentUserType = Account.objects.filter(username=username3).values('user_type')
                ut=Account.objects.get(username=username3)
                allUserTypes=Account.objects.all()
                planEval = Plan_Evaluation.objects.all()

                querylist3 = []
                querylist4 = []
                tempList = []

                querylist6= []


                crisis = CMOPlanReport.objects.get(caseID=caseID)
                #status1= statusReport.objects.get(caseID=caseID)
                status = statusReport.objects.all()
                index = 0
                for case in status:

                    if str(case.caseID_id) == str(caseID):

                        tempList.append(status[index])
                        print(case.statRepID)

                        index += 1

                    else:
                        # print("wrong case ID")
                        index += 1
                        print(index)


                y = CMOPlanReport.objects.get(planID=crisis.caseID)
                # print(request.POST.get("inputPlanID"))

                # print(request.POST.get("txtUType"))


                peList = Plan_Evaluation.objects.all()
                flagApp=False
                for pe in peList:

                    if (str(pe.planID_id) == str(crisis.planID) and str(pe.user_type_id) == ut.user_type) and str(pe.authorizationStatus)!="Pending":  # first if
                        print("PE Plan ID :" + str(pe.planID_id) + "PE User Type :" + str(pe.user_type_id))
                        flagApp=True
                        # javascript alert at crisis.html saying user has already approved/rejected the plan

                if crisis:
                    querylist3.append(crisis)
                if status:
                    querylist6.append(tempList[-1])


        # now you have the value of sku
        # so you can continue with the rest
            return render(request, 'crisis.html',{'statusFull':tempList,'statusEval': querylist6,'cCrisis':querylist3,'planEval':planEval,'MinName':ministerName,'decisionTable':decisionTable,'currentUserType':currentUserType,'allUserTypes':allUserTypes,'email':email1,'passw':passw,'flag':flagApp})
    else:
        if request.session.has_key('email'):
            email1 = request.session['email']
            passw = request.session['passw']
            username2 = User.objects.filter(email=email1)
            username3 = username2[0].username
            z=request.POST.get("inputPlanID")
            y=CMOPlanReport.objects.get(planID=z)
           # print(request.POST.get("inputPlanID"))

            #print(request.POST.get("txtUType"))
            a = request.POST.get("txtUType")
            b=Account.objects.get(user_type=a)
            peList=Plan_Evaluation.objects.all()
            plan = Plan_Evaluation()
            plan.planID = y
            plan.user_type = b

            if request.POST.get("approve"):
                if (a == "pm"):
                    plan.authorizationStatus = "Approved"
                    plan.eval_hasComment = "False"
                    plan.eval_comment = " "
                    plan.save()
                    auth = authorizationReport()
                    auth.planID = y
                    auth.save()
                    print("PM Saved")
                    return render(request, "home.html")

                else:
                    plan.authorizationStatus = "Approved"
                    plan.eval_hasComment = "False"
                    plan.eval_comment = " "
                    plan.save()
                    print("HEALTH MINISTER SAVED")
                    return render(request, "home.html")

            elif request.POST.get("reject"):
                plan.authorizationStatus = "Rejected"
                plan.eval_comment = request.POST.get('txtMinComment')
                plan.eval_hasComment = "True"
                plan.save()
                return render(request, "home.html")

                return render(request, "home.html")

def justification(request):
    if request.method=='GET':
        cID = request.GET.get('caseID')
        pID = request.GET.get('planID')
        uty= request.GET.get('utype')
        if not cID and pID and uty:
            return render(request, 'currentCrisis.html')
        else:
            if request.session.has_key('email'):
                email1 = request.session['email']
                passw = request.session['passw']
                username2 = User.objects.filter(email=email1)
                username3 = username2[0].username
                ministerName = Account.objects.filter(username=username3).values('minister_name')
                dt = Account.objects.filter(username=username3).values('decisionTable')
                utype = Account.objects.filter(username=username3).values('user_type')
                querylist3 = []
                querylist4 = []
                print(cID)
                crisis = CMOPlanReport.objects.get(caseID=cID)
                status= statusReport.objects.get(caseID=cID)




                if crisis:
                    querylist3.append(crisis)
                if status:
                    querylist4.append(status)


        # now you have the value of sku
        # so you can continue with the rest
            return render(request, 'justification.html',{'crisisEval':querylist3,'statusEval':querylist4,'MinName':ministerName,'dt1':dt,'ut':utype,'email':email1,'passw':passw})
    else:
        cID = request.GET.get('caseID')
        pID = request.GET.get('planID')
        uty = request.GET.get('utype')
        if request.session.has_key('email'):
            email1 = request.session['email']
            passw = request.session['passw']
            username2 = User.objects.filter(email=email1)
            username3 = username2[0].username
            y=CMOPlanReport.objects.get(planID=pID)

            b=Account.objects.get(user_type=uty)
            plan = Plan_Evaluation()
            plan.planID = y
            plan.user_type = b
            if request.POST.get("sendReject"):
                plan.authorizationStatus = "Rejected"
                plan.eval_comment = "Pm Reject"
                plan.eval_hasComment = "True"
                plan.save()
                just = justificationReport()
                just.planID = y
                just.justification=request.POST.get('inputJustification')
                just.save()


                return render(request, "home.html")
            else:

                return render(request, "historicalCrisis.html")
        else:

            return render(request, "login.html")




def createpost(request):
        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('content'):
                post=Post()
                post.title= request.POST.get('title')
                post.content= request.POST.get('content')
                post.save()
                return render(request, 'createpost.html')  
        else:
                return render(request,'createpost.html')


def updateCrisis(request):
	if request.session.has_key('email'):
		email1 = request.session['email']
		username2 = User.objects.filter(email=email1)
		username3 = username2[0].username
		ministerName = Account.objects.filter(username=username3).values('minister_name')
		
	queryDashboard = CMOPlanReport.objects.all()
	return render(request, 'home.html', {'queryDashboard':queryDashboard})
	# else:
		# return render(request,'home.html')	
			
	