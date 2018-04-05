from .models import *
from django.shortcuts import render

def crisis(request):
	return{
		'showCrisisList': list(CMOPlanReport.objects.all())
    }

def status(request):
	querylist1 = []
	caseIds = CMOPlanReport.objects.values_list('caseID')
	for i in range(len(caseIds)):
		qs1=statusReport.objects.filter(caseID_id=caseIds[i]).last()
		if qs1:
			querylist1.append(qs1)
	return{
		'filterStatus': querylist1
    }

