""" WorldPersonality Definition """

import random
import time
from typing import Optional

from rowantree.contracts import StoreType, UserEvent, UserStore
from rowantree.game.service.sdk import WorldStatus

from ..abstract.abstract_personality import AbstractPersonality


class WorldPersonality(AbstractPersonality):
    """
    WorldPersonality (Default)
    Generates game world content.

    Attributes
    ----------
    """

    max_sleep_time: int = 3  # in seconds
    encounter_change: int = 100  # in percent

    def contemplate(self) -> None:
        """Reviews active players, and for content."""

        # get active users
        world_status: WorldStatus = self.rowantree_service.world_status_get()
        for target_user in world_status.active_users:
            # Lets add an encounter
            self._encounter(target_user=target_user)

        # now sleep..
        self._slumber()

    def _encounter(self, target_user: str) -> None:
        """
        Cause an encounter.

        Parameters
        ----------
        target_user: str
            The target active user.
        """

        if WorldPersonality._luck(odds=self.encounter_change) is True:
            user_stores: dict[StoreType, UserStore] = self.rowantree_service.user_stores_get(user_guid=target_user)
            user_population: int = self.rowantree_service.user_population_get(user_guid=target_user)

            event: Optional[UserEvent] = self.loremaster_service.generate_event(
                user_population=user_population, user_stores=user_stores
            )
            self._process_user_event(event=event, target_user=target_user)

    def _slumber(self) -> None:
        """
        Sleep wrapper.
        Sleeps for a random amount of time up to the max.
        """

        time.sleep(random.randint(1, self.max_sleep_time))

    @staticmethod
    def _luck(odds: int) -> bool:
        """
        Probability Sample (should something happen)

        Parameters
        ----------
        odds: int
            Change in percent (up to 100%)

        Returns
        -------
        trigger: bool
            Result of the probability evaluation.

        """
        # Ask only for what you truely need and beware you may be granted your wish.
        flip: int = random.randint(1, 100)
        if flip <= odds:
            return True
        return False
