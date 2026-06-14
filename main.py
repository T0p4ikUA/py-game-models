import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as f:
        platers_data = json.load(f)

    for nickname, player_data in platers_data.items():
        if not isinstance(player_data, dict):
            continue

        race_data = player_data.get("race")
        if race_data and isinstance(race_data, dict):
            race_name = race_data.get("name")
            # Створюємо расу тільки якщо є її ім'я
            if race_name:
                race_obj, _ = Race.objects.get_or_create(
                    name=race_name,
                    defaults={"description": race_data.get("description", "")}
                )
            else:
                continue
        else:
            continue

        skills_list = race_data.get("skills", [])
        if isinstance(skills_list, list):
            for skill_item in skills_list:
                if isinstance(skill_item, dict):
                    skill_name = skill_item.get("name")
                    if skill_name:
                        Skill.objects.get_or_create(
                            name=skill_name,
                            defaults={"bonus": skill_item.get("bonus", "")},
                            race=race_obj
                        )

        guild_data = player_data.get("guild")
        if guild_data and isinstance(guild_data, dict):
            guild_name = guild_data.get("name")
            if guild_name:
                guild_obj, _ = Guild.objects.get_or_create(
                    name=guild_name,
                    defaults={
                        "description": guild_data.get("description", "")
                    },
                )
            else:
                guild_obj = None
        else:
            guild_obj = None

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data.get("email", ""),
                "bio": player_data.get("bio", ""),
                "race": race_obj,
                "guild": guild_obj
            }
        )


if __name__ == "__main__":
    main()
