from django.shortcuts import render, redirect
from collection.models import Thing
from collection.forms import ThingForm
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
	things = Thing.objects.all()
	return render(request, 'index.html', {'things': things})

# def index(request):
# 	number = 6
# 	thing = "Thing name"
# 	return render(request, 'index.html', {'number': number, 'thing': thing,})

def thing_detail(request,slug):
	thing = Thing.objects.get(slug=slug)
	return render(request, 'things/thing_detail.html', {'thing': thing},)

def edit_thing(request, slug):
	thing = Thing.objects.get(slug=slug)
	# make sure the logged in user is the owner of the thing
	if thing.user != request.user:
		raise Http404

	form_class = ThingForm

	if request.method == 'POST':
		form = form_class(data=request.POST, instance=thing)
		if form.is_valid():
			form.save()
			return redirect('thing_detail', slug=thing.slug)
	else:
		form = form_class(instance=thing)

	return render(request, 'things/edit_thing.html', {'thing': thing, 'form': form,})

def create_thing(request):
    form_class = ThingForm

    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and
        # apply to the form
        form = form_class(request.POST)
        if form.is_valid():
            # create an instance but don't save yet
            thing = form.save(commit=False)

            # set the additional details
            thing.user = request.user
            thing.slug = slugify(thing.name)

            # save the object
            thing.save()

            # redirect to our newly created thing
            return redirect('thing_detail', slug=thing.slug)

    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'things/create_thing.html', {
        'form': form,
    })

def browse_by_name(request, initial=None):
    if initial:
        things = Thing.objects.filter(name__istartswith=initial)
        things = things.order_by('name')
    else:
        things = Thing.objects.all().order_by('name')

    return render(request, 'search/search.html', {
        'things': things,
        'initial': initial,
    })