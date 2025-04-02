from fastapi import APIRouter
from fastapi.responses import UJSONResponse

from models import Item, ItemBase
from repositories import get_conn
from repositories.products import (add_product, delete_product,
                                   get_prods_to_buy, get_produduct_by_id,
                                   update_product)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def list_products():
    products = []
    conn = get_conn()
    items = get_prods_to_buy(conn)
    conn.close()

    for item_ in items:
        product = Item(
            item_id=item_[0],
            name=item_[1],
            is_done=item_[2],
            done_at=str(item_[3])
        )
        products.append(product.model_dump())

    return {"Produtos": products}


@router.get("/{product_id}")
async def get_product(product_id: int):
    conn = get_conn()
    product = get_produduct_by_id(conn, product_id)
    conn.close()

    if (not product):
        return {"erro": f"Produto {product_id} não encontrado"}

    product_item = Item(
        item_id=product[0],
        name=product[1],
        is_done=product[2],
        done_at=str(product[3])
    )

    return {"Produto": product_item}


@router.post("/")
async def add(name: str):
    conn = get_conn()
    product_name = add_product(conn, name)
    conn.close()

    return {'Adicionado': product_name}


@router.put("/{product_id}")
async def update(product_id: int, product: ItemBase):
    prod_to_update = Item(
        item_id=product_id,
        name=product.name,
        is_done=product.done_at != None,
        done_at=product.done_at
    )

    if prod_to_update.name.strip() == '' and prod_to_update.done_at == None:
        return UJSONResponse({'Erro': 'Atualize ao menos um atributo'}, 400)

    conn = get_conn()
    product_name = update_product(conn, prod_to_update)
    conn.close()

    return {'Atualizado': product_name}


@router.delete("/{product_id}")
async def delete(product_id: int):
    conn = get_conn()
    id = delete_product(conn, product_id)
    conn.close()

    return {'Excluído': id}
