from rest_framework.permissions import BasePermission


class CanViewAdminHistory(BasePermission):
    """
    Allows admins access to pass this.
    """

    message = 'You do not have permission to view admin history!'
    view_name = 'drf_user_activity_tracker_mongodb.view_activitylog'

    def has_permission(self, request, view):
        return request.user.has_perm(self.view_name)
