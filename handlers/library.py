"""
Library system handler
Handles book categories, browsing, searching, downloading, and favorites
"""

import logging
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.db import Database
from states.forms import LibraryStates
from utils.helpers import t
from keyboards.reply import get_main_keyboard

logger = logging.getLogger(__name__)
db = Database()


# ==================== HELPER FUNCTIONS ====================

def get_library_categories_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create 3x3 grid inline keyboard for library categories"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    categories = db.get_all_library_categories(lang)

    buttons = []
    for category in categories:
        # category: (id, name, emoji, book_count)
        cat_id = category[0]
        name = category[1]
        emoji = category[2]
        count = category[3]

        button_text = f"{emoji} {name}\n({count} kitob)"
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=f"lib_cat_{cat_id}"
        ))

    # Add buttons in rows of 3
    for i in range(0, len(buttons), 3):
        keyboard.row(*buttons[i:i+3])

    # Add featured books button
    keyboard.add(InlineKeyboardButton(
        text="🌟 Tavsiya etiladigan kitoblar",
        callback_data="lib_featured"
    ))

    # Add favorites button
    keyboard.add(InlineKeyboardButton(
        text="⭐ Sevimli kitoblar",
        callback_data="lib_favorites"
    ))

    return keyboard


def format_book_list(books: list, page: int, total_count: int, lang: str = 'uz') -> str:
    """Format books list for display"""
    if not books:
        return t(0, 'library_no_search_results')  # Using user_id=0 as fallback

    text = ""
    emojis = ['📕', '📗', '📘', '📙']  # Rotate through different book emojis

    offset = (page - 1) * 15
    for idx, book in enumerate(books, start=1):
        # book: (id, title, author, year, file_id, download_count)
        book_id = book[0]
        title = book[1]
        author = book[2] if book[2] else "Noma'lum"
        year = book[3] if book[3] else ""

        emoji = emojis[(offset + idx - 1) % len(emojis)]

        text += f"/{book_id}  {emoji} {title} - {author}"
        if year:
            text += f" ({year})"
        text += "\n"

    text += f"\n📄 Sahifa {page} / {(total_count + 14) // 15}\n\n"

    # Add navigation hints
    if page > 1:
        text += "📄 Oldingi 15 ta: /prev\n"
    if page * 15 < total_count:
        text += "📄 Keyingi 15 ta: /next\n"

    text += "\n🔍 Qidirish: Kitob yoki muallif nomini yozing\n"
    text += "🔙 Orqaga: /back"

    return text


# ==================== MAIN HANDLERS ====================

async def library_menu(message: Message, state: FSMContext):
    """Show library main menu with categories"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    await state.finish()  # Clear any previous state
    await LibraryStates.choosing_category.set()

    keyboard = get_library_categories_keyboard(lang)

    await message.answer(
        t(user_id, 'library_title'),
        reply_markup=keyboard
    )


async def category_selected(callback: CallbackQuery, state: FSMContext):
    """Handle category selection"""
    user_id = callback.from_user.id
    lang = db.get_user_language(user_id)

    # Extract category ID from callback data: lib_cat_1
    category_id = int(callback.data.split('_')[-1])

    # Get category info
    category = db.get_library_category(category_id)
    if not category:
        await callback.answer("❌ Kategoriya topilmadi", show_alert=True)
        return

    # Save to state
    await state.update_data(
        current_category=category_id,
        current_page=1,
        category_name=category[1] if lang == 'uz' else category[2] if lang == 'ru' else category[3]
    )
    await LibraryStates.browsing_books.set()

    # Get books for this category
    books = db.get_books_by_category(category_id, limit=15, offset=0, lang=lang)
    total_count = db.get_books_count_by_category(category_id)

    if not books:
        await callback.message.edit_text(
            f"📚 {category[1]}\n\n❌ Bu kategoriyada hozircha kitoblar yo'q"
        )
        return

    # Format and display book list
    category_name = category[1] if lang == 'uz' else category[2] if lang == 'ru' else category[3]
    text = f"📚 {category_name} ({total_count} kitob)\n\nKerakli kitob raqamini yozing:\n\n"
    text += format_book_list(books, 1, total_count, lang)

    await callback.message.edit_text(text)
    await callback.answer()


async def handle_book_request(message: Message, state: FSMContext):
    """Handle book number request (e.g., /1, /2, etc.)"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    current_state = await state.get_state()
    if current_state not in [LibraryStates.browsing_books.state, LibraryStates.searching_books.state]:
        return

    # Extract book ID from command
    try:
        book_id = int(message.text.strip('/'))
    except ValueError:
        return

    # Get book from database
    book = db.get_book(book_id)
    if not book:
        await message.answer(t(user_id, 'library_book_not_found'))
        return

    # Send "downloading" message
    loading_msg = await message.answer(t(user_id, 'library_book_downloading'))

    # book structure: (id, category_id, title_uz, title_ru, title_en, author, year, pages,
    #                  language, description, file_id, channel_message_id, download_count, is_featured, created_at)

    title = book[2] if lang == 'uz' else book[3] if lang == 'ru' else book[4]
    author = book[5] if book[5] else "Noma'lum"
    year = book[6] if book[6] else "N/A"
    pages = book[7] if book[7] else "N/A"
    book_lang = book[8] if book[8] else "N/A"
    description = book[9] if book[9] else ""
    file_id = book[10]

    # Get category name
    category = db.get_library_category(book[1])
    category_name = category[1] if category else "N/A"

    # Format book details
    book_details = t(user_id, 'library_book_details').format(
        title=title,
        author=author,
        year=year,
        pages=pages,
        category=category_name,
        language=book_lang,
        description=description if description else ""
    )

    try:
        # Send PDF file
        if file_id:
            await message.answer_document(
                document=file_id,
                caption=book_details
            )
        else:
            await message.answer("❌ Kitob fayli topilmadi")
            await loading_msg.delete()
            return

        # Delete loading message
        await loading_msg.delete()

        # Increment download counter
        db.increment_book_download(book_id, user_id)

        # Send additional info
        next_book = book_id + 1
        await message.answer(
            t(user_id, 'library_book_sent').format(next=next_book),
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(
                    text=f"⭐ Sevimlilar",
                    callback_data=f"lib_fav_{book_id}"
                ),
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data="lib_back_to_category"
                )
            )
        )

    except Exception as e:
        logger.error(f"Error sending book {book_id}: {e}")
        await loading_msg.delete()
        await message.answer("❌ Kitobni yuborishda xatolik yuz berdi")


