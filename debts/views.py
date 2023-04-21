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
    print(field_names)
    data = [[getattr(ins, name) for name in field_names]
            for ins in model.objects.prefetch_related().all()]
    return render(request, 'main.html', {'field_names': field_names, 'data': data})

def register_request(request):
	if request.method == "post":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register.html", context={"form":form})

@login_required
def accountView(request):
	if request.method == "post":
		while True:
			form = PaymentForm(request.POST)
			users = get_user_model().objects.values_list('username')
			if form.payee not in users:
				messages.error(request, "Please enter a valid username (it's case sensitive!)")
				continue
			break
	
	form = PaymentForm()
	model = Money
	
    #find amount of money owed, received and net
	i = 0
	got = 0
	owed = 0
	for payer, payee in list(zip(model.objects.values_list('payer'))):
		if payer == request.user.username:
			owed += model.objects.values_list('sum')[i]
		if payee == request.user.username:
			got += model.objects.values_list('sum')[i]
		i += 1
	net = got - owed
	
