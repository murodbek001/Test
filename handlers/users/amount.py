from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import cats_markup, numbers


@dp.message_handler(state=ShopState.amount)
async def get_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    product_name = data.get("product_name")
    product_price = data.get("product_price")
    amount = message.text
    if int(amount) > 0:
        amount = int(amount)
        user_id = message.from_user.id
        cart_id = db.select_cart(user_id=user_id)[0]
        products = db.check_product_exist(product_id=product_id,cart_id=cart_id)
        print(products)
        if products:
            last_quantity = products[2]
            print(last_quantity)
            db.cart_product_update(product_id=product_id, quantity=amount + last_quantity, cart_id=cart_id)

        else:
             db.add_cart_item(product_id=product_id, quantity=amount, cart_id=cart_id)
        await message.answer(f"<b>{product_name}</b>\n\n<code>{product_name} x {amount} = {product_price * amount} so'm</code>\n\n<b>Заказ добавлен!</b>\nВы можете проверить в:\n📥 Корзина", parse_mode="html", reply_markup=cats_markup)
        await ShopState.category.set()
    else:
        await message.answer("Miqdorni to'g'ri raqamlar bilan kiriting ☺️", reply_markup=numbers)