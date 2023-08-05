""" Story Teller Definition """
import json
import random
from pathlib import Path
from typing import Any, Optional

from pydantic import ValidationError

from rowantree.contracts import StoreType, UserEvent, UserStore

from ..abstract.abstract_loremaster import AbstractLoremaster


class WorldStoryTeller(AbstractLoremaster):
    """
    The Story Teller
    This class handles world encounters.
    """

    MAX_ENCOUNTER_TRIES = 10

    events: list[UserEvent] = []

    def __init__(self, **data: Any):
        super().__init__(**data)

        with open(file=(Path(__file__).parent / "events.json").resolve(), mode="r", encoding="utf-8") as file:
            global_events_dict = json.load(file)

        for event_dict in global_events_dict["events"]:
            try:
                event: UserEvent = UserEvent.parse_obj(event_dict)
                self.events.append(event)
            except ValidationError as error:
                print(event_dict)
                raise error

    def generate_event(self, user_population: int, user_stores: dict[StoreType, UserStore]) -> Optional[UserEvent]:
        """
        Generates a world event (encounter).

        Parameters
        ----------
        user_population: UserPopulation
            The target user population.
        user_stores: UserStores
            The target user stores.

        Returns
        -------
        outbound_event: Optional[UserEvent]
            An optional encounter for the target user.
        """

        num_events: int = len(self.events)
        requirement_check: bool = False
        counter: int = 0
        new_event: Optional[UserEvent] = None

        while requirement_check is False:
            counter += 1
            event_index = random.randint(1, num_events) - 1
            new_event = self.events[event_index].copy()

            # check requirements
            for requirement in new_event.requirements:
                if requirement == "population":
                    min_required_pop = new_event.requirements[requirement]
                    # logging.debug('reported user population: ' + str(user_population))
                    if user_population >= min_required_pop:
                        requirement_check = True
                else:
                    # assume it is a store - get the current amount of the store for the user
                    min_required_store = new_event.requirements[requirement]
                    if requirement in user_stores:
                        if user_stores[requirement].amount >= min_required_store:
                            requirement_check = True

            # bail out if we've reached the max, no encounters this time
            if counter >= self.MAX_ENCOUNTER_TRIES:
                new_event = None
                requirement_check = True

        if new_event is None:
            return None

        # remove the requirements stanza before we send to over to the client
        new_event.requirements = {}

        return new_event
