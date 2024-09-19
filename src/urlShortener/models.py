from django.db import models


class URL(models.Model):
    original_url = models.URLField()
    shortened_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("shortened_id",),
                name="unique_shortened_id",
            ),
        )

    def __str__(self):
        return self.shortened_id

    def increment_click_count(self) -> None:
        self.click_count += 1
        self.save()

