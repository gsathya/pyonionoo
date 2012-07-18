from pyonionoo.parser import Router


def get_routers(file_path):
    routers = []
    with open(file_path) as f:
    
        for line in f.readlines():
            router = Router(line)
            routers.append(router)

        return routers
