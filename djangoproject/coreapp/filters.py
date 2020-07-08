from rest_framework import filters, exceptions

from coreapp.consts_db import ApprovalStatus
from coreapp.utils import to_bool


class PostSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = request.GET.getlist('search_fields', [])
        search_fields_mappings = getattr(view, 'search_fields_mappings', {})
        if search_fields:
            try:
                return [search_fields_mappings[v] for v in search_fields]
            except KeyError:
                raise exceptions.ValidationError(
                    detail='Valid search fields are: ' + str(list(search_fields_mappings.keys())))
        return super().get_search_fields(view, request)


class PostCategoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        TODO: reorganize
        :return: returns user's all post unless particular approved_only/pending_only/rejected_only is mentioned
        only approved_only/pending_only/rejected_only is applicable if superuser
        """
        current_user_only = to_bool(request.query_params.get('my-only', None))
        approval_status = request.query_params.getlist('approval-status', [])

        if current_user_only:  # ?my-only=true
            if request.user.is_authenticated:
                queryset = queryset.filter(author=request.user)
            else:
                raise exceptions.NotAuthenticated(detail='Must be authenticated to fetch my-only=true')

        if approval_status:  # approval-status=all/approved/pending/rejected
            if not current_user_only and not (request.user.is_authenticated and request.user.moderator_account):
                raise exceptions.PermissionDenied(
                    detail='restricted url fields without my-only=true : approval-status')
            elif approval_status[0].lower() == 'all':
                approval_status = [ApprovalStatus.PENDING, ApprovalStatus.APPROVED, ApprovalStatus.REJECTED]
            else:
                try:
                    approval_status = [ApprovalStatus.STATUS_VALUE[v.upper()] for v in approval_status]
                except KeyError:
                    raise exceptions.ValidationError(detail='Invalid requested approval-status')
            queryset = queryset.filter(approval_status__in=approval_status)
        else:
            queryset = queryset.approved_only()

        return queryset
