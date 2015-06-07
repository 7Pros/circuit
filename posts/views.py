from django.shortcuts import redirect

from posts.models import Post, Hashtag
import re

def PostCreateView(request):
    if (len(request.POST['content']) <= 256):
        parsedString = ParseContent(request.POST['content'])
        post = Post(content=request.POST['content'], author=request.user)
        post.save()
        SaveHashtags(parsedString['hashtags'], post)
    return redirect(request.META['HTTP_REFERER'] or 'landingpage')


def ParseContent(content):
    hashtags = re.findall(r"#(\w+)", content)
    mentions = re.findall(r"@(\w+)", content)
    return {'hashtags': hashtags, 'mentions': mentions}

def SaveHashtags(hashtags, post):
    for hashtagWord in hashtags:
        hashtagList = Hashtag.objects.filter(name=hashtagWord)

        if len(hashtagList) == 0:
            hashtag = Hashtag(name=hashtagWord.lower())
            hashtag.save()
            hashtag.posts.add(post)
        else:
             hashtagList[0].posts.add(post)