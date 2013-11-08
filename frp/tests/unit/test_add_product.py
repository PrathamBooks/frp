from frp import app, models, lastuser

def test_add_product(test_db, test_client, last_user):
    "Adding a product to the database"
    app.lastuser_auth_data = dict(
        token_scope = u'name email',
        userid = u'1', 
        username = u'alokk', 
        email = u'kuchlous@gmail.com', 
        fullname = u'Alok Kuchlous'
        )
    app.lastuser_auth_token = dict(
        access_token = u'pAfGGWHzRtqRmdSQ_CdrWA',
        token_type = u'bearer',
        scope = u'email id')

    op = test_client.get("/product/add")
    print op.data
