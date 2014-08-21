from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from cageInventory.models import *
from django.template import loader, Context
import datetime
import json
import cageInventory.settings


def index(request):
	total = Item.objects.all().count()
	in_count = Item.objects.filter(status = True).count()
	out_count = Item.objects.filter(status = False).count()
	missing = Item.objects.filter(status = None).count()
	transactions = Transaction.objects.all().order_by('-start_date')[:10]
	return render_to_response('cageInventory/index.html',{'total':total,
														'in':in_count,
														'out':out_count,
														'missing':missing,
														'transactions':transactions})


def all_view(request):
	if request.is_ajax():
		t = loader.get_template('cageInventory/all_view_ajax.html')
		c = Context({'items':Item.objects.all()})
		rendered = t.render(c)
		return HttpResponse(json.dumps({'rendered':str(rendered)}))
	return render_to_response('cageInventory/all_view.html',{'items':Item.objects.all()})


def in_view(request):
	if request.is_ajax():
		t = loader.get_template('cageInventory/in_view_ajax.html')
		c = Context({'items':Item.objects.filter(status=True)})
		rendered = t.render(c)
		return HttpResponse(json.dumps({'rendered':str(rendered)}))
	return render_to_response('cageInventory/in_view.html',{'items':Item.objects.filter(status=True)})


def out_view(request):
	if request.is_ajax():
		t = loader.get_template('cageInventory/out_view_ajax.html')
		c = Context({'items':Item.objects.filter(status=False)})
		rendered = t.render(c)
		return HttpResponse(json.dumps({'rendered':str(rendered)}))
	return render_to_response('cageInventory/out_view.html',{'items':Item.objects.filter(status=False)})


def missing_view(request):
	return render_to_response('cageInventory/missing_view.html',{'items':Item.objects.filter(status=None)})


def transactions_view(request):
	if request.is_ajax():
		t = loader.get_template('cageInventory/trans_view_ajax.html')
		c = Context({'items':Transaction.objects.all().order_by('-start_date')})
		rendered = t.render(c)
		return HttpResponse(json.dumps({'rendered':str(rendered)}))
	return render_to_response('cageInventory/trans_view.html',{'items':Transaction.objects.all().order_by('-start_date')})


def transaction_detail(request, item_id):
	return render_to_response('cageInventory/transaction_detail.html',{'item':Transaction.objects.get(id=item_id)})


def item_detail(request, item_id):
	return render_to_response('cageInventory/item_detail.html',{'item':Item.objects.get(id=item_id),
																'trans':Transaction.objects.filter(this_item=Item.objects.get(id=item_id))})


def students(request):
	return render_to_response('cageInventory/students.html',{'items':Student.objects.all()})


def student_detail(request, item_id):
	return render_to_response('cageInventory/student_detail.html',{'item':Student.objects.get(id=item_id),
																'trans':Transaction.objects.filter(student=Student.objects.get(id=item_id))})


def graph_data(request):
	if request.is_ajax():
		curTime = ceil(datetime.datetime.now())
		elementData = []
		for i in range(0,150,15):
			elementData.append({'period':(curTime - datetime.timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M'),
								'out':Transaction.objects.filter(start_date__gte=curTime-datetime.timedelta(minutes=i+15),
																 start_date__lt=curTime-datetime.timedelta(minutes=i)).count(),
								'in':Transaction.objects.filter(end_date__gte=curTime-datetime.timedelta(minutes=i+15),
																 end_date__lt=curTime-datetime.timedelta(minutes=i)).count()})

		return HttpResponse(json.dumps(elementData), mimetype="application/json")
	else:
		return HttpResponseRedirect('/')


def ceil(dt):
    if dt.minute % 15 or dt.second:
        return dt + datetime.timedelta(minutes = 15 - dt.minute % 15,
                                       seconds = -(dt.second % 60))
    else:
        return dt


def check_in_out(request, item_id, uid):
	if request.is_ajax():
		try:
			# Try to select the proper item
			this_item = Item.objects.get(id_num=item_id)
		except:
			# If for whatever reason, the item cannot be found, give a 404
			return HttpResponse(json.dumps({'resp':'bad_item'}))


		if this_item.status == True:
			# If it's currently checked in, we need to check it out
			try:
				# Since we're checking an item out, we need the student
				this_student = Student.objects.get(uid=uid)
			except:
				# If we can't get it for whatever reason, stop the request
				return HttpResponse(json.dumps({'resp':'bad_uid'}))

			# We now have an item and a student, let's make the transaction
			new_trans = Transaction(student=this_student,this_item=this_item,start_date=datetime.datetime.now())
			new_trans.save()

			# Now let's mark the item as being checked out
			this_item.status = False
			this_item.save()

			# One last thing: if the value is above the 'needs signature' level, tell the jQuery to redirect it to that page
			if this_item.model.value > cageInventory.settings.value_threshold:
				return HttpResponse(json.dumps({'resp':'need','item':this_item.id,'trans':new_trans.id}))
			else:
				return HttpResponse(json.dumps({'resp':'good','item':this_item.id,'trans':new_trans.id}))

		else:
			# To avoid errors, we look for all open transactions on the current item
			this_trans = Transaction.objects.filter(this_item=this_item,end_date=None)

			# And we close each of them individually
			for trans in this_trans:
				trans.end_date = datetime.datetime.now()
				trans.save()

			# Now we mark the item as being returned, and save it
			this_item.status = True
			this_item.save()
			return HttpResponse(json.dumps({'resp':'back'}))

	else:
		return HttpResponseRedirect('/')


def needs_signature(request):
	pass


def dashdata(request):
	#if not request.is_ajax():
#		return HttpResponseRedirect('/')
	total = Item.objects.all().count()
	in_count = Item.objects.filter(status = True).count()
	out_count = Item.objects.filter(status = False).count()
	missing = Item.objects.filter(status = None).count()
	transactions = Transaction.objects.all().order_by('-start_date')[:10]
	transList = []
	for trans in transactions:
		if trans.end_date:
			transList.append({'tid':str(trans.id),'student':str(trans.student),'this_item':str(trans.this_item),'start_date':str(trans.start_date.strftime('%Y-%m-%d %H:%M')),'end_date':str(trans.end_date.strftime('%Y-%m-%d %H:%M'))})
		else:
			transList.append({'tid':str(trans.id),'student':str(trans.student),'this_item':str(trans.this_item),'start_date':str(trans.start_date.strftime('%Y-%m-%d %H:%M')),'end_date':'None'})
	return HttpResponse(json.dumps({'totalnum':total,'innum':in_count,'outnum':out_count,'missingnum':missing,'trans':transList}))