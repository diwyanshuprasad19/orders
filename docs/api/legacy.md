# Orders — legacy aliases

Prefer `/v1/orders`.

## Legacy create

`POST /orders` · same `OrderCreate` · **201** body shape:
```json
{"order_id":"<uuid>","sku":"...","qty":1,"status":"confirmed"}
```
(not full `OrderOut`)

## Legacy get

`GET /orders/{order_id}` · `{"order_id","sku","qty","status"}` · **404** if missing
