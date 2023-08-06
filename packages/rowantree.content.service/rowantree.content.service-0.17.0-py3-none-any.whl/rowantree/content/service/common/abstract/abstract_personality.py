""" Abstract Personality Definition """

import logging
import random
from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from rowantree.contracts import Action, ActionQueue, StoreType, UserEvent, UserEventOtherType, UserStore
from rowantree.game.service.sdk import RowanTreeService

from .abstract_loremaster import AbstractLoremaster


class AbstractPersonality(BaseModel):
    """
    WorldPersonality (Default)
    Generates game world content.

    Attributes
    ----------
    rowantree_service: RowanTreeService
        The Rowan Tree Service Interface.
    loremaster: AbstractLoremaster
        An instance of a story teller for encounter generation.
    """

    rowantree_service: RowanTreeService
    loremaster_service: AbstractLoremaster

    class Config:
        """Pydantic Default Config Over-Rides"""

        arbitrary_types_allowed = True

    ##############
    ## Event Queueing
    ##############

    # TODO: Review the complexity of this
    # pylint: disable=too-many-branches
    def _process_user_event(self, event: Optional[UserEvent], target_user: str) -> None:
        """
        Processes the provided user event (applies the state change of the event)

        Parameters
        ----------
        event: Optional[dict]
            The optional event to process.

        target_user: str
            The target user guid.
        """

        if event is None:
            return

        action_queue: ActionQueue = ActionQueue(queue=[])
        user_stores: dict[StoreType, UserStore] = self.rowantree_service.user_stores_get(user_guid=target_user)

        # process rewards
        rewards_to_remove: list = []
        for reward in event.reward.keys():
            if event.reward[reward] <= 1:
                amount: int = 1
            else:
                amount: int = random.randint(1, event.reward[reward])  # Determine an amount up to the max specified.

            if reward == UserEventOtherType.POPULATION:
                action_queue.queue.append(Action(name="deltaUserPopulationByGUID", arguments=[target_user, amount]))
                event.reward[reward] = amount  # Update to the actual amount
            else:
                if reward in user_stores:
                    store_amt: int = user_stores[reward].amount
                    if store_amt < amount:
                        amount = store_amt

                    action_queue.queue.append(
                        Action(name="deltaUserStoreByStoreNameByGUID", arguments=[target_user, reward, amount])
                    )
                    event.reward[reward] = amount
                else:
                    # Remove skipped types
                    rewards_to_remove.append(reward)
        for reward in rewards_to_remove:
            del event.reward[reward]

        # process curses
        curses_to_remove: list = []
        for curse in event.curse.keys():
            if curse == UserEventOtherType.POPULATION:
                if event.curse[curse] <= 1:
                    pop_amount: int = 1
                else:
                    pop_amount: int = random.randint(1, event.curse[curse])

                user_population: int = self.rowantree_service.user_population_get(user_guid=target_user)
                if user_population < pop_amount:
                    pop_amount: int = user_population

                action_queue.queue.append(
                    Action(name="deltaUserPopulationByGUID", arguments=[target_user, (pop_amount * -1)])
                )
                event.curse[curse] = pop_amount
            else:
                if event.curse[curse] <= 1:
                    amount: int = 1
                else:
                    amount: int = random.randint(1, event.curse[curse])

                if curse in user_stores:
                    store_amt = user_stores[curse].amount
                    if store_amt < amount:
                        amount = store_amt
                else:
                    # Remove skipped types
                    curses_to_remove.append(curse)
                action_queue.queue.append(
                    Action(name="deltaUserStoreByStoreNameByGUID", arguments=[target_user, curse, (amount * -1)])
                )
                event.curse[curse] = amount
        for curse in curses_to_remove:
            del event.curse[curse]

        # Send them the whole event object.
        action_queue.queue.append(
            Action(name="sendUserNotificationByGUID", arguments=[target_user, event.json(by_alias=True)])
        )

        logging.debug(action_queue.json(by_alias=True))
        self.rowantree_service.action_queue_process(queue=action_queue)

    @abstractmethod
    def contemplate(self):
        """Main loop for processing an epoch of events"""
