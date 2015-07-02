"""
--Brief Description--

@author 7Pros
@copyright 
"""
from rest_framework import renderers, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import permissions, throttling, parsers
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes, throttle_classes, parser_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from posts.views import post_content_is_valid, parse_content, save_hashtags, post_image_is_valid
from circles.models import Circle
from posts.models import Post


class RootView(APIView):
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer, )
    permissions_classes = permissions.AllowAny
    parser_classes = parsers.JSONParser, parsers.FormParser

    def get(self, request, *args, **kwargs):
        # TODO: add about page
        return Response({
            'API options':
                {
                    'login':
                        {
                        'URL':'/api/login/',
                        'Methods Allowed':'GET, POST'
                        },
                    'create':
                        {
                        'url':'/api/create/',
                        'Methods Allowed':'POST'
                        },
                    'Documentation':'Please read our Manual here: https://github.com/7Pros/circuit/blob/develop/MANUAL.md',
                    'Contact':'Please go to our About page: '
                }
        })


@api_view(['GET', 'POST'])
@renderer_classes((renderers.TemplateHTMLRenderer, renderers.JSONRenderer, ))
@permission_classes((permissions.AllowAny, ))
@authentication_classes((SessionAuthentication, ))
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
@parser_classes((parsers.JSONParser, parsers.MultiPartParser))
@csrf_exempt
def user_login(request):
    if request.method == 'GET':
        return Response(template_name='api/login.html', status=status.HTTP_200_OK)

    if request.method == 'POST':
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)
            if request.content_type == 'application/x-www-form-urlencoded':
                setattr(user,'circles', user.circle_set.all())
                return Response(data={
                    'message':
                        {
                            'status':0,
                            'content':'Login successful'
                        },
                    'user':user
                }, template_name='api/post_create.html', status=status.HTTP_202_ACCEPTED)
            elif request.content_type == 'application/json':
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)

                print(token.key)
                return Response(data={
                    'message':
                        {
                            'content':'Login succesful. To create a post please use post URL and give with it the given token to authenticate yourself!',
                            'token':token.key
                        }
                }, status=status.HTTP_202_ACCEPTED)

        return Response(data={
                            'message':
                                {
                                    'status':1,
                                    'content':'Login failed'
                                }
                        }, template_name='api/login.html', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@renderer_classes((renderers.TemplateHTMLRenderer, renderers.JSONRenderer, ))
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((SessionAuthentication, TokenAuthentication, ))
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
@parser_classes((parsers.JSONParser, parsers.MultiPartParser))
@csrf_exempt
def post_create(request):
    if request.method == 'POST' and request.content_type == 'multipart/form-data':
        if request.user.is_authenticated \
            and post_content_is_valid(request.data['content']):

            parsedString = parse_content(request.data['content'])
            post = Post(content=request.data['content'], author=request.user)

            if request.data['image'] and post_image_is_valid(request.data['image']):
                post.image = request.data['image']

            # TODO: fix circles
            if 'circle' in request.data and request.data['circle'] != '0':
                post.circles = Circle.objects.get(pk=request.data['circle'])

            post.save()
            save_hashtags(parsedString['hashtags'], post)
            setattr(request.user,'circles', request.user.circle_set.all())

            return Response(data={
                'message':
                    {
                        'status':0,
                        'content':'Post created'
                    },
                'user':request.user
            }, template_name='api/post_create.html', status=status.HTTP_201_CREATED)
    elif request.method == 'POST' and request.content_type == 'application/json':
        if request.user.is_authenticated \
            and post_content_is_valid(request.data['content']):

            parsedString = parse_content(request.data['content'])
            post = Post(content=request.data['content'], author=request.user)

            if 'image' in request.data and request.data['image'] and post_image_is_valid(request.data['image']):
                post.image = request.data['image']

            # TODO: fix circles
            if 'circle' in request.data and request.data['circle'] != '0':
                post.circles = Circle.objects.get(pk=request.data['circle'])

            post.save()
            save_hashtags(parsedString['hashtags'], post)

            token = request.auth

            return Response(data={
                'message':
                    {
                        'content':'Post created',
                        'token':token.key
                    }
            }, template_name='api/post_create.html', status=status.HTTP_201_CREATED)

        return Response(data={
            'message':
                {
                    'status':1,
                    'content':'Something went wrong!'
                }
        },template_name='api/post_create.html', status=status.HTTP_401_UNAUTHORIZED)
