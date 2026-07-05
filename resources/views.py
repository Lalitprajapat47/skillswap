from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Resource


@login_required
def resource_list(request):
    query = request.GET.get('q', '').strip()

    resources = Resource.objects.select_related('uploaded_by')

    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(skill_tag__icontains=query)
        )

    return render(request, 'resources.html', {
        'resources': resources,
        'query': query,
    })


@login_required
def upload_resource(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        skill_tag = request.POST.get('skill_tag', '').strip()
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        file = request.FILES.get('file')

        if title and skill_tag and (file or link):
            Resource.objects.create(
                title=title,
                skill_tag=skill_tag,
                description=description,
                link=link,
                file=file,
                uploaded_by=request.user,
            )

    return redirect('resource_list')


@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, uploaded_by=request.user)
    resource.delete()
    return redirect('resource_list')