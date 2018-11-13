from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Image, Comments
from .forms import UpdateProfile, PostImageForm, CommentForm
from django.http import HttpResponseRedirect


@login_required(login_url='/accounts/login/')
def index(request):
    pics = Image.get_all()
    return render(request, 'index.html', {'pics': pics})


@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    profiles = Profile.get_user(user.id)
    pics = Image.get_by_user(user.id)
    if profiles:
        profile = profiles[len(profiles)-1]
    else:
        profile = profiles

    if request.method == 'POST':
        profile_form = UpdateProfile(request.POST, request.FILES)
        upload_form = PostImageForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)
        if profile_form.is_valid():
            if Profile.get_user(user.id):
                deleter = Profile.get_user(user.id)
                deleter.delete()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save_profile()
            return HttpResponseRedirect('/profile')
        if upload_form.is_valid():
            image = upload_form.save(commit=False)
            image.user = user
            image.save_image()
    else:
        profile_form = UpdateProfile()
        upload_form = PostImageForm()
        comment_form = CommentForm
    return render(request, 'registration/profile.html', {'user': user, 'profile': profile, 'pics': pics, 'profile_form': profile_form,
                                            'upload_form': upload_form, 'coment_form': comment_form})


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        search_pics = Image.search_image(search_term)
        search_prof = Profile.search_profiles(search_term)
        message = f'{search_term}'

        return render(request, 'search.html', {'message': message, 'pics': search_pics, 'profiles': search_prof})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {'message': message})

@login_required(login_url='/accounts/login/')
def single_pic(request, img):
    user = request.user
    picture = Image.get_img_by_id(img)
    comments = Comments.get_by_image(img)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.image = picture
            comment.save()
            return redirect('picture', picture.id)
    else:
        comment_form = CommentForm()

    return render(request, 'picture.html', {'comment_form': comment_form, 'pic': picture, 'user': user, 'comments': comments})
