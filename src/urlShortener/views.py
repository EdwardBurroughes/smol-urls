from django import http
from django.db import transaction
from django import views
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import domain, models, utils, queries


@method_decorator(csrf_exempt, name='dispatch')
class ShortenURL(views.View):

    def get(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        shortened_id = kwargs["shortened_id"]
        # potentially use a domain driven design
        url = get_object_or_404(models.URL, shortened_id=shortened_id)
        url.increment_click_count()
        return redirect(
            url.original_url
        )

    def post(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        try:
            data = domain.ShortenUrl.deserialise(request.body)
            hash_id = utils.hash_url_to_base62(data.url)
            url_instance, created = queries.get_or_create_shortened_url(
                hash_id,
                data.url
            )
            return http.JsonResponse(
                {
                    "original_url": url_instance.original_url,
                    "shortened_url": request.build_absolute_uri(
                        f"/{url_instance.shortened_id}"
                    ),
                    "created": created
                },
                status=200,
            )
        except domain.MalformedPayload as e:
            # add something meaningful
            return http.HttpResponseBadRequest({"message": "Malformed payload"})

    def delete(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        with transaction.atomic():
            url_instance = get_object_or_404(models.URL, shortened_id=kwargs["shortened_id"])
            url_instance.delete()
        return http.JsonResponse({"status": "success"}, status=200)
