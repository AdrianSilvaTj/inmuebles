""" Aqui definiremos los permisos (Autorización) personalizados para cada tipo de usuario """
from rest_framework import permissions

class AdminOrReadOnlyPermission(permissions.IsAdminUser):
    """ Permisos administrativos o solo lectura """
    def has_permission(self, request, view):
        # redefinimos esta función has_permission
        # Cualquiera puede hacer una consulta de datos
        if request.method == 'GET':
            return True
        # para otras operaciones debe por lo menos ser un usuario staff
        staff_permission = bool(request.user and request.user.is_staff)
        return staff_permission
    
class CommentUserOrReadOnlyPermission(permissions.BasePermission):
    """ Solo el usuario creador de un comentario puede editarlo """
    def has_object_permission(self, request, view, obj):
        # si el metodo es de lectura, cualquiera puede hacerlo
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # verifica que el usuario actual sea el dueño del comentario
            return obj.comment_user  == request.user