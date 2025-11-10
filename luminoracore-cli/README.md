# 🛠️ LuminoraCore CLI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/cli)
[![Status](https://img.shields.io/badge/status-v1.1_ready-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-28%2F28_passing-brightgreen.svg)](#)

**✅ PROFESSIONAL CLI TOOL - v1.1 PRODUCTION READY**

Professional command-line tool for AI personality management with LuminoraCore. Includes real API testing, interactive wizard, development server, memory management, and database migrations.

## Key Features

### Core Features (v1.1)
- **✅ Validate** - Validate personality files against official schema
- **✅ Compile** - Compile personalities to provider-specific prompts
- **✅ Create** - Create new personalities with interactive wizard
- **✅ Test** - Test personalities with real LLM providers (OpenAI, Claude, etc.)
- **✅ Blend** - Blend multiple personalities with custom weights
- **✅ Serve** - Local development server with web interface
- **✅ List** - List and browse available personalities
- **✅ Update** - Update personality cache from repository
- **✅ Real Testing** - Real connections to LLM APIs
- **✅ Web Interface** - Integrated UI for testing and management
- **✅ Error Handling** - Robust with automatic retries

### New in v1.1 - Memory & Database Tools
- **✅ Migrate** - Database migration management (up, down, status, list)
- **✅ Memory** - Query and manage facts, episodes, and affinity
- **✅ Snapshot** - Export/import session states and memories
- **✅ Feature Flags** - Configure v1.1 features dynamically

## Installation

```bash
pip install luminoracore-cli
```

## Quick Start

### v1.1 Commands
```bash
# Validate a personality file
luminoracore validate my_personality.json

# Compile for OpenAI
luminoracore compile dr_luna --model openai

# Start interactive testing
luminoracore test scientist --provider openai

# Create new personality
luminoracore create --interactive

# Start development server
luminoracore serve
```

### v1.1 Commands
```bash
# Check migration status
luminora-cli migrate --status

# Query facts
luminora-cli memory facts --session-id user_123

# Create snapshot
luminora-cli snapshot create --session-id user_123 --output backup.json

# Restore snapshot
luminora-cli snapshot restore --input backup.json --session-id new_user
```

## Commands

### v1.1 Commands

#### Migrate
Manage database migrations for v1.1 features:

```bash
# Check migration status
luminoracore migrate --status

# List all migrations
luminoracore migrate --list

# Apply migrations (up)
luminoracore migrate up

# Apply specific migration
luminoracore migrate up --target 003

# Rollback migrations (down)
luminoracore migrate down

# Dry-run (preview changes)
luminoracore migrate up --dry-run

# Force migration (skip checks)
luminoracore migrate up --force
```

#### Memory
Query and manage memory systems:

```bash
# Query facts for a session
luminoracore memory facts --session-id user_123

# Query facts by category
luminoracore memory facts --category preferences --limit 10

# Query episodes
luminoracore memory episodes --session-id user_123

# Query episodes by type
luminoracore memory episodes --type achievement --min-importance 0.8

# Check affinity level
luminoracore memory affinity --session-id user_123

# Export all memory data
luminoracore memory export --output memory_data.json
```

#### Snapshot
Export and import session states:

```bash
# Create snapshot of a session
luminoracore snapshot create --session-id user_123 --output snapshot.json

# Create snapshot with specific components
luminoracore snapshot create --session-id user_123 --include facts,episodes,affinity

# Restore snapshot
luminoracore snapshot restore --input snapshot.json --session-id user_456

# List snapshots
luminoracore snapshot list

# Compare snapshots
luminoracore snapshot diff snapshot1.json snapshot2.json
```

### v1.1 Commands

### Validate
Validate personality files against the LuminoraCore schema:

```bash
# Validate a single file
luminoracore validate personality.json

# Validate all files in a directory
luminoracore validate personalities/ --strict

# Output results to file
luminoracore validate *.json --format json --output results.json
```

### Compile
Compile personalities to provider-specific prompts:

```bash
# Compile for OpenAI
luminoracore compile dr_luna --provider openai --model gpt-3.5-turbo

# Compile for Anthropic
luminoracore compile scientist --provider anthropic --model claude-3-sonnet

# Save compiled prompt to file
luminoracore compile my_personality --output compiled_prompt.txt
```

### Create
Create new personalities with interactive wizard or templates:

```bash
# Interactive creation
luminoracore create --interactive

# From template
luminoracore create --template scientist --name "Dr. Smith"

# Non-interactive mode
luminoracore create --name "Assistant" --archetype "Helper" --output assistant.json
```

### Test
Test personalities interactively:

```bash
# Interactive testing
luminoracore test dr_luna --provider openai --interactive

# Quick test with sample message
luminoracore test scientist --provider anthropic --message "Explain quantum physics"
```

### Blend
Blend multiple personalities with custom weights:

```bash
# Blend two personalities
luminoracore blend dr_luna:0.6 captain_hook:0.4

# Interactive weight adjustment
luminoracore blend scientist:0.5 teacher:0.3 coach:0.2 --interactive

# Save blended personality
luminoracore blend personality1:0.7 personality2:0.3 --output blended.json
```

### Serve
Start development server with web interface:

```bash
# Start server on default port
luminoracore serve

# Custom port and host
luminoracore serve --port 3000 --host 0.0.0.0

# API only mode
luminoracore serve --api-only --cors
```

### List
List available personalities:

```bash
# List all personalities
luminoracore list

# List with details
luminoracore list --detailed

# Search personalities
luminoracore list --search "scientist"
```

### Update
Update personality cache from repository:

```bash
# Update all personalities
luminoracore update

# Update specific personality
luminoracore update dr_luna

# Force refresh
luminoracore update --force
```

### Init
Initialize new project:

```bash
# Initialize in current directory
luminoracore init

# Initialize with template
luminoracore init --template fastapi

# Initialize with custom name
luminoracore init --name "my-project"
```

### Info
Show personality information:

```bash
# Show personality details
luminoracore info dr_luna

# Show compilation info
luminoracore info scientist --provider openai

# Show validation info
luminoracore info my_personality --validate
```

## Configuration

Create a configuration file at `~/.luminoracore/config.yaml`:

```yaml
# Cache settings
cache_dir: ~/.luminoracore/cache
max_cache_size: 1073741824  # 1GB
cache_ttl: 86400  # 24 hours

# Repository settings
repository_url: https://api.luminoracore.com/v1
api_key: your-api-key-here
timeout: 30
max_retries: 3

# Validation settings
strict_validation: false
schema_url: null

# Compilation settings
default_provider: openai
default_model: gpt-3.5-turbo
include_metadata: true

# Server settings
default_port: 8000
default_host: 127.0.0.1
auto_reload: true

# UI settings
theme: default
color_output: true
progress_bars: true
table_style: default

# Logging settings
log_level: INFO
log_file: null
```

## Environment Variables

You can also configure the CLI using environment variables:

```bash
export LUMINORACORE_API_KEY="your-api-key"
export LUMINORACORE_DEFAULT_PROVIDER="openai"
export LUMINORACORE_CACHE_DIR="/path/to/cache"
export LUMINORACORE_STRICT_VALIDATION="true"
```

## Templates

The CLI includes several personality templates:

- `scientist` - Analytical and evidence-based
- `teacher` - Patient and educational
- `coach` - Motivational and supportive
- `assistant` - Helpful and efficient
- `creative` - Imaginative and artistic
- `custom` - Blank template for customization

## Development Server

The development server provides:

- **Web Interface**: Interactive personality testing and creation
- **API Endpoints**: RESTful API for programmatic access
- **WebSocket Support**: Real-time chat interface
- **Documentation**: Built-in API documentation

### API Endpoints

- `GET /api/personalities` - List personalities
- `GET /api/personalities/{id}` - Get personality details
- `POST /api/compile` - Compile personality to prompt
- `POST /api/validate` - Validate personality JSON
- `POST /api/blend` - Blend multiple personalities
- `WS /ws/chat` - WebSocket chat interface

## Examples

### Basic Workflow

```bash
# 1. Create a new personality
luminoracore create --interactive

# 2. Validate the personality
luminoracore validate my_personality.json

# 3. Test the personality
luminoracore test my_personality --provider openai --interactive

# 4. Compile for production
luminoracore compile my_personality --provider openai --output prompt.txt
```

### Advanced Workflow

```bash
# 1. Download personalities from repository
luminoracore update

# 2. Blend multiple personalities
luminoracore blend dr_luna:0.4 teacher:0.4 coach:0.2 --output hybrid.json

# 3. Validate blended personality
luminoracore validate hybrid.json --strict

# 4. Start development server
luminoracore serve --port 8080
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](https://docs.luminoracore.com/cli)
- 💬 [Discord Community](https://discord.gg/luminoracore)
- 🐛 [Issue Tracker](https://github.com/luminoracore/cli/issues)
- 📧 [Email Support](mailto:cli@luminoracore.com)
