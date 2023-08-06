import os
from hestia_earth.earth_engine import init_gee
from hestia_earth.earth_engine.coordinates import run
from hestia_earth.earth_engine.gee_utils import load_region, load_geometry, area_km2


ENABLED = os.environ.get('VALIDATE_SPATIAL', 'true') == 'true'
gee_init = False


def init_gee_by_nodes(nodes: list):
    should_init = any([n.get('@type', n.get('type')) in ['Site', 'Organisation'] for n in nodes])
    return init_gee() if should_init and ENABLED else None


def is_enabled(): return ENABLED


def id_to_level(id: str): return id.count('.')


def fetch_data(**kwargs):
    return run(kwargs).get('features', [])[0].get('properties')


def get_region_id(gid: str, **kwargs):
    try:
        level = id_to_level(gid)
        field = f"GID_{level}"
        id = fetch_data(collection=f"users/hestiaplatform/gadm36_{level}",
                        ee_type='vector',
                        fields=field,
                        **kwargs
                        ).get(field)
        return None if id is None else f"GADM-{id}"
    except Exception:
        return None


def get_region_size(gid: str):
    return area_km2(load_region(gid).geometry()).getInfo()


def get_boundary_size(boundary: dict):
    return area_km2(load_geometry(boundary)).getInfo()
