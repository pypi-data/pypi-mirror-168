from whizbang.config.app_config import AppConfig
from whizbang.domain.exceptions import AzCliException
from whizbang.domain.handler.handler_base import HandlerBase
from whizbang.domain.manager.az.az_lock_manager import AzLockManager
from whizbang.domain.models.lock import LockType, ResourceLock


class LockHandler(HandlerBase):
    def __init__(self,
                 app_config: AppConfig,
                 manager: AzLockManager):
        HandlerBase.__init__(self, app_config=app_config)
        self.manager = manager

    def create_resource_level_lock(self, lock_type: LockType,
                                   name: str,
                                   resource: str,
                                   resource_group: str,
                                   resource_type: str):
        """
        Creates a resource level lock
        :param lock_type: The type of lock to create
        :param name: The name of the lock
        :param resource: The resource name to lock
        :param resource_group: The resource group holding the lock
        :param resource_type: The resource type matches the service provider of the resource e.g. Microsoft.Storage/storageAccounts
        :return:
        """
        resource_lock = ResourceLock(
            lock_type=lock_type,
            name=name,
            resource=resource,
            resource_group=resource_group,
            resource_type=resource_type
        )
        self.manager.create_resource_level_lock(resource_lock=resource_lock)

    def delete_resource_level_lock(self,
                                   name: str,
                                   resource: str,
                                   resource_group: str,
                                   resource_type: str):
        """
        Deletes a resource level lock
        :param name: The name of the lock
        :param resource: The resource name to lock
        :param resource_group: The resource group holding the lock
        :param resource_type: The resource type matches the service provider of the resource e.g. Microsoft.Storage/storageAccounts
        :return:
        """
        resource_lock = ResourceLock(
            name=name,
            resource=resource,
            resource_group=resource_group,
            resource_type=resource_type
        )
        self.manager.delete_resource_level_lock(resource_lock=resource_lock)

    def show_resource_level_lock(self,
                                   name: str,
                                   resource: str,
                                   resource_group: str,
                                   resource_type: str):
        """
        Shows a resource level lock
        :param name: The name of the lock
        :param resource: The resource name to lock
        :param resource_group: The resource group holding the lock
        :param resource_type: The resource type matches the service provider of the resource e.g. Microsoft.Storage/storageAccounts
        :return: Returns a dictionary definition of the lock if it exists, else returns None
        """
        resource_lock = ResourceLock(
            name=name,
            resource=resource,
            resource_group=resource_group,
            resource_type=resource_type
        )
        try:
            return self.manager.show_resource_level_lock(resource_lock=resource_lock)
        except AzCliException:
            return None
