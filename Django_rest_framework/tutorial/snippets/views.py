# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from django.contrib.auth.models import User

from snippets.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import action
# Create your views here.


"""
	Use method view to create an endpoint for the root of our API

	The DefaultRouter class will automatically create this API root view for us, so we don't really need this method any more
"""
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })


# class UserList(generics.ListAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
		This viewset automatically provides 'list' and 'detail' actions

		also the readonlymodelviewset will automatically provide the read-only operations
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer



# class SnippetHighlight(generics.GenericAPIView):
# 	"""
# 		since we will not return a whole object, but a field of a model, we need to customize our own get method
# 	"""
# 	queryset = Snippet.objects.all()
# 	renderer_classes = (renderers.StaticHTMLRenderer,)

# 	def get(self, request, *args, **kwargs):
# 		snippet = self.get_object()
# 		return Response(snippet.highlighted)


# class SnippetList(APIView):
# 	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# 	def perform_create(self, serializer):
# 		serializer.save(owner=self.request.user)

# 	def get(self, request, format=None):
# 		snippets = Snippet.objects.all()
# 		# need pass the request as a context and careful don't let it be a set!!
# 		serializer = SnippetSerializer(snippets, many=True, context={'request':request})
# 		return Response(serializer.data)

# 	def post(self, request, format=None):
# 		serializer = SnippetSerializer(data=request.data)
# 		if serializer.is_valid():
# 			self.perform_create(serializer)
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):

# 	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

# 	def get_object(self, pk):
# 		try:
# 			return Snippet.objects.get(pk=pk)
# 		except Snippet.DoesNotExist:
# 			raise Http404

# 	def get(self, request, pk, format=None):
# 		snippet = self.get_object(pk)
# 		serializer = SnippetSerializer(snippet, context={"request": request})
# 		return Response(serializer.data)

# 	def put(self, request, pk,  format=None):
# 		snippet = self.get_object(pk)
# 		serializer = SnippetSerializer(snippet, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 	def delete(self, request, pk, format=None):
# 		snippet = self.get_object(pk)
# 		snippet.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetViewSet(viewsets.ModelViewSet):
	"""
		This viewset automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

		additonally we also provide an extra 'highlight' action
	"""

	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

	@action(detail=True, renderer_classes = [renderers.StaticHTMLRenderer])
	def highlight(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

	def perform_create(self, serializer):
		"""
			Method used to pass the request user data to the serializer so we can bind the snippet with the corresponding user
		"""
		serializer.save(owner=self.request.user)
