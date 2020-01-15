from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from events.serializers import *
from events.models import *


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    """ 
    Logout.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"success": "logout"}, status=status.HTTP_200_OK)

class EventView(APIView):
    """ 
    Creates the event. 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        request.data['creator'] = request.user.id
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            if event:
                return Response({"success": "event created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

    """
    Update event.
    """
    def put(self, request, format='json'):
        request.data['creator'] = request.user.id
        event = get_object_or_404(Event, pk= request.data['id'])

        if event.creator.id != request.data['creator']:
            return Response({"message": "you are not event creator"}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            if event:
                return Response({"success": "event updated"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Delete event.
    """
    def delete(self, request, format='json'):
        event = get_object_or_404(Event, pk = request.data['id'])
        if event.creator.id != request.user.id:
            return Response({"message": "you are not event creator"}, status=status.HTTP_403_FORBIDDEN)

        try:
            event.delete()
            return Response({"success": "event deleted"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": ex}, status=status.HTTP_400_BAD_REQUEST)      
            

    def update(self, request):
        request.data['creator'] = request.user.id
        event = get_object_or_404(Event, pk= request.data['id'])

        if event.creator.id != request.data['creator']:
            return Response({"message": "you are not event creator"}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            if event:
                return Response({"success": "event updated"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventList(APIView):
    """
    List events.
    """
    def get(self, request, ini, fin):
        sort = request.GET.get('sort', '')
        text = request.GET.get('text', '')

        events = Event.objects.all()
        if sort == 'date':
            events = events.order_by('-date')
        elif sort == 'comments':
            events = events.annotate(num_comments=Count('comments')).order_by('-num_comments')
        elif sort == 'interested':
            events = events.annotate(num_interested=Count('interaction', filter=Q(interaction__option='Interested'))).order_by('-num_interested')
        if text !=  '':
            events = events.filter(name__icontains = text, description__icontains = text)
        
        events = events[int(ini):int(fin)]
        serializer = EventSerializer(events, many = True)
        return Response(serializer.data)   

class EventDetail(APIView):
    """
    Get detail event
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        event = get_object_or_404(Event, pk = pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)  

class InteractionCreate(APIView):
    """ 
    Creates the interaction. 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        request.data['userId'] = request.user.id
        serializer = InteractionSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            if event:
                return Response({"success": "interaction created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentCreate(APIView):
    """ 
    Creates the comment. 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        request.data['creator'] = request.user.id
        if not 'eventId' in request.data:
            return Response({"error": "eventId required"}, status=status.HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Event, pk=request.data['eventId'])

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            event.comments.add(comment)
            if comment:
                return Response({"success": "comment created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResponseCreate(APIView):
    """ 
    Creates the comment. 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        request.data['creator'] = request.user.id
        if not 'commentId' in request.data:
            return Response({"error": "commentId required"}, status=status.HTTP_400_BAD_REQUEST)
        comment_parent = get_object_or_404(Comment, pk=request.data['commentId'])

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            comment_parent.responses.add(comment)
            if comment:
                return Response({"success": "response created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
