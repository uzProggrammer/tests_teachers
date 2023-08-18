from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, PostComment
from .forms import PostCommentForm, PostForm, PostCreateForm
from django.utils import timezone
from assignments.models import Assignment, StudentAnswer

def all_posts(request):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    posts = Post.objects.all()
    return render(request, 'posts/posts.html', {'posts': posts, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def post(request, post_id):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
           user =request.user
           body = form.cleaned_data['body']
           PostComment(user=user, body=body, post=post).save()

    return render(request, 'posts/post.html', {'post': post, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)}, )

def update_post(request,post_id):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    post = get_object_or_404(Post, id=post_id)
    if post.author.username != request.user.username:
        return render(request, '404.html')
    else:
        form = PostForm(request.POST or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                form.save(commit=False)
                form.date_updated = timezone.now()
                return HttpResponseRedirect("/posts/post/" + str(post_id))

        return render(request, 'posts/post_update.html', {'post': post, 'form': form, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)}, )

def create_post(request):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    if request.user.is_authenticated:
        form = PostCreateForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                author = request.user
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                Post(author=author, title=title, content=content).save()
            return HttpResponseRedirect("/posts/")
        return render(request, 'posts/post_create.html', {'form': form, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def delete_post(request, post_id):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    if request.user.is_staff:
        post = Post.objects.get(id=post_id)
        if request.method == 'POST':
            post.delete()
            return HttpResponseRedirect('/posts/')
        return render(request, 'posts/post_delete.html', {'post': post, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def add_post_like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(f'/posts/post/{post_id}')
    else:
        return HttpResponseRedirect('users/login/')