async def handle_pagination(message: Message, state: FSMContext):
    """Handle /next and /prev pagination"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    current_state = await state.get_state()
    if current_state != LibraryStates.browsing_books.state:
        return

    data = await state.get_data()
    current_page = data.get('current_page', 1)
    category_id = data.get('current_category')
    category_name = data.get('category_name', 'Kategoriya')

    if not category_id:
        return

    # Determine new page
    if message.text == '/next':
        new_page = current_page + 1
    elif message.text == '/prev':
        new_page = max(1, current_page - 1)
    else:
        return

    # Get books for new page
    offset = (new_page - 1) * 15
    books = db.get_books_by_category(category_id, limit=15, offset=offset, lang=lang)
    total_count = db.get_books_count_by_category(category_id)

    if not books:
        await message.answer("❌ Bu sahifada kitoblar yo'q")
        return

    # Update state
    await state.update_data(current_page=new_page)

    # Format and display
    text = f"📚 {category_name} ({total_count} kitob)\n\nKerakli kitob raqamini yozing:\n\n"
    text += format_book_list(books, new_page, total_count, lang)

    await message.answer(text)


async def handle_back(message: Message, state: FSMContext):
    """Handle /back command"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    current_state = await state.get_state()

    if current_state in [LibraryStates.browsing_books.state, LibraryStates.searching_books.state]:
        # Go back to categories
        await state.finish()
        await LibraryStates.choosing_category.set()

        keyboard = get_library_categories_keyboard(lang)
        await message.answer(
            t(user_id, 'library_title'),
            reply_markup=keyboard
        )


async def handle_search(message: Message, state: FSMContext):
    """Handle book search"""
    user_id = message.from_user.id
    lang = db.get_user_language(user_id)

    current_state = await state.get_state()
    if current_state != LibraryStates.browsing_books.state:
        return

    query = message.text.strip()
    if len(query) < 2:
        await message.answer("❌ Qidiruv uchun kamida 2 ta belgi kiriting")
        return

    data = await state.get_data()
    category_id = data.get('current_category')

    # Search books
    books = db.search_books(query, category_id, lang)

    if not books:
        await message.answer(t(user_id, 'library_no_search_results'))
        return

    await LibraryStates.searching_books.set()

    text = t(user_id, 'library_search_results').format(query=query)

    emojis = ['📕', '📗', '📘', '📙']
    for idx, book in enumerate(books, start=1):
        book_id = book[0]
        title = book[1]
        author = book[2] if book[2] else "Noma'lum"
        year = book[3] if book[3] else ""

        emoji = emojis[(idx - 1) % len(emojis)]

        text += f"/{book_id}  {emoji} {title} - {author}"
        if year:
            text += f" ({year})"
        text += "\n"

    text += "\n🔙 Orqaga: /back"

    await message.answer(text)


async def handle_favorites_toggle(callback: CallbackQuery, state: FSMContext):
    """Toggle book favorite status"""
    user_id = callback.from_user.id

    # Extract book ID from callback: lib_fav_123
    book_id = int(callback.data.split('_')[-1])

    # Toggle favorite
    added = db.toggle_favorite_book(book_id, user_id)

    if added:
        await callback.answer(t(user_id, 'library_favorite_added'), show_alert=True)
    else:
        await callback.answer(t(user_id, 'library_favorite_removed'), show_alert=True)


