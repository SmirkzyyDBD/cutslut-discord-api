# Discord API Bot Documentation

This documentation outlines the usage, structure, and features of the Cutslut Discord API bot. The bot tracks user status, activity, and profile information for [bio link webapp](https://cutslut.app) and integrates Flask for API handling and Discord.py for server interaction.

---

## Overview

The bot serves as a bridge between Discord and an external website, providing API endpoints that allow querying of user statuses and other data by user ID. The bot features role automation, health checks, and version tracking, alongside user-specific data retrieval.

---

## Prerequisites

- Python 3.11.5+
- Discord bot token
- API key for secure access
- Libraries listed in `requirements.txt`
- Properly configured environment variables in a `.env` file

### **Required Libraries**

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```
API_VERSION=1.0.0
BOT_TOKEN=your_actual_discord_bot_token
API_KEY=your_secure_api_key
GUILD_ID=your_discord_server_id
WELCOME_WEBHOOK=webhook_link
LOGS_WEBHOOK=logs_webhook_link
API_HEALTH=health_check_api_route
WEBSITE_URL=base_website_url
USER_ROLE=user_role_id
```

- **API_VERSION**: Version of the bot’s API.
- **BOT_TOKEN**: Token for the Discord bot.
- **API_KEY**: Secure key for API requests.
- **GUILD_ID**: Discord server ID.
- **WELCOME_WEBHOOK**: Webhook for welcome messages.
- **LOGS_WEBHOOK**: Webhook for logging important events.
- **API_HEALTH**: URL to check API health.
- **WEBSITE_URL**: URL of the associated website.
- **USER_ROLE**: Role ID to assign to new members.

---

## API Endpoints

### **GET /api/v1/version**

Returns the current API version.

#### **Headers**

| Header        | Type   | Description                |
| ------------- | ------ | -------------------------- |
| Authorization | string | API key for authentication |

#### **Example Request (CURL)**

```bash
curl -H "Authorization: your_secure_api_key" "http://localhost:80/api/v1/version"
```

#### **Example Request (TypeScript)**

```typescript
const fetch = require("node-fetch");

async function getVersion() {
  const response = await fetch("http://localhost:80/api/v1/version", {
    method: "GET",
    headers: {
      Authorization: "your_secure_api_key",
    },
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  const data = await response.json();
  console.log(data);
}
getVersion();
```

#### **Response**

```json
{
  "version": "1.0.0"
}
```

---

### **GET /api/v1/healthcheck**

Performs a health check.

#### **Headers**

| Header        | Type   | Description                |
| ------------- | ------ | -------------------------- |
| Authorization | string | API key for authentication |

#### **Example Request (CURL)**

```bash
curl -H "Authorization: your_secure_api_key" "http://localhost:80/api/v1/healthcheck"
```

#### **Example Request (TypeScript)**

```typescript
const fetch = require("node-fetch");

async function healthCheck() {
  const response = await fetch("http://localhost:80/api/v1/healthcheck", {
    method: "GET",
    headers: {
      Authorization: "your_secure_api_key",
    },
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  const data = await response.json();
  console.log(data);
}
healthCheck();
```

#### **Response**

```json
{
  "health": "Alive"
}
```

---

### **GET /api/v1/userStatus**

Retrieves status and activity details for a specific Discord user.

#### **URL Parameters**

| Parameter | Type   | Description                  |
| --------- | ------ | ---------------------------- |
| user_id   | string | The Discord user ID to query |

#### **Headers**

| Header        | Type   | Description                |
| ------------- | ------ | -------------------------- |
| Authorization | string | API key for authentication |

#### **Example Request (CURL)**

```bash
curl -H "Authorization: your_secure_api_key" "http://localhost:80/api/v1/userStatus?user_id=123456789012345678"
```

#### **Example Request (TypeScript)**

```typescript
const fetch = require("node-fetch");

async function getUserStatus(userId: string) {
  const response = await fetch(
    `http://localhost:80/api/v1/userStatus?user_id=${userId}`,
    {
      method: "GET",
      headers: {
        Authorization: "your_secure_api_key",
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  const data = await response.json();
  console.log(data);
}
getUserStatus("123456789012345678");
```

#### **Example Response**

```json
{
  "status": "online",
  "activities": [
    {
      "name": "Visual Studio Code",
      "type": "ActivityType.playing",
      "details": "Debugging app.py",
      "state": "Writing bot documentation",
      "large_image_url": "https://example.com/large.png",
      "small_image_url": "https://example.com/small.png"
    }
  ],
  "username": "smirkzyy",
  "display_name": "Smirkzyy",
  "profile_picture": "https://cdn.discordapp.com/avatars/1234567890/avatar.png"
}
```

---

## Bot Commands and Events

### **Commands**

#### **+setautorole**

Sets a default role for new members.

| Parameter | Type   | Description                 |
| --------- | ------ | --------------------------- |
| role_name | string | The name of the role to set |

**Example:**

```plaintext
+setautorole Member
```

**Permissions:** Administrator required.

**Logs Webhook:** Logs the new role configuration.

---

### **status**

Checks the status of API and website.

| Parameter | Type   | Description                                                 |
| --------- | ------ | ----------------------------------------------------------- |
| service   | string | "all" (default), "api", or "web" to check specific services |

**Example:**

```plaintext
+status api
```

**Returns:** Service health indicators.

---

### **Events**

#### **on_member_join**

- Assigns roles to new members.
- Sends a custom welcome message.
- Logs events and errors.

---

## Error Handling

- Logs significant errors and unauthorized access attempts via the logs webhook.
- Gracefully handles exceptions for role assignment and status checks.

---

## Contributing

Please follow the existing code structure and naming conventions. For changes or enhancements:

- Use descriptive commit messages.
- Add relevant test cases.

For more information or troubleshooting, contact the project maintainers.

---

**Last Updated:** 14th January 2025
