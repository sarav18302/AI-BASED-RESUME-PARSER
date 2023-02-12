from django.contrib import admin
from .models import Profile, Poll, FollowersCount,SubmitVote

# Register your models here.
admin.site.register(Profile)
admin.site.register(Poll)
# admin.site.register(LikePost)
admin.site.register(SubmitVote)
admin.site.register(FollowersCount)