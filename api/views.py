"""@package api
API views controllers.

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
    """
    Generic View of the root view, which contains the use documentation of the API, it gives it as a Browsable API or JSON.

    This can be requested from anyone and renders the requests from JSON and Forms.
    """
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
                        'Methods Allowed':'GET, POST',
                        'Required data':
                            {
                                'email':'The registered email for the user\'s account',
                                'password':'The password for the account'
                            }
                        },
                    'create':
                        {
                        'url':'/api/create/',
                        'Methods Allowed':'POST',
                        'Required data':
                            {
                                'content':'Maximum length of 256 characters. It is the post content and it can contain text, mentions, and hashtags',
                                'image':'An uploaded image or None if non will be given',
                                'circles':'The int value of a circle. Default values are:\n 0 -> Me circle \n 1 -> Public circle'
                            }

                        },
                    'Documentation':'Please read our Manual here: https://github.com/7Pros/circuit/blob/develop/MANUAL.md',
                    'Contact':'Please go to our About page: '
                }
        })


@api_view(['GET', 'POST'])
@renderer_classes((renderers.TemplateHTMLRenderer, renderers.JSONRenderer, ))
@authentication_classes((SessionAuthentication, TokenAuthentication, ))
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
@permission_classes((permissions.AllowAny, ))
@parser_classes((parsers.JSONParser, parsers.MultiPartParser))
@csrf_exempt
def user_login(request):
    """
    It returns the login to the API, authenticate users and grants access to post creation.

    The decorators render the responses to HTML or JSON, take care of the authentication and the throttling and set
    the permissions to anyone, as well as the parsing of the incoming data.

    @param request: the incoming request.
    @return: Response rendering a template in case the request was made with a form or a json in case it was a application/json type.
    """
    if request.method == 'GET':
        return Response(template_name='api/login.html', status=status.HTTP_200_OK)

    if request.method == 'POST':
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)
            if 'application/x-www-form-urlencoded' in request.content_type:
                setattr(user,'circles', user.circle_set.all())
                return Response(data={
                    'message':
                        {
                            'status':0,
                            'content':'Login successful'
                        },
                    'user':user
                }, template_name='api/post_create.html', status=status.HTTP_202_ACCEPTED)
            elif 'application/json' in request.content_type:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)

                user_circles = user.circle_set.all()
                user_circles_json = dict()
                for circle in user_circles:
                    user_circles_json.pop(circle.pk, circle.name)
                return Response(data={
                    'message':
                        {
                            'content':'Login succesful. To create a post please use post URL and give with it the given token to authenticate yourself!',
                            'token':token.key
                        },
                    'post-required-values':
                        {
                            'content':
                            {
                                'Description':'Can contain mentions and hashtags.',
                                'Restrictions':'Text max length 256 characters and min length 1 character.',
                            },
                            'circle':
                            {
                                'Description':'Determines from who the post can be seen.',
                                'Restrictions':'Select one, if one is selected than is going to be in the circle \'Me\'',
                                'Values':user_circles_json,
                            },
                            'image':
                            {
                                'Description':'It can be a file uploaded, desafortunately not via json',
                                'Restrictions':'If none given, please write None'
                            }
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
@authentication_classes((SessionAuthentication, TokenAuthentication, ))
@permission_classes((permissions.IsAuthenticated, ))
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
@parser_classes((parsers.JSONParser, parsers.MultiPartParser))
@csrf_exempt
def post_create(request):
    """
    If the user is authenticated, it will perform the posting of a new entry to the user it was logged in profile.

    The decorators take care of the rendering of the content, the authentication of the incoming requests, the permissions the
    incoming requests have, the throttling and the parsers.

    @param request: incoming request.
    @return: Response rendering a template in case the request was made with a form or a json in case it was a application/json type.
    """
    if request.method == 'POST' and 'multipart/form-data' in request.content_type:
        # authentication
        if request.user.is_authenticated:
            # post validation
            if post_content_is_valid(request.data['content']):

                parsedString = parse_content(request.data['content'])
                post = Post(content=request.data['content'], author=request.user)

                # non required fields
                if request.data['image'] and post_image_is_valid(request.data['image']):
                    post.image = request.data['image']

                # TODO: fix circles
                # non required fields
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
        #Authentification failed response
        return Response(data={
                        'message':
                            {
                                'status':1,
                                'content':'Not authenticated or content is not valid!'
                            }
                    },template_name='api/post_create.html', status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST' and 'application/json' in request.content_type:
        if request.user.is_authenticated:
            if post_content_is_valid(request.data['content']):

                parsedString = parse_content(request.data['content'])
                post = Post(content=request.data['content'], author=request.user)

                if 'image' in request.data and request.data['image'] and post_image_is_valid(request.data['image']):
                    post.image = request.data['image']

                # TODO: fix circles
                if 'circle' in request.data and request.data['circle'] != '0':
                    post.circles = Circle.objects.get(pk=request.data['circle'])

                post.save()
                save_hashtags(parsedString['hashtags'], post)

                user_circles = request.user.circle_set.all()
                user_circles_json = dict()
                for circle in user_circles:
                    user_circles_json.pop(circle.pk, circle.name)
                token = request.auth

                return Response(data={
                    'message':
                        {
                            'action-feedback':'Post created',
                            'user-authentication-token':token.key
                        },
                    'post-required-values':
                        {
                            'content':
                            {
                                'Description':'Can contain mentions and hashtags.',
                                'Restrictions':'Text max length 256 characters and min length 1 character.',
                            },
                            'circle':
                            {
                                'Description':'Determines from who the post can be seen.',
                                'Restrictions':'Select one, if one is selected than is going to be in the circle \'Me\'',
                                'Values':user_circles_json,
                            },
                            'image':
                            {
                                'Description':'It can be a file uploaded, desafortunately not via json',
                                'Restrictions':'If none given, please write None'
                            }
                        }
                }, template_name='api/post_create.html', status=status.HTTP_201_CREATED)
        return Response(data={
            'message':
                {
                    'status':1,
                    'content':'Not authenticated or content is not valid!'
                }
        },template_name='api/post_create.html', status=status.HTTP_401_UNAUTHORIZED)
    #Authentification failed response
    return Response(data={
            'message':
                {
                    'status':1,
                    'content':'Something went wrong!'
                }
        },template_name='api/post_create.html', status=status.HTTP_401_UNAUTHORIZED)
