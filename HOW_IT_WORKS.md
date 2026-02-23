# How It Works: Technical Deep Dive 🧠

This document explains the core logic and architectural decisions behind the **Secret Birthday Planner**.

## 1. Smart Venue Discovery Logic
The application uses a simulated **Discovery Service** (`discovery_service.py`) to provide highly relevant venue suggestions.

### The 5KM Radius Algorithm
When a user enters a neighborhood (e.g., *Koramangala*), the service:
1. Filters its `REAL_DATA` registry for venues in that specific area.
2. If data exists, it generates 5-10 plans specifically for that neighborhood.
3. If no specific area data exists, it falls back to city-wide data with random "simulated" distances within 5KM.

### Dynamic Plan Generation
Plans are NOT static. They are generated based on:
- **Budget Margin**: Suggests options from 50% to 200% of the user's budget.
- **Needs Matching**: Automatically prioritizes venues that offer the specific requirements (Cake, Food, etc.) selected by the group.

## 2. Automated Budget Distribution
The `Event` model in `models.py` uses a weighted distribution property:

| Category | Default Weight |
| :--- | :--- |
| **Cake** | 30% |
| **Decoration** | 20% |
| **Food** | 50% |

**Collaborative Redistribution**: If the group decides they don't need a cake, the system automatically redistributes that 30% to Food and Decor proportionally, ensuring every rupee is put to use.

## 3. Group Collaboration System
### Invite & Join Flow
1. **Generation**: A unique UUID-based code is generated upon event creation.
2. **Session Identification**: We use Name-based sessions. When a friend joins via a link, their name is stored in the session and linked to the event's `GroupMember` registry.
3. **Ghost Planning**: The system allows guest-style planning without requiring secondary friends to create full app accounts.

### Real-Time Chat
The chat system uses an API-polling strategy:
- **Backend**: `chat_messages` table stores every message with a timestamp and sender.
- **Frontend**: A JavaScript interval polls the API every 3 seconds to fetch new messages and update the UI container seamlessly.

## 4. Security Architecture
- **PIN-Based Access**: Uses a "Simple Auth" pattern where a Name + PIN combo identifies a user.
- **Resource Ownership**: Database queries for host-specific views are strictly filtered by `creator_id` ensured through the Flask Session.

---
*For more information on the implementation, refer to the [walkthrough.md](./walkthrough.md) in the brain directory.*
