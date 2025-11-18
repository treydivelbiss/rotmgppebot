import os

DUNGEONS = [
    "Pirate Cave", "Forest Maze", "Spider Den", "Forbidden Jungle", "The Hive",
    "Snake Pit", "Sprite World", "Cave of a Thousand Treasures", "Ancient Ruins", "Magic Woods", 
    "Candyland Hunting Grounds", "Undead Lair", "Puppet Master's Theatre", "Toxic Sewers", "Cursed Library", "Mad Lab","Abyss of Demons",
    "Manor of the Immortals", "Haunted Cemetery", "The Machine", "Davy Jones' Locker", "Ocean Trench", "The Crawling Depths", "Woodland Labyrinth",
    "Deadwater Docks", "Puppet Master's Encore", "Cnidarian Reef", "Parasite Chambers", "The Tavern", "Sulfurous Wetlands", "Mountain Temple", 
    "Lair of Draconis", "Tomb of the Ancients", "The Third Dimension", "Lair of Shaitan", "Secluded Thicket", "High Tech Terror", "Ice Citadel", "Moonlight Village",
    "The Nest", "Cultist Hideout", "Fungal Cavern", "Crystal Cavern", "Spectral Penitentiary", "Kogbold Steamworks", "Lost Halls", "The Void", "The Shatters",
    "Heroic Undead Lair", "Infernal Abyss of Demons", "Plagued Nest", "Advanced Kogbold Steamworks", 
    "Oryx's Castle", "Oryx's Chamber", "Wine Cellar", "Oryx's Sanctuary",
    "Malogia", "Untaris", "Katalund", "Forax",
    "Legacy Heroic Undead Lair", "Legacy Heroic Abyss of Demons",
    "Rainbow Road", "Santa's Workshop", "Ice Tomb", "Battle for the Nexus", "Stromwell's Rift I", "Stromwell's Rift II", "Stromwell's Rift III",
    "Belladonna's Garden", "Queen Bunny Chamber", "Mad God Mayhem", "The Trials of Cronus", "Hidden Interregnum", "Oryxmania", "White Snake Invasion"
]

BASE_DIR = "./dungeons"
os.makedirs(BASE_DIR, exist_ok=True)

for dungeon in DUNGEONS:
    # Convert dungeon name to a safe folder name
    # folder_name = dungeon.replace(" ", "_")
    folder_name = dungeon
    folder_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

print("Finished creating dungeon folders.")
