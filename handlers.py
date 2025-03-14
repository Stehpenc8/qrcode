from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router,F
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
import qrcode
from aiogram.types import BufferedInputFile
import io
import app.keyboard as kb
from aiogram import Bot

router = Router()
bot = Bot(token='7381846033:AAGJLEvyAaLeaPMIK0a_Xi5ntAK6-vrRyAo')

class QR(StatesGroup):
    text = State()
    image = State()

#start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello', reply_markup=kb.main)

#reply to keyboard
@router.message(F.text=='генерация qr кода по тексту')
async def text_handler(message: Message, state: FSMContext):
    await state.set_state(QR.text)
    await message.answer('Напишите текст, который хотите закодировать')

@router.message(F.text=='генерация qr кода по изображению')
async def image_handler(message: Message, state: FSMContext):
    await state.set_state(QR.image)
    await message.answer('Пришлите изображение, которое хотите закодировать')

#collect data 
@router.message(QR.text)
async def QR_text(message: Message, state: FSMContext):
    try:
        await state.update_data(text_QR=message.text)
        data = await state.get_data()
        text = data['text_QR']
        if len(text) > 1000:
                await message.answer("❌ Текст слишком длинный (максимум 1000 символов)")
                return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Генерируем изображение
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Сохраняем в буфер памяти
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        
        # Отправляем пользователю
        await message.answer_photo(
            BufferedInputFile(buf.read(), filename="qrcode.png"),
            caption="QR-код для вашего текста: "
        )
        await state.clear()
    except:
        await message.answer('Это не текст, пришлите текст или выберите другую генерацию...')


@router.message(QR.image)
async def QR_image(message: Message, state: FSMContext):
    try:
        await state.update_data(image_QR=message.photo[-1])

        data = await state.get_data()
        file_id = (data['image_QR']).file_id

        file = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"


        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(file_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Сохраняем QR-код в байтовый поток
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Отправляем QR-код пользователю
        await message.answer_photo(
            photo=BufferedInputFile(img_byte_arr.getvalue(), filename="qr_code.png"),
            caption="QR-код для вашего файла:"
        )
        await state.clear()
    except:
        await message.answer('Это не изображение, пришлите мне изображение или выберите другую генерацию...')