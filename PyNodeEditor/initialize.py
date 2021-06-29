import os
from core.constants import APP_CONFIG_PATH, USER_CONFIG_PATH
from core.nodeLogger import get_node_logger

logger = get_node_logger(__file__)


def init_app():
    categories = get_all_nodes_from_app_config()
    print(categories)


def get_all_nodes_from_app_config():
    app_node_dir = os.path.join(APP_CONFIG_PATH, "nodes")
    node_categories = [x for x in os.listdir(app_node_dir) if os.path.isdir(os.path.join(app_node_dir, x))]


if __name__ == '__main__':
    init_app()
