# helpdesk.py: datos de ejemplo de la tienda ficticia Tiendalia
import random
from pathlib import Path

DOCS = {
 "devoluciones": "Puedes devolver un producto en 30 días desde la entrega si está sin usar y en su embalaje original. Los productos personalizados no se devuelven. El reembolso llega al método de pago original en 5 a 7 días laborables tras recibir el paquete en el almacén.",
 "envios": "El envío estándar tarda de 2 a 4 días laborables en la península y de 5 a 8 en Canarias y Baleares. El envío exprés llega al día siguiente si el pedido se hace antes de las 14:00. Los pedidos superiores a 50 euros tienen envío estándar gratuito.",
 "facturas": "La factura está disponible en Mi cuenta, Pedidos, Descargar factura, en las 24 horas siguientes al envío. Para cambiar los datos fiscales hay que solicitarlo antes de que el pedido salga del almacén; después solo se puede emitir una factura rectificativa.",
 "pagos": "Aceptamos tarjeta, PayPal y transferencia. Si el pago con tarjeta falla, comprueba el límite de tu banco y que el 3D Secure esté activo. Las transferencias deben llegar en 3 días o el pedido se cancela automáticamente.",
 "cuenta": "Para restablecer la contraseña usa el enlace Olvidé mi contraseña; caduca en 30 minutos. Si tu cuenta se bloquea tras cinco intentos fallidos, se desbloquea sola en 15 minutos. Para borrar tu cuenta escribe a privacidad@tiendalia.example.",
 "garantia": "Todos los productos electrónicos tienen 3 años de garantía legal. Para usarla necesitas el número de pedido. Si el fallo aparece en los primeros 30 días, cambiamos el producto sin coste; después se repara o se sustituye según el caso.",
 "cupones": "Los cupones no se acumulan y no valen en productos rebajados. Cada cupón caduca en la fecha indicada y solo se puede usar una vez por cuenta. Si un cupón válido no funciona, envía una captura del carrito al soporte.",
 "seguimiento": "Recibirás un correo con el número de seguimiento cuando el pedido salga del almacén. El estado puede tardar hasta 12 horas en actualizarse. Si lleva más de 5 días sin movimiento, abrimos una incidencia con el transportista.",
 "incidencias": "Si el paquete llega dañado, haz fotos del paquete y del producto y escribe en las 48 horas siguientes a la entrega. Enviamos un recambio sin coste o reembolsamos, según prefieras.",
 "privacidad": "Guardamos tus datos de pedido 6 años por obligación fiscal. Puedes pedir acceso, rectificación o supresión escribiendo al delegado de protección de datos. No vendemos tus datos a terceros.",
}

_PLANTILLAS = {
 "facturacion": ["No me ha llegado la factura del pedido {n}", "Necesito cambiar el CIF de la factura del pedido {n}", "Me habéis cobrado dos veces el pedido {n}", "I was charged twice for order {n}, please refund one", "La factura del pedido {n} tiene un importe distinto al que pagué"],
 "envio": ["El pedido {n} lleva 6 días sin moverse en el seguimiento", "¿Cuándo llega mi pedido {n}? Dijeron 3 días", "Where is my order {n}? Tracking has not updated", "El transportista dice que entregó el pedido {n} pero no lo tengo", "Quiero cambiar la dirección de entrega del pedido {n}"],
 "devolucion": ["Quiero devolver el pedido {n}, no es lo que esperaba", "¿Cómo devuelvo un producto sin usar? Pedido {n}", "Han pasado 40 días, ¿puedo devolver el pedido {n}?", "I want a refund for order {n}", "Devolví el pedido {n} hace dos semanas y no me han reembolsado"],
 "tecnico": ["El producto del pedido {n} no enciende", "La pantalla del pedido {n} llegó rota", "Falla la batería a las dos semanas, pedido {n}", "My device from order {n} stopped working after the update", "¿Cómo uso la garantía del pedido {n}?"],
 "cuenta": ["No puedo iniciar sesión, mi cuenta está bloqueada", "No me llega el correo para restablecer la contraseña", "Quiero borrar mi cuenta y mis datos", "I can't log in, it says too many attempts", "Quiero cambiar el email de mi cuenta"],
}

def tickets(n=60, seed=7):
    rnd = random.Random(seed); cats = list(_PLANTILLAS); out = []
    for i in range(n):
        c = cats[i % len(cats)]
        text = rnd.choice(_PLANTILLAS[c]).format(n=rnd.randint(10000, 99999))
        out.append({"id": f"T{i+1:03d}", "text": text, "category": c})
    rnd.shuffle(out)
    return out

def orders(n=40, seed=11):
    rnd = random.Random(seed)
    return [{"id": 10000 + i * 37, "date": f"2026-{rnd.randint(9, 11):02d}-{rnd.randint(1, 28):02d}",
             "status": rnd.choice(["entregado", "enviado", "preparando", "devuelto"]),
             "total": round(rnd.uniform(9, 320), 2), "customer": f"C{rnd.randint(1, 12):02d}"} for i in range(n)]

def make_invoice(i, folder="facturas"):
    """Dibuja una factura PNG y devuelve (ruta, verdad_esperada)."""
    from PIL import Image, ImageDraw, ImageFont
    rnd = random.Random(100 + i)
    names = ["Auriculares", "Cable USB-C", "Raton", "Teclado", "Funda", "Cargador"]
    items = [(rnd.choice(names), rnd.randint(1, 3), round(rnd.uniform(5, 80), 2)) for _ in range(rnd.randint(2, 4))]
    total = round(sum(q * p for _, q, p in items), 2)
    try: font = ImageFont.load_default(size=22)
    except TypeError: font = ImageFont.load_default()
    img = Image.new("RGB", (900, 600), "white"); d = ImageDraw.Draw(img); y = 40
    d.text((40, y), f"TIENDALIA - Factura F-{2026000 + i}", fill="black", font=font); y += 50
    for n, q, p in items:
        d.text((40, y), f"{n:<14} {q} x {p:>7.2f} EUR", fill="black", font=font); y += 40
    d.text((40, y + 20), f"TOTAL: {total:.2f} EUR", fill="black", font=font)
    Path(folder).mkdir(exist_ok=True); path = f"{folder}/f{i:02d}.png"; img.save(path)
    truth = {"numero": f"F-{2026000 + i}", "total": total,
             "lineas": [{"concepto": n, "cantidad": q, "precio": p} for n, q, p in items]}
    return path, truth