
def wrapped_preprocessing_paths(startswith: list[str]):
    def is_include(path: str):
        for s in startswith:
            if path.startswith(s):
                return True
        else:
            return False

    def wrapper(endpoints):
        filtered = []
        for (path, path_regex, method, callback) in endpoints:
            if is_include(path=path):
                filtered.append((path, path_regex, method, callback))
        return filtered

    return wrapper
