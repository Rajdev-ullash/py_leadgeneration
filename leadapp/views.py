from multiprocessing import context
from django.shortcuts import redirect, render
from .forms import LeadsForm
from .models import Leads
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.

def index(request):
    # if request.method == 'POST':
    #     form = LeadsForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/')
    # else:
    #     form = LeadsForm()

    leads = Leads.objects.all()
    paginator = Paginator(leads, 4) # Show 4 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'page_obj':page_obj
    }
    
    return render(request, 'index.html',context)

def leads_create(request):
    if request.method == 'POST':
        form = LeadsForm(request.POST)

    else:
        form = LeadsForm()

    return save_leads_form(request, form, 'leads_create.html')

def save_leads_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            data['form_is_valid'] = True

            leads = Leads.objects.all().order_by('-id')
            paginator = Paginator(leads, 4) # Show 4 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            data['html_book_list'] = render_to_string('leads_list.html',{'page_obj':page_obj})
        else:
            data['form_is_valid'] = False
    context={'form':form}

    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)


