import datetime
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from debts.forms import NewUserForm, PaymentForm
from .models import Money

def main(request):
    model = Money
    field_names = [f.name for f in model._meta.get_fields()]
    field_names.remove('id')
    data = [[getattr(ins, name) for name in field_names]
            for ins in model.objects.prefetch_related().all()]
    return render(request, 'main.html', {'field_names': field_names, 'data': data})

def register_request(request):
	form = NewUserForm()
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("account/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	message = messages.get_messages(request)
	return render(request=request, template_name="registration/register.html", context={"form":form, "messages": message})

@login_required
def accountView(request):
	form = PaymentForm()
	model = Money

	if request.method == "POST":
		form = PaymentForm(request.POST)
		if form.is_valid():
			payment = form.save(commit=False)
			payment.payer = request.user.username
			payment.date = datetime.datetime.now()
			payment.save()
			messages.success(request, "Success!")
			return redirect("/")
	
    #find amount of money owed, received and net
	i = 0
	got = 0
	owed = 0
	payers = []
	payees = []
	[payers.append(payer[0]) for payer in model.objects.values_list('payer')]
	[payees.append(payee[0]) for payee in model.objects.values_list('payee')]
	for payer, payee in list(zip(payers, payees)):
		if payer == request.user.username:
			owed += model.objects.values_list('sum')[i][0]
		if payee == request.user.username:
			got += model.objects.values_list('sum')[i][0]
		i += 1
	net = got - owed
	
	return render(request, "account.html", {"got": got, "owed": owed, "net": net, "form": form})