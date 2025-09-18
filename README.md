# 🐉 Simple D&D AI Dungeon Master - Lost Mine of Phandelver

An interactive Dungeons & Dragons solo adventure powered by AI, featuring the classic "Lost Mine of Phandelver" campaign. This Streamlit application serves as your personal AI Dungeon Master, managing character sheets, dice rolling, inventory, and immersive storytelling.

## ✨ Features

### 🎮 Core Gameplay
- **AI Dungeon Master**: Powered by OpenRouter API with intelligent story narration
- **Solo Campaign**: Complete "Lost Mine of Phandelver" adventure for single players
- **Interactive Chat**: Real-time conversation with your AI DM
- **Persistent Story**: Chat history saved across sessions

### 📋 Character Management
- **Complete Character Sheet**: Name, race, class, level, and stats
- **Health Tracking**: Current HP, Max HP, and Temporary HP monitoring
- **Ability Scores**: Six core D&D stats (STR, DEX, CON, INT, WIS, CHA)
- **Point-Buy System**: Balanced character creation with 75-point limit
- **Auto-Save**: Character data persisted to database

### 🎒 Inventory System
- **Equipment Tracking**: Current armor and weapons
- **Item Management**: Add, remove, and track quantities
- **Currency System**: Gold and silver coin tracking
- **Smart Inventory**: Automatic item stacking and management

### 🎲 Dice Rolling
- **Multi-Die Support**: Roll multiple dice types simultaneously
- **Standard D&D Dice**: d3, d4, d6, d8, d10, d12, d20
- **Roll History**: Last roll result displayed
- **Manual Integration**: Tell the AI your roll results for authentic gameplay

### 💾 Data Management
- **SQLite Database**: Reliable local data storage
- **Chat History**: Complete conversation preservation
- **Character Persistence**: Automatic character sheet saving
- **Reset Functionality**: Clean slate for new adventures

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd dnd-ai-dm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

4. **Get your OpenRouter API Key**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Create an account and generate an API key
   - Add the key to your `.env` file

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

### Setting Up Your Character

1. **Basic Information**
   - Enter your character's name, race, and class
   - Set your character level (starting at 1)
   - Input Armor Class (AC)

2. **Health Points**
   - Set Current HP, Max HP, and Temporary HP
   - Values will be tracked throughout your adventure

3. **Ability Scores**
   - Distribute points across six abilities: STR, DEX, CON, INT, WIS, CHA
   - Each stat ranges from 8-16
   - Total points cannot exceed 75

4. **Equipment & Inventory**
   - Set your current armor and weapon
   - Add items to your inventory with quantities
   - Track gold and silver coins

### Playing the Game

1. **Start Adventure**: Click "🚀 Mulai Petualangan" to begin
2. **Interact with AI DM**: Type your actions in the chat input
3. **Roll Dice**: Use the sidebar dice roller for skill checks and combat
4. **Manage Character**: Update HP, inventory, and equipment as needed
5. **Save Progress**: Your character and chat history auto-save

### Dice Rolling System

- Select dice types (d3 to d20)
- Choose number of dice to roll
- Roll results appear in sidebar
- Share results with AI DM for authentic gameplay

## 🏗️ Project Structure

```
dnd-ai-dm/
├── app.py                 # Main Streamlit application
├── db.py                  # Database operations (SQLite)
├── openrouter_client.py   # OpenRouter API integration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── chat_history.db        # SQLite database (auto-created)
└── README.md              # Project documentation
```

## 🔧 Configuration

### Supported AI Models
The application uses Google's Gemini 2.5 Flash model by default. You can modify the model in `openrouter_client.py`:

```python
payload = {
    "model": "google/gemini-2.5-flash-image-preview:free",  # Change this line
    "messages": messages
}
```

### Database Schema

**Chat Table**
- `id`: Primary key
- `role`: Message sender (user/assistant/system)
- `content`: Message content
- `created_at`: Timestamp

**Character Table**
- `id`: Primary key
- Character stats and equipment data
- `created_at`: Timestamp

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **SQLite**: Local database storage
- **OpenRouter**: AI model API gateway
- **Python-dotenv**: Environment variable management

### Key Features
- Responsive web interface
- Real-time AI chat integration
- Persistent data storage
- Dice rolling simulation
- Character sheet validation

## 🎲 Gameplay Features

### Combat System
- Track HP changes during combat
- Roll damage and healing dice
- Manage temporary hit points
- Equipment-based AC calculation

### Inventory Management
- Dynamic item addition/removal
- Quantity tracking
- Currency management
- Equipment state tracking

### Story Progression
- AI-driven narrative
- Player choice consequences
- Character development
- Campaign milestone tracking

## 🚨 Troubleshooting

### Common Issues

**API Key Errors**
- Ensure `.env` file exists with correct API key
- Check OpenRouter account has sufficient credits
- Verify API key permissions

**Database Issues**
- Database file auto-creates on first run
- Delete `chat_history.db` to reset all data
- Check file permissions in project directory

**Streamlit Errors**
- Update Streamlit: `pip install --upgrade streamlit`
- Check Python version compatibility
- Restart application after code changes

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Happy Adventuring! 🗡️✨**

*May your rolls be high and your adventures legendary!*
