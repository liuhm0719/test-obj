project_members: dict[str, set[int]] = {}
user_projects: dict[int, set[str]] = {}


def add_member(project_id: str, user_id: int) -> bool:
    if project_id not in project_members:
        project_members[project_id] = set()
    if user_id not in user_projects:
        user_projects[user_id] = set()

    if user_id in project_members[project_id]:
        return False

    project_members[project_id].add(user_id)
    user_projects[user_id].add(project_id)
    return True


def remove_member(project_id: str, user_id: int) -> bool:
    if project_id not in project_members or user_id not in project_members[project_id]:
        return False

    project_members[project_id].discard(user_id)
    user_projects.get(user_id, set()).discard(project_id)
    return True


def get_project_members(project_id: str) -> list[int]:
    return list(project_members.get(project_id, set()))


def get_user_projects(user_id: int) -> list[str]:
    return list(user_projects.get(user_id, set()))


def remove_all_project_members(project_id: str) -> None:
    members = project_members.pop(project_id, set())
    for uid in members:
        user_projects.get(uid, set()).discard(project_id)


def remove_user_from_all_projects(user_id: int) -> None:
    projects = user_projects.pop(user_id, set())
    for pid in projects:
        project_members.get(pid, set()).discard(user_id)
