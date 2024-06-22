import asyncio

from telegram import Update
import logging
from telegram.constants import ChatAction
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from db import save_file, search_files

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Welcome {update.effective_user.first_name} to my bot! I can help you with various tasks. Type /help to see the list of available commands.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Available commands: /start, /help, /contact, /search <keyword>')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('You can contact me through this bot or email me at [your email]')

async def save_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.document:
        document = update.message.document
        file_id = document.file_id
        file_name = document.file_name
        file_keywords = file_name.split()  # Example of extracting keywords from the file name
        
        # Check if the file with the same file_id already exists in the database
        existing_files = search_files(file_id)
        file_count = sum(1 for _ in existing_files)
        
        if file_count == 0:  # Check if no documents found
            save_file(file_id, file_name, file_keywords)
            await update.message.reply_text(f'File {file_name} saved with id: {file_id}')
            
            # Send notification message to the group
            chat_id = update.message.chat_id
            notification_message = 'This file will be removed after 1 minute.'
            await context.bot.send_message(chat_id, notification_message)
            
            # Schedule the file deletion after 1 minute
            await schedule_file_deletion(chat_id, file_id, context.bot)
        else:
            await update.message.reply_text('This file has already been uploaded.')

async def schedule_file_deletion(chat_id, document_message_id, deletion_message_id, context: ContextTypes.DEFAULT_TYPE):
    # Sleep for 1 minute
    await asyncio.sleep(60)
    try:
        # Delete the document message
        await context.bot.delete_message(chat_id, document_message_id)
        
        # Delete the deletion message
        await context.bot.delete_message(chat_id, deletion_message_id)
    except BadRequest as e:
        print(f"Failed to delete message in chat {chat_id}: {e}")
    


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)  # Get the query from the command arguments
    if query:
        results = search_files(query)
        count = sum(1 for _ in results)  # Count the number of documents returned by the cursor
        results.rewind()  # Rewind the cursor to iterate over it again
        if count > 0:
            for item in results:
                message = await update.message.reply_document(document=item['file_id'], caption=f'Found: {item["file_name"]}')
                # Schedule the file deletion
                asyncio.create_task(schedule_file_deletion(update.message.chat_id, message.message_id, context.bot))
        else:
            await update.message.reply_text(f'No files found for query: {query}')
    else:
        await update.message.reply_text('Please provide a search keyword. Usage: /search <keyword>')


async def search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    
    # Send a "searching" message
    searching_message = await update.message.reply_text("Searching...")

    try:
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        
        # Simulate a delay for searching (for testing purposes)
        await asyncio.sleep(2)
        
        results = search_files(query)
        
        if results:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=searching_message.message_id)
            for item in results:
                await send_file_and_schedule_deletion(update.message, item)
        else:
            await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=searching_message.message_id, text=f'No files found for query: {query}')
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=searching_message.message_id, text=f"An error occurred: {e}")

async def send_file_and_schedule_deletion(message, file_info):
    document_message = await message.reply_document(document=file_info['file_id'], caption=f'Found: {file_info["file_name"]}')
    deletion_message = await message.reply_text("This file will be deleted after 1 minute.")
    await schedule_file_deletion(message.chat_id, document_message.message_id, message.bot, deletion_message.message_id)



# async def search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.message.text
#     await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

#     # Simulate a delay for searching (for testing purposes)
#     await asyncio.sleep(2)

#     results = search_files(query)

    
#     if results:
#         for item in results:
#             await update.message.reply_document(document=item['file_id'], caption=f'Found: {item["file_name"]}')
#     else:
#         await update.message.reply_text(f'No files found for query: {query}')


