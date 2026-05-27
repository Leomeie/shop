import pytest
from rest_framework import status
from apps.products.models import Category, Product
from apps.reviews.models import Review


@pytest.fixture
def category(db):
    return Category.objects.create(name="测试分类", level=1, is_active=True)


@pytest.fixture
def product(category, db):
    return Product.objects.create(
        name="测试商品",
        description="测试描述",
        category=category,
        status="active",
        main_image="test.jpg",
        file="test.zip",
    )


@pytest.mark.django_db
class TestReviewImages:
    def test_create_review_with_images(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        resp = api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 5,
            "content": "很好用",
            "images": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert len(resp.data["data"]["images"]) == 2

    def test_create_review_without_images(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        resp = api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 4,
            "content": "不错",
        }, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["data"]["images"] == []

    def test_images_max_5(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        images = [f"https://example.com/img{i}.jpg" for i in range(6)]
        resp = api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 3,
            "images": images,
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_images_must_be_urls(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        resp = api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 3,
            "images": ["not-a-url"],
        }, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_review_list_includes_images(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 5,
            "images": ["https://example.com/a.jpg"],
        }, format="json")
        resp = api_client.get(f"/api/v1/reviews/product/{product.pk}/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["results"][0]["images"] == ["https://example.com/a.jpg"]

    def test_images_stored_as_json(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        api_client.post("/api/v1/reviews/", {
            "product_id": product.pk,
            "rating": 5,
            "images": ["https://example.com/x.jpg"],
        }, format="json")
        review = Review.objects.filter(user=test_user, product=product).first()
        assert review.images == ["https://example.com/x.jpg"]


@pytest.mark.django_db
class TestReviewStats:
    def test_stats_with_reviews(self, api_client, test_user, product, db):
        Review.objects.create(
            user=test_user, product=product, rating=5,
            images=["https://example.com/a.jpg"],
        )
        resp = api_client.get(f"/api/v1/reviews/product/{product.pk}/stats/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["data"]["total"] == 1
        assert resp.data["data"]["avg_rating"] == 5.0

    def test_stats_empty(self, api_client, product):
        resp = api_client.get(f"/api/v1/reviews/product/{product.pk}/stats/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["data"]["total"] == 0
