import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as f:
        platers_data = json.load(f)

    for nickname, player_data in platers_data.items():

        race_data = player_data["race"]
        race_obj, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data["description"]}
        )

        skills_list = race_data.get("skills", [])
        for skill_item in skills_list:
            Skill.objects.get_or_create(
                name=skill_item["name"],
                defaults={"bonus": skill_item.get("bonus")},
                race=race_obj
            )
        if player_data.get("guild"):
            guild_data = player_data["guild"]
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")},
            )
        else:
            guild_obj = None
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email" : player_data["email"],
                "bio" : player_data["bio"],
                "race": race_obj,
                "guild": guild_obj
            }
        )


if __name__ == "__main__":
    main()
