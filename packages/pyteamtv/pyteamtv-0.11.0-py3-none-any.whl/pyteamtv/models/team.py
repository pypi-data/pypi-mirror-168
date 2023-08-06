from .list import List
from .person import Person
from .player import Player
from .teamtv_object import TeamTVObject


class Team(TeamTVObject):
    @property
    def name(self):
        return self._name

    @property
    def team_id(self):
        return self._team_id

    @property
    def sport_type(self):
        return self._sport_type

    @property
    def tags(self):
        return self._tags

    def _use_attributes(self, attributes: dict):
        tags = attributes.get("tags", {})
        if not isinstance(tags, dict):
            tags = {}

        self._team_id = attributes["teamId"]
        self._name = attributes["name"]
        self._sport_type = attributes["sportType"]
        self._tags = tags

    def __repr__(self):
        return f"<Team name={self.name} team_id={self.team_id}>"

    def get_players(self):
        def player_factory(requester, attributes) -> Player:
            return Player(requester, dict(team=self, **attributes))

        return List(
            player_factory, self._requester, "GET", f"/teams/{self.team_id}/players"
        )

    def add_player(self, person: Person, number: str) -> Player:
        data = self._requester.request(
            "POST",
            f"/teams/{self.team_id}/players",
            {"personId": person.person_id, "number": number},
        )

        # Add the data from the person object. The
        # players POST api doesn't return the person object
        data["person"] = dict(
            personId=person.person_id,
            firstName=person.first_name,
            lastName=person.last_name,
            gender=person.gender,
            tags=person.tags,
        )
        data["team"] = self
        return Player(self._requester, data)
