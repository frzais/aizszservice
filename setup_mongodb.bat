@echo off
echo ========================================
echo Ultroid MongoDB Setup Script
echo ========================================

echo.
echo 1. Installing MongoDB dependencies...
pip install pymongo[srv]

echo.
echo 2. Testing MongoDB connection...
python test_mongodb.py

echo.
echo 3. Creating .env file...
echo MONGO_URI=mongodb+srv://mandar309:mandar309@frz.6gibfsm.mongodb.net/?retryWrites=true^&w=majority^&appName=frz > .env
echo API_ID=your_api_id_here >> .env
echo API_HASH=your_api_hash_here >> .env
echo SESSION=your_session_string_here >> .env
echo BOT_TOKEN=your_bot_token_here >> .env
echo LOG_CHANNEL=0 >> .env
echo ADDONS=False >> .env
echo VCBOT=False >> .env

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API credentials
echo 2. Generate session string
echo 3. Run: python -m pyUltroid
echo.
pause
