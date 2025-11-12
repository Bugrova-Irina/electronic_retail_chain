from users.permissions import IsActiveEmployee


class ActiveEmployeePermissionMixin:
    """
    Миксин для предоставления доступа только активным сотрудникам
    """
    permission_classes = (IsActiveEmployee,)
