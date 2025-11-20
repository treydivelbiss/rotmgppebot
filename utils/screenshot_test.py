

from find_items import find_items_in_image

# file_path = "./downloads/screenshot.png"
# file_path = "./downloads/merlot2.png"
file_path = "./downloads/doublewhite.png"
# dungeon = "Wine Cellar"
# dungeon = "Ice Citadel"
# dungeon = "Oryx's Chamber"
dungeon = "Oryx's Sanctuary"

found_items = find_items_in_image(file_path, templates_folder=f"./dungeons/{dungeon}")
if found_items:
    # player_name = str(interaction.user.display_name)
    # loot_results, total = await calculate_loot_points(interaction.guild.id, player_name, found_items)

    msg_lines = [f"`LogicVoid's` Loot Summary:"]
    for item in found_items:
        msg_lines.append(f"- {item['item']}")

    # print("\n".join(msg_lines))