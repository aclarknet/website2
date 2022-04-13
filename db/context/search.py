from ..utils import get_search_results


def context_search(context, request=None, models=None, q=None):
    if request.method == "POST":
        q = request.POST.get("q")
    if q:
        context["items"] = get_search_results(q, models=models, request=request)
    else:
        context["items"] = []
    return context
