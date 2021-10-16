from faker import Faker
fake = Faker()
def fake_products(cantidad):

    for id in range(1, cantidad+1):
        nombre = "Producto "+str(id)
        precio = float(fake.pydecimal(left_digits=3, right_digits=1,
                       positive=True, min_value=1, max_value=550))
        foto = ''
        canti =fake.random_int(min=1, max=79)
        productoTalla ="'{{1,2}}'"
        updated_at="now()"
        created_at='now()'
        marca = fake.random_int(min=1, max=2)
        print("INSERT INTO productos (nombre, precio, foto,cantidad,\"productoTalla\",updated_at,created_at,marca_id) VALUES ('%s', %s, '%s',%s, %s, %s,%s,%s);" % (
            nombre, precio,foto,canti,productoTalla,updated_at,created_at,marca))


fake_products(100)