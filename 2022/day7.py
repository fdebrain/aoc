import os

from aocd import get_data
from dotenv import load_dotenv

load_dotenv()


class File:
    def __init__(self, name, size, parent):
        self.name = name
        self.parent = parent
        self.size = size


class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.content = []

    def add_file_content(self, file_name, file_size):
        self.content.append(File(file_name, file_size, parent=self))

    def add_folder_content(self, folder_name):
        self.content.append(Folder(folder_name, parent=self))


class Disk:
    def __init__(self, root="/"):
        self.root = Folder(root)
        self.current_dir = self.root

    def populate_disk_tree(self, data):
        for line in data:
            if line.startswith("$"):
                command = line.split(" ")[1]
                if command != "cd":
                    continue  # ls

                target = line.split(" ")[2]

                if target == self.root.name:
                    continue
                elif target == "..":
                    self.current_dir = self.current_dir.parent
                    continue
                else:
                    new_dir = [d for d in self.current_dir.content if d.name == target]
                    self.current_dir = new_dir[0]
            elif line.startswith("dir"):
                folder_name = line.split(" ")[1]
                self.current_dir.add_folder_content(folder_name)
            else:
                file_size, file_name = line.split(" ")
                self.current_dir.add_file_content(file_name, int(file_size))

    def estimate_folder_size(self, folder):
        """Recursiverly estimate the size of the given folder."""
        return sum(
            item.size if isinstance(item, File) else self.estimate_folder_size(item)
            for item in folder.content
        )

    def bfs(self):
        """Explore each tree node in a breadth-first-search fashion.

        Each tree node correspond to a folder in the disk.
        """
        to_explore = [self.root]
        total_size = 0

        while to_explore:
            # Fetch next folder to explore
            exploring = to_explore.pop()

            # Estimate its size and add to total_size if less than 100_000
            size = self.estimate_folder_size(exploring)
            total_size += size if size < 100_000 else 0

            # Add children to list to explore
            to_explore.extend(
                item for item in exploring.content if isinstance(item, Folder)
            )
        return total_size

    def bfs2(self, to_free):
        to_explore = [self.root]
        smallest_dir_size = float("inf")

        while to_explore:
            # Fetch next folder to explore
            exploring = to_explore.pop()

            # Estimate its size and add to total_size if less than 100_000
            size = self.estimate_folder_size(exploring)

            if size < smallest_dir_size and size > to_free:
                smallest_dir_size = size

            # Add children to list to explore
            to_explore.extend(
                item for item in exploring.content if isinstance(item, Folder)
            )
        return smallest_dir_size


if __name__ == "__main__":
    session_id = os.getenv("SESSION_ID")
    data = get_data(day=7, year=2022, session=session_id)
    data = data.split("\n")

    # Part 1: Find all of the directories with a total size of at most 100000.
    # What is the sum of the total sizes of those directories?
    disk = Disk()
    disk.populate_disk_tree(data)
    print(disk.bfs())

    # Part 2: Find smallest directory that would free up enough space.
    # What is the total size of that directory?
    disk_size = disk.estimate_folder_size(disk.root)
    remaining_space = 70_000_000 - disk_size
    space_to_free = 30_000_000 - remaining_space
    print(disk.bfs2(space_to_free))
