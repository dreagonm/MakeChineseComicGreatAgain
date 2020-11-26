def bullet_get(objs):
    bullet_dic = {}
    for obj in objs:
        message = {
            'bullet': obj.bullet,
            'typeface': obj.typeface,
            'color': obj.color,
            'type': obj.get_type_display(),
            'size': obj.size
        }
        bullet_dic['%s' % obj.id] = message
    return bullet_dic