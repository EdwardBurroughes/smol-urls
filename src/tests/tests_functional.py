import json

import pytest
import responses
from django.urls import reverse
from urllib.parse import urlparse

from urlShortener.models import URL


#TODO - add docker compose for the project

class TestShortenURL:

    @pytest.mark.django_db
    def test_shortend_url_post(self, client):
        url = reverse("shorten-url")
        original_url = "https://github.com/HelloWorld/JonFish"

        post_data = {"url": original_url}

        res = client.post(
            url,
            json.dumps(post_data),
            content_type="application/json"
        )
        response_data = res.json()
        shortened_url = response_data["shortened_url"]
        id = urlparse(shortened_url).path[1:]
        assert id == "EIPjve20"

        url_instance = URL.objects.get(shortened_id=id)
        assert url_instance.click_count == 0

    def test_shorten_url_post_bad_request(self, client):
        url = reverse("shorten-url")
        post_data = {"url": "https://github.com/HelloWorld/JonFish", "whitby": "kippers"}
        res = client.post(url, json.dumps(post_data), content_type="application/json")
        assert res.status_code == 400

    @pytest.mark.django_db
    def test_shortened_url_already_exists(self, client):
        url = reverse("shorten-url")
        original_url = "https://github.com/HelloWorld/JonFish"
        id = "EIPjve20"

        URL.objects.create(
            shortened_id=id,
            original_url=original_url,
        )

        post_data = {"url": original_url}
        res = client.post(
            url,
            json.dumps(post_data),
            content_type="application/json"
        )
        assert res.status_code == 200
        data = res.json()
        assert not data["created"]

    @pytest.mark.django_db
    def test_shorten_url_deleted(self, client):

        original_url = "https://github.com/HelloWorld/JonFish"
        id = "EIPjve20"

        URL.objects.create(
            shortened_id=id,
            original_url=original_url,
        )
        assert URL.objects.count() == 1
        url = reverse("delete-shortened-url", kwargs={"shortened_id": id})
        client.delete(url)
        assert URL.objects.count() == 0

    @responses.activate
    @pytest.mark.django_db
    def test_redirect_to_url(self, client):
        original_url = "http://example.com"
        id = "EIPjve20"
        responses.add(
            responses.GET,
            original_url,
            status=200,
        )
        url = URL.objects.create(
            shortened_id=id,
            original_url=original_url,
        )
        res = client.get(reverse("redirect-url", kwargs={"shortened_id": id}))
        assert res.status_code == 302

        url_after_redirect = URL.objects.get(id=url.id)
        assert url_after_redirect.click_count == 1