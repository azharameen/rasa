import glob
import json

import io
import jsonpickle
import pytest

from rasa_core import utils
from rasa_core.domain import Domain
from rasa_core.tracker_store import InMemoryTrackerStore
from tests.utilities import tracker_from_dialogue_file


@pytest.mark.parametrize("filename", glob.glob('data/test_dialogues/*json'))
def test_dialogue_serialisation(filename):
    dialogue_json = utils.read_file(filename)
    restored = json.loads(dialogue_json)
    tracker = tracker_from_dialogue_file(filename)
    en_de_coded = json.loads(jsonpickle.encode(tracker.as_dialogue()))
    assert restored == en_de_coded


@pytest.mark.parametrize("pair", zip(sorted(glob.glob('data/test_dialogues/*json')),
                                     ["examples/formbot/domain.yml",
                                      "examples/moodbot/domain.yml",
                                      "examples/restaurantbot/restaurant_domain.yml"]))
def test_inmemory_tracker_store(pair):
    filename, domainpath = pair
    domain = Domain.load(domainpath)
    tracker = tracker_from_dialogue_file(filename, domain)
    tracker_store = InMemoryTrackerStore(domain)
    tracker_store.save(tracker)
    restored = tracker_store.retrieve(tracker.sender_id)
    assert restored == tracker


def test_tracker_restaurant():
    domain = Domain.load("examples/restaurantbot/restaurant_domain.yml")
    filename = 'data/test_dialogues/restaurantbot.json'
    tracker = tracker_from_dialogue_file(filename, domain)
    assert tracker.get_slot("price") == "lo"
    assert tracker.get_slot("name") is None     # slot doesn't exist!
