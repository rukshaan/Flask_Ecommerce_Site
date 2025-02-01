from intasend import APIService


API_PUBLISHABLE_KEY='ISPubKey_test_4aaa7726-4542-4c38-a284-70afe13103fd'

API_TOKEN='ISSecretKey_test_da9dd0d3-ecfd-4d1f-8b9e-7cbadf6c3f7b'
try:
    service=APIService(token=API_TOKEN,test=True)
    create_order = service.collect.mpesa_stk_push(
        phone_number='0778901558',
        email='shaanruk0309@gmail.com',
        amount=100,
        narrative='Purchase of items'
    )

    print(create_order)
except Exception as e:
    print("Error:", e)


