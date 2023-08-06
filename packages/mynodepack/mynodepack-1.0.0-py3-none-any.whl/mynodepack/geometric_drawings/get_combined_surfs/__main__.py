
### third-party import
from pygame import Surface


OPTIONS = (
  'topleft',
  'topright',
  'bottomleft',
  'bottomright',
  'midleft',
  'midright',
  'midbottom',
  'midtop',
  'center',
)

def get_combined_surfs(
    surf_a: Surface,
    surf_b: Surface,
    pos_from_b:{'widget_name': 'option_menu', 'widget_kwargs': {'options': OPTIONS}, 'type':str} ='center',
    pos_to_a:{'widget_name': 'option_menu', 'widget_kwargs': {'options': OPTIONS}, 'type':str} ='center',
    offset_pos_by: 'python_literal' = (0, 0),
) -> [{'name': 'surface', 'type': Surface}]:
    """Return new surface by combining surfs a and b."""
    rect_a = surf_a.get_rect()
    rect_b = surf_b.get_rect()

    pos = getattr(rect_b, pos_from_b)
    setattr(rect_a, pos_to_a, pos)
    rect_a.move_ip(offset_pos_by)

    size = rect_a.union(rect_b).size

    surf = Surface(size).convert_alpha()
    surf.fill((0,)*4)

    surf.blit(surf_b, rect_b)
    surf.blit(surf_a, rect_a)

    return surf


main_callable = get_combined_surfs
