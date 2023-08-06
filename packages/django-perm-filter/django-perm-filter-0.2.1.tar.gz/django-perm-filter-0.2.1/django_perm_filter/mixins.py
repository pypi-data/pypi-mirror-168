from django_perm_filter.utils import filter_perms


class PermissionFilterMixin(object):
    """Django admin mixin."""

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in ("permissions", "user_permissions"):
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            qs = filter_perms(qs)
            kwargs["queryset"] = qs

        return super().formfield_for_manytomany(db_field, request, **kwargs)
