from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, ListFollowed, Like


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        context = {
            "username": username,
            "all_posts": Post.objects.all()
        }

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session["user"] = username

            return HttpResponseRedirect(reverse("index"), context)
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def post(request):

    # Order messages reverse chronologically, add page numbers
    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)

    # If the user sends a message via post through the textbox, save the entry in the "Post" table
    if request.method == "POST":

        new_entry = request.POST["user_post"]
        new_post = Post.objects.create(username=User.objects.get(username=request.session["user"]), post=new_entry)
        context = {
            "logged_user": request.session["user"],
            "all_posts": all_posts,
        }
        return render(request, "network/main.html", context)

    else:

        context = {
            "logged_user": request.session["user"],
            "all_posts": all_posts,
        }

        return render(request, "network/main.html", context)

@csrf_exempt
def edit(request, post_id):
    # Query for the requested post
    try:
        post = Post.objects.get(username__username=request.session["user"], pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "POST":
        data = json.loads(request.body)
        edited_content = data.get("post")
        Post.objects.update_or_create(username__username=request.session["user"], pk=post_id,
                                      defaults={
                                          "post": edited_content
                                      })
        return JsonResponse({"message": "Post updated successfully"}, status=201)

@csrf_exempt
def profile(request, username):
    # query implementation to get a user's "following" list
    a = ListFollowed.objects.filter(user__username=request.session["user"])

    if not a:
        list_following = []
    else:
        container = []
        for item in a:
            b = item.people_followed.username
            container.append(b)
            list_following = container
    total_posts = Post.objects.filter(username__username=username).order_by("-timestamp")
    paginator = Paginator(total_posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    request.session["profile"] = username
    context = {
        "logged_user": request.session["user"],
        "profile_name": username,
        "num_followers": User.objects.get(username=username).num_followers,
        "num_following": User.objects.get(username=username).num_following,
        "list_following": list_following,
        "posts": posts
    }
    return render(request, "network/profile.html", context)

@csrf_exempt
def change_followers(request):

    # From follow.js, query database to get list of ppl the signed in user follows. Return list & # of user's followers.
    if request.method == "GET":
        a = ListFollowed.objects.filter(user__username=request.session["user"])
        b = list(a)
        num_of_followers = User.objects.get(username=request.session["profile"]).num_followers
        if not a:
            list_following = []
        else:
            container = []
            for item in b:
                c = item.people_followed.username
                container.append(c)
                # return container
            list_following = container
        return JsonResponse({"list_following": str(list_following), "num_of_followers": str(num_of_followers)})

    # From follow.js, query database via post to change the number of selected users' "followers"
    elif request.method == "POST":
        data = json.loads(request.body)
        profile_name = data["profile_name"]
        num_fol_change = data["num_fol_change"]

        if num_fol_change == 1:

            # add 1 to count of ppl being followed
            user = User.objects.get(username=request.session["user"])
            user.num_following += num_fol_change
            user.save()

            # add 1 to the selected profiles' num of followers
            profile_user = User.objects.get(username=profile_name)
            profile_user.num_followers += num_fol_change
            profile_user.save()

            # add the clicked user to the list of people being followed

            ListFollowed.objects.create(user=User.objects.get(username=request.session["user"]),
                                        people_followed=User.objects.get(username=profile_name))

        else:

            # Subtract 1 from the selected profiles' num of followers
            profile_user = User.objects.get(username=profile_name)
            profile_user.num_followers += num_fol_change
            profile_user.save()

            # delete 1 from count of ppl being followed
            user = User.objects.get(username=request.session["user"])
            if user.num_following != 0:
                user.num_following += -1
                user.save()

                ListFollowed.objects.filter(user__username=request.session["user"],
                                            people_followed__username=profile_name).delete()

            else:
                pass

        return JsonResponse({"message": "This works"}, status=201)

    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)

@csrf_exempt
def following(request):
    # Query database to get list of ppl, signed in user follows & their posts. Pass to template via context, "posts"
    if request.user.is_authenticated:
        # object list of users followed by the current user
        cur_user_foll = ListFollowed.objects.filter(user__username=request.session["user"])
        users_followed = []
        for user in cur_user_foll:
            x = user.people_followed
            users_followed.append(x)

        test_list = []
        if users_followed:
            for name in users_followed:
                try:
                    total_posts = Post.objects.filter(username__username=name).order_by("-timestamp")
                    for item in total_posts:
                        test_list.append(item)
                    paginator = Paginator(test_list, 10)
                    page = request.GET.get('page')
                    posts = paginator.get_page(page)
                except:
                    return HttpResponse("There was an error. Sorry")
        else:
            messages.info(request, "There are no users currently being followed")
            return render(request, "network/following.html")

        context = {
            "users_followed": users_followed,
            "posts": posts
        }
        return render(request, "network/following.html", context)
    else:
        return HttpResponse("User not Logged in. Login required")

@csrf_exempt
def likes(request, post_id):
    # From edit.js, query database to update the like count of a user on clicking the like button.
    # Send the new "True" or "False" value and the like count number via Jsonresponse
    if request.method == "POST":
        data = json.loads(request.body)
        # post_id = data["post_id"]
        status = data["status"]

        a = Like.objects.update_or_create(user=User.objects.get(username=request.session["user"]),
                                          liked_posts=Post.objects.get(pk=post_id),
                                          defaults={
                                              "like_unlike": status
                                          })
        note = Post.objects.get(pk=post_id)

        # From edit.js, On clicking the like button send a change "True" or "False" to server.
        # On server info receipt, Change the boolean status of the Like Field by adding or subtracting, if True or False
        if status is True:
            note.like_count += 1
            note.save()
        else:
            note.like_count += -1
            note.save()
        count_num = Post.objects.get(pk=post_id).like_count

        b = Like.objects.filter(user__username=request.session["user"], liked_posts__id=post_id)
        boolean_value = b[0].like_unlike

    if request.method == "GET":
        b = Like.objects.filter(user__username=request.session["user"], liked_posts__id=post_id)
        if not b:
            Like.objects.create(user=User.objects.get(username=request.session["user"]),
                                liked_posts=Post.objects.get(pk=post_id), like_unlike=False)
            boolean_value = False
        else:
            boolean_value = b[0].like_unlike
        count_num = Post.objects.get(pk=post_id).like_count

    return JsonResponse({"data": boolean_value, "count": count_num})
