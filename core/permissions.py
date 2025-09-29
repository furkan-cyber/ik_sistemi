from rest_framework import permissions 
 
class IsIlanlariPermission(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj): 
        if not hasattr(request.user, 'ikuser'): 
            return False 
        return obj.ik_firma == request.user.ikuser.ik_firma 
 
class AdayAkisPermission(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj): 
        if not hasattr(request.user, 'ikuser'): 
            return False 
        return obj.is_ilani.ik_firma == request.user.ikuser.ik_firma 
