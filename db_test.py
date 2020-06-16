from interface_db import orm_peewee_classes as data

# with data.connect() as db:
#     print(db.is_closed())
#     results = data.category.select()
#     for i in results:
        # print(i.name)
n = 20
while n < 40:
    url = f'www.test{n}.com'
    category = data.category(name='test', context='na', url=url, website_id=1)
    try:
        category.save()
        print('success')
    except Exception:
        pass
    n += 1