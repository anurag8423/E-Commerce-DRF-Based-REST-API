from django.core.cache import cache

def invalidate_product_cache(product_id=None):
    keys_patterns = [
        'product_list*',
        'category_list*',
        'product_detail*'
    ]
    if product_id:
        keys_patterns.append(f'product_{product_id}_*')
    
    for key_pattern in keys_patterns:
        keys = cache.keys(key_pattern)
        if keys:
            cache.delete_many(keys)