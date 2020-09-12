from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Tag
from .serializers import *


@api_view(['GET', 'Post'])
def posts_list(request):
    """
    List of posts.
    """
    if request.method == 'GET':
        data = []
        tag = request.GET.get('tag', 0)
        if int(tag):
            posts = Post.objects.filter(tag=tag).order_by('date')
        else:
            posts = Post.objects.all().order_by('date')
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 3)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        posts_page = PostSerializer(data, context={'request': request}, many=True)

        tags = Tag.objects.all()
        tags = TagSerializer(tags, context={'request': request}, many=True)

        return Response({'postsPage': posts_page.data,
                         'tags': tags.data,
                         'count': paginator.count,
                         'numPages': paginator.num_pages,
                         })

    if request.method == 'Post':
        pass


@api_view(['GET'])
def posts_detail(request, id):
    """
    Get letter by id.
    """
    try:
        letter = Letter.objects.get(id=id)
    except Letter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LetterSerializer(letter, context={'request': request})
        return Response(serializer.data)
