# Cutslut Discord API Bot Documentation

This documentation outlines the usage and structure of the Cutslut Discord API bot, which tracks user status, activity, and profile information for [cutslut.app](https://cutslut.app).

---

## Overview

The bot provides an API endpoint to check user status and activity within a Discord server by their user ID. It integrates with Flask for API handling and Discord.py for interacting with Discord servers.

---

## Prerequisites

- Python 3.11.5+
- Discord bot token
- API key for secure access
- Libraries in `requirements.txt` installed
- Environment variables setup (.env file)

### **Required Libraries**

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the root of your project:

```
API_VERSION=api_version (e.g: 1.0.0)
BOT_TOKEN=your_actual_discord_bot_token
API_KEY=your_secure_api_key
GUILD_ID=your_discord_server_id
WELCOME_WEBHOOK=webhook_link
API_HEALTH=health_check_api_route
API_VERSION=api_version_route
WEBSITE_URL=base_website_url
```

- **API_VERSION**: The version your API is on.
- **BOT_TOKEN**: The token for your Discord bot.
- **API_KEY**: A secure key for API authorization.
- **GUILD_ID**: The ID of the Discord server to monitor.
- **WELCOME_WEBHOOK**: Your Discord webhook link.
- **API_HEALTH**: API route for your health check.
- **API_VERSION**: API Route for your version check.
- **WEBSITE_URL**: Base website URL.

---

## API Endpoint

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
curl -H "Authorization: your_secure_api_key" "http://localhost:6969/api/v1/userStatus?user_id=123456789012345678"
```

#### **Example Request (TypeScript)**

```typescript
const fetch = require("node-fetch");

async function getUserStatus(userId: string) {
  const response = await fetch(
    `http://localhost:6969/api/v1/userStatus?user_id=${userId}`,
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
  "activities": [
    {
      "details": "Debugging app.py",
      "large_image_url": "https://cdn.discordapp.com/app-assets/383226320970055681/565945350645481492.png",
      "name": "Visual Studio Code",
      "small_image_url": "https://cdn.discordapp.com/app-assets/383226320970055681/565949878753165353.png",
      "state": "Debugging: cutslut_discord_api",
      "type": "ActivityType.playing"
    }
  ],
  "display_name": "smirkzyy",
  "profile_picture": "https://cdn.discordapp.com/avatars/641652579310239746/edc82e420fe354a2929a50b746f9a44e.png?size=1024",
  "status": "dnd",
  "username": "smirkzyy"
}
```

#### **Error Responses**

| Status Code | Message              | Description                             |
| ----------- | -------------------- | --------------------------------------- |
| 401         | Unauthorized         | Invalid or missing API key              |
| 400         | user_id not provided | No user ID was supplied in the request  |
| 404         | User not found       | The user ID was not found in the server |

---

## Code Structure

### **fetch_user_status(user_id)**

Asynchronously retrieves the status and activity of a user by ID from a specific guild.

#### **Attributes Included**

- `status`: User's online status (`online`, `offline`, `dnd`, `idle`).
- `activities`: A list of current user activities, each containing:
  - `name`: Name of the activity.
  - `type`: Type of the activity.
  - `details`: Additional details (optional).
  - `state`: Current state or status of the activity.
  - `large_image_url`: URL for the large activity image.
  - `small_image_url`: URL for the small activity image.
- `username`: The user's Discord username.
- `display_name`: The user's server-specific nickname (if available).
- `profile_picture`: URL to the user's profile picture.

### **Security Considerations**

- **API Key Usage**: Ensure that your API key is kept secret and never hard-coded in your codebase.
- **Server Access**: The bot can only retrieve user information from servers where it is a member.

---

## Deployment

To run the bot and the API service concurrently:

Windows:

```bash
python app.py
```

Linux:

```bash
python3 app.py
```

---

## Troubleshooting

1. **`AttributeError: 'CustomActivity'`**:

   - This occurs when accessing attributes (`details`) not available on `CustomActivity`.
   - Solution: The code now handles `CustomActivity` separately using `state`.

2. **Bot Not Fetching User Information**:
   - Ensure `GUILD_ID` is correct and the bot has permissions to read member data.

---

## Conclusion

This API bot allows seamless integration of Discord user presence and activity data into your applications while ensuring security and flexibility with API key authentication.
