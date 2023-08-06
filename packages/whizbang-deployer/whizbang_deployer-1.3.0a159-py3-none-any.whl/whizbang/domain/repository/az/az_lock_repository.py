from whizbang.data.az_cli_context import AzCliContext
from whizbang.domain.models.lock import ResourceLock
from whizbang.domain.repository.az.az_repository_base import AzRepositoryBase


class AzLockRepository(AzRepositoryBase):
    def __init__(self, context: AzCliContext):
        AzRepositoryBase.__init__(self, context)

    @property
    def _resource_provider(self) -> str:
        return 'lock'

    def create_resource_level_lock(self, resource_lock: ResourceLock):
        """
        Creates a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns None
        """

        self._execute(f'create --lock-type {resource_lock.lock_type.name}'
                      f' --name {resource_lock.name}'
                      f' --resource {resource_lock.resource}'
                      f' --resource-group {resource_lock.resource_group}'
                      f' --resource-type {resource_lock.resource_type}')

    def delete_resource_level_lock(self, resource_lock: ResourceLock):
        """
        Deletes a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns None
        """

        self._execute(f'delete'
                      f' --name {resource_lock.name}'
                      f' --resource {resource_lock.resource}'
                      f' --resource-group {resource_lock.resource_group}'
                      f' --resource-type {resource_lock.resource_type}')

    def show_resource_level_lock(self, resource_lock: ResourceLock) -> dict:
        """
        Shows a lock scoped to a specific resource
        :param resource_lock: The definition of the lock
        :return: Returns a dictionary definition of the lock
        """

        response = self._execute(f'show'
                                 f' --name {resource_lock.name}'
                                 f' --resource {resource_lock.resource}'
                                 f' --resource-group {resource_lock.resource_group}'
                                 f' --resource-type {resource_lock.resource_type}')
        return response.results