async def show_favorites(callback: CallbackQuery, state: FSMContext):
    """Show user's favorite books"""
    user_id = callback.from_user.id
    lang = db.get_user_language(user_id)

    favorites = db.get_user_favorites(user_id, lang)

    if not favorites:
        await callback.answer(t(user_id, 'library_no_favorites'), show_alert=True)
        return

    text = f"⭐ {t(user_id, 'library_favorites')}\n\n"

    emojis = ['📕', '📗', '📘', '📙']
    for idx, book in enumerate(favorites, start=1):
        book_id = book[0]
        title = book[1]
        author = book[2] if book[2] else "Noma'lum"
        year = book[3] if book[3] else ""

        emoji = emojis[(idx - 1) % len(emojis)]

        text += f"/{book_id}  {emoji} {title} - {author}"
        if year:
            text += f" ({year})"
        text += "\n"

    text += "\n🔙 Orqaga: /back"

    await LibraryStates.browsing_books.set()
    await callback.message.edit_text(text)
    await callback.answer()


async def show_featured(callback: CallbackQuery, state: FSMContext):
    """Show featured/recommended books"""
    user_id = callback.from_user.id
    lang = db.get_user_language(user_id)

    featured = db.get_featured_books(lang, limit=20)

    if not featured:
        await callback.answer("❌ Tavsiya etiladigan kitoblar yo'q", show_alert=True)
        return

    text = f"🌟 {t(user_id, 'library_featured')}\n\n"

    emojis = ['📕', '📗', '📘', '📙']
    for idx, book in enumerate(featured, start=1):
        book_id = book[0]
        title = book[1]
        author = book[2] if book[2] else "Noma'lum"
        year = book[3] if book[3] else ""

        emoji = emojis[(idx - 1) % len(emojis)]

        text += f"/{book_id}  {emoji} {title} - {author}"
        if year:
            text += f" ({year})"
        text += "\n"

    text += "\n🔙 Orqaga: /back"

    await LibraryStates.browsing_books.set()
    await callback.message.edit_text(text)
    await callback.answer()


async def back_to_category(callback: CallbackQuery, state: FSMContext):
    """Go back to category book list"""
    user_id = callback.from_user.id
    lang = db.get_user_language(user_id)

    data = await state.get_data()
    category_id = data.get('current_category')
    category_name = data.get('category_name', 'Kategoriya')

    if not category_id:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
        return

    # Get books for this category
    books = db.get_books_by_category(category_id, limit=15, offset=0, lang=lang)
    total_count = db.get_books_count_by_category(category_id)

    await state.update_data(current_page=1)
    await LibraryStates.browsing_books.set()

    # Format and display book list
    text = f"📚 {category_name} ({total_count} kitob)\n\nKerakli kitob raqamini yozing:\n\n"
    text += format_book_list(books, 1, total_count, lang)

    await callback.message.edit_text(text)
    await callback.answer()


# ==================== REGISTRATION ====================

def register_library_handlers(dp: Dispatcher):
    """Register all library-related handlers"""

    # NOTE: Main library menu is now accessed through Students menu
    # No direct handler from main menu needed

    # Category selection
    dp.register_callback_query_handler(
        category_selected,
        lambda c: c.data.startswith('lib_cat_'),
        state=LibraryStates.choosing_category
    )

    # Book request (e.g., /1, /2, etc.)
    dp.register_message_handler(
        handle_book_request,
        lambda msg: msg.text and msg.text.startswith('/') and msg.text[1:].isdigit(),
        state=[LibraryStates.browsing_books, LibraryStates.searching_books]
    )

    # Pagination
    dp.register_message_handler(
        handle_pagination,
        Text(equals=['/next', '/prev']),
        state=LibraryStates.browsing_books
    )

    # Back button
    dp.register_message_handler(
        handle_back,
        Text(equals='/back'),
        state=[LibraryStates.browsing_books, LibraryStates.searching_books]
    )

    # Search
    dp.register_message_handler(
        handle_search,
        lambda msg: msg.text and not msg.text.startswith('/'),
        state=LibraryStates.browsing_books
    )

    # Favorites toggle
    dp.register_callback_query_handler(
        handle_favorites_toggle,
        lambda c: c.data.startswith('lib_fav_'),
        state='*'
    )

    # Show favorites
    dp.register_callback_query_handler(
        show_favorites,
        lambda c: c.data == 'lib_favorites',
        state=LibraryStates.choosing_category
    )

    # Show featured books
    dp.register_callback_query_handler(
        show_featured,
        lambda c: c.data == 'lib_featured',
        state=LibraryStates.choosing_category
    )

    # Back to category
    dp.register_callback_query_handler(
        back_to_category,
        lambda c: c.data == 'lib_back_to_category',
        state='*'
    )

    logger.info('✅ Library handlers registered')
