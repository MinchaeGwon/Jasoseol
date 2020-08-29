from django.shortcuts import render, redirect, get_object_or_404
from .forms import JssForm, CommentForm
from .models import Jasoseol, Comment
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
#from django.http import Http404

def home(request):
    all_jss = Jasoseol.objects.all()

    return render(request, 'home.html', {'all_jss':all_jss})

@login_required(login_url='/login/')
def my_index(request):
    my_jss = Jasoseol.objects.filter(author=request.user)
    return render(request, 'home.html', {'all_jss':my_jss})

@login_required(login_url='/login/') #두번째 방법
def create(request):
    #로그인 못하면 글 작성 못하게 함 -> 첫번째 방법
    # if not request.user.is_authenticated:
    #     return redirect('login')

    if request.method == 'POST':
        filled_form = JssForm(request.POST)
        
        if filled_form.is_valid():
            temp_form = filled_form.save(commit=False)
            temp_form.author = request.user
            filled_form.save()
            return redirect('home')

    jss_form = JssForm()
    return render(request, 'create.html', {'jss_form':jss_form})

@login_required(login_url='/login/')
def detail(request, jss_id):
    # try:
    #     my_jss = Jasoseol.objects.get(pk=jss_id)
    # except:
    #     raise Http404

    my_jss = get_object_or_404(Jasoseol, pk=jss_id)
    comment_form = CommentForm();



    return render(request, 'detail.html', {'my_jss':my_jss, 'comment_form':comment_form})

def delete(request, jss_id):
    my_jss = Jasoseol.objects.get(pk=jss_id)
    
    if request.user == my_jss.author:
        my_jss.delete()
        return redirect('home')

    raise PermissionDenied

def update(request, jss_id):
    my_jss = Jasoseol.objects.get(pk=jss_id)
    jss_form = JssForm(instance=my_jss)

    if request.user == my_jss.author:
        if request.method =='POST':
            updated_form = JssForm(request.POST, instance=my_jss)
            if updated_form.is_valid():
                updated_form.save()
                return redirect('home')

    return render(request, 'create.html', {'jss_form':jss_form})

def create_comment(request, jss_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        temp_form = comment_form.save(commit=False)
        temp_form.author = request.user
        temp_form.jasoseol = Jasoseol.objects.get(pk=jss_id)
        temp_form.save()
        return redirect('detail', jss_id)

def delete_comment(request, jss_id, comment_id):
    my_comment = Comment.objects.get(pk=comment_id)

    if request.user == my_comment.author:
        my_comment.delete()
        return redirect('detail', jss_id)
    else:
        raise PermissionDenied
