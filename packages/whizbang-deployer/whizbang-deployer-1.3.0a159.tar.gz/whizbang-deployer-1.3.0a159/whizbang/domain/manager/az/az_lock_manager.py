from whizbang.domain.manager.az.az_manager_base import AzManagerBase
from whizbang.domain.manager.az.az_resource_manager_base import AzResourceManagerBase
from whizbang.domain.models.lock import ResourceLock
from whizbang.domain.repository.az.az_lock_repository import AzLockRepository


class AzLockManager(AzResourceManagerBase):
    def __init__(self, repository: AzLockRepository):
        AzManagerBase.__init__(self, repository)
        self._repository: AzLockRepository

    def create_resource_level_lock(self, resource_lock: ResourceLock):
        """
        Creates a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns None
        """

        self._repository.create_resource_level_lock(resource_lock=resource_lock)

    def delete_resource_level_lock(self, resource_lock: ResourceLock):
        """
        Deletes a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns None
        """

        self._repository.delete_resource_level_lock(resource_lock=resource_lock)

    def show_resource_level_lock(self, resource_lock: ResourceLock) -> dict:
        """
        Shows a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns dictionary definition of a lock
        """

        return self._repository.show_resource_level_lock(resource_lock=resource_lock)