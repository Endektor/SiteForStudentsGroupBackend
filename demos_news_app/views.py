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
        nextPage = 1
        prevPage = 1
        posts = Post.objects.all()
        # page = request.GET.get('page', 1)
        # paginator = Paginator(posts, 10)
        # try:
        #     data = paginator.page(page)
        # except PageNotAnInteger:
        #     data = paginator.page(1)
        # except EmptyPage:
        #     data = paginator.page(paginator.num_pages)

        pasts_page = PostSerializer(posts, context={'request': request}, many=True)
        # if data.has_next():
        #     nextPage = data.next_page_number()
        # if data.has_previous():
        #     prevPage = data.previous_page_number()

        tags = Tag.objects.all()
        tags = TagSerializer(tags, context={'request': request}, many=True)

        return Response({'posts_page': pasts_page.data,
                         'tags': tags.data,
                         # 'count': paginator.count,
                         # 'numpages': paginator.num_pages,
                         # 'nextlink': '/api/letters/?page=' + str(nextPage),
                         # 'prevlink': '/api/letters/?page=' + str(prevPage)
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