from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    snippets = {
        'ahihi1' : 1,
        'ahihi2' : 2,
    }
    return Response(snippets)