# action.py

import requests
import time

BASE_URL = "https://discord.com/api/v9"
USER_TOKEN = ""
WEBHOOK_URL = ""
ACCOUNT_INFO = {}
LAST_CREATED_ID = None

def init(token, webhook_url):
    global USER_TOKEN, WEBHOOK_URL
    USER_TOKEN = token
    WEBHOOK_URL = webhook_url

def set_account_info(info):
    global ACCOUNT_INFO
    ACCOUNT_INFO = info

def headers():
    return {"Authorization": USER_TOKEN, "Content-Type": "application/json"}

def resolve_channel_id(channel_id):
    global LAST_CREATED_ID
    if not channel_id:
        return channel_id
    if str(channel_id) == "LAST_CREATED":
        if LAST_CREATED_ID:
            return LAST_CREATED_ID
        return channel_id
    return str(channel_id)

def get_account_info():
    try:
        r = requests.get(f"{BASE_URL}/users/@me", headers=headers(), timeout=10)
        if r.status_code == 200:
            data = r.json()
            uid = int(data.get("id", 0))
            if uid:
                ts = ((uid >> 22) + 1420070400000) / 1000
                from datetime import datetime
                data["created_at"] = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S UTC")
            return data
        return {}
    except:
        return {}

def get_custom_status():
    try:
        r = requests.get(f"{BASE_URL}/users/@me/settings", headers=headers(), timeout=10)
        if r.status_code == 200:
            return r.json().get("custom_status", None)
        return None
    except:
        return None

def set_custom_status(text=""):
    try:
        cs = {"text": text} if text else None
        r = requests.patch(f"{BASE_URL}/users/@me/settings", headers=headers(), json={"custom_status": cs}, timeout=10)
        return r.status_code == 200, None
    except Exception as e:
        return False, str(e)

def clear_custom_status():
    try:
        r = requests.patch(f"{BASE_URL}/users/@me/settings", headers=headers(), json={"custom_status": None}, timeout=10)
        return r.status_code == 200, None
    except Exception as e:
        return False, str(e)

def get_guilds():
    try:
        r = requests.get(f"{BASE_URL}/users/@me/guilds", headers=headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return []
    except:
        return []

def get_guild_channels(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return []
    except:
        return []

def get_guild_member_self(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/users/@me/guilds/{guild_id}/member", headers=headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return {}
    except:
        return {}

def get_full_guilds_info(user_id=None):
    guilds = get_guilds()
    result = []
    for g in guilds:
        gd = {"id": g["id"], "name": g["name"], "owner": g.get("owner", False), "channels": []}
        member = get_guild_member_self(g["id"])
        gd["joined_at"] = member.get("joined_at", "Unknown")
        channels = get_guild_channels(g["id"])
        for ch in channels:
            if ch["type"] in [0, 2, 4, 5, 15]:
                gd["channels"].append({"id": ch["id"], "name": ch["name"], "type": ch["type"]})
        result.append(gd)
        time.sleep(0.3)
    return result

def list_channels(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=headers(), timeout=10)
        if r.status_code == 200:
            channels = []
            type_map = {0: "TEXT", 2: "VOICE", 4: "CATEGORY", 5: "ANNOUNCEMENT", 13: "STAGE", 15: "FORUM"}
            for ch in r.json():
                channels.append({
                    "channel_id": ch["id"],
                    "name": ch["name"],
                    "type": type_map.get(ch["type"], f"TYPE_{ch['type']}"),
                    "position": ch.get("position", 0),
                    "parent_id": ch.get("parent_id"),
                    "topic": ch.get("topic", "")
                })
            channels.sort(key=lambda x: x["position"])
            return True, channels
        elif r.status_code == 403:
            return False, "No permission to view channels"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def list_categories(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=headers(), timeout=10)
        if r.status_code == 200:
            categories = []
            for ch in r.json():
                if ch["type"] == 4:
                    categories.append({
                        "category_id": ch["id"],
                        "name": ch["name"],
                        "position": ch.get("position", 0)
                    })
            categories.sort(key=lambda x: x["position"])
            return True, categories
        elif r.status_code == 403:
            return False, "No permission"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def get_server_info(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}?with_counts=true", headers=headers(), timeout=10)
        if r.status_code == 200:
            g = r.json()
            info = {
                "name": g.get("name"),
                "guild_id": g.get("id"),
                "owner_id": g.get("owner_id"),
                "description": g.get("description"),
                "member_count": g.get("approximate_member_count"),
                "online_count": g.get("approximate_presence_count"),
                "icon": g.get("icon"),
                "banner": g.get("banner"),
                "boost_level": g.get("premium_tier"),
                "boost_count": g.get("premium_subscription_count"),
                "verification_level": g.get("verification_level"),
                "created_at": None,
                "features": g.get("features", []),
                "roles": []
            }
            gid = int(g.get("id", 0))
            if gid:
                ts = ((gid >> 22) + 1420070400000) / 1000
                from datetime import datetime
                info["created_at"] = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S UTC")
            for role in g.get("roles", []):
                info["roles"].append({
                    "role_id": role["id"],
                    "name": role["name"],
                    "color": role.get("color", 0),
                    "position": role.get("position", 0)
                })
            info["roles"].sort(key=lambda x: x["position"], reverse=True)
            channels = get_guild_channels(guild_id)
            info["channel_count"] = len(channels)
            info["text_channels"] = len([c for c in channels if c["type"] == 0])
            info["voice_channels"] = len([c for c in channels if c["type"] == 2])
            return True, info
        elif r.status_code == 403:
            return False, "No permission to view server info"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def get_user_info(guild_id, user_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}/members/{user_id}", headers=headers(), timeout=10)
        if r.status_code == 200:
            m = r.json()
            user = m.get("user", {})
            info = {
                "user_id": user.get("id"),
                "username": user.get("username"),
                "display_name": user.get("global_name"),
                "avatar": user.get("avatar"),
                "nickname": m.get("nick"),
                "joined_server": m.get("joined_at"),
                "roles": m.get("roles", []),
                "is_bot": user.get("bot", False),
                "account_created": None
            }
            uid = int(user.get("id", 0))
            if uid:
                ts = ((uid >> 22) + 1420070400000) / 1000
                from datetime import datetime
                info["account_created"] = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S UTC")
            return True, info
        elif r.status_code == 403:
            return False, "No permission to view member info"
        elif r.status_code == 404:
            return False, "User not found in this server"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def search_message(channel_id, query, limit=20):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.get(f"{BASE_URL}/channels/{cid}/messages?limit={limit}", headers=headers(), timeout=10)
        if r.status_code == 200:
            results = []
            query_lower = query.lower()
            for m in r.json():
                content = m.get("content", "")
                if query_lower in content.lower():
                    msg = {
                        "message_id": m["id"],
                        "author": m["author"]["username"],
                        "author_id": m["author"]["id"],
                        "content": content,
                        "timestamp": m["timestamp"],
                        "is_bot": m["author"].get("bot", False)
                    }
                    if m.get("attachments"):
                        msg["attachments"] = [a["url"] for a in m["attachments"]]
                    results.append(msg)
            if results:
                return True, results
            return True, f"No messages found containing '{query}'"
        elif r.status_code == 403:
            return False, "No permission to read messages"
        elif r.status_code == 404:
            return False, "Channel not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def send_message(channel_id, content):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.post(f"{BASE_URL}/channels/{cid}/messages", headers=headers(), json={"content": content}, timeout=10)
        if r.status_code == 200:
            return True, None
        elif r.status_code == 404:
            return False, f"Channel {cid} not found"
        elif r.status_code == 403:
            return False, f"No permission to send in channel {cid}"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def send_webhook_message(content):
    try:
        r = requests.post(WEBHOOK_URL, json={"content": str(content)}, timeout=10)
        return r.status_code in [200, 204]
    except:
        return False

def reply_to_message(channel_id, message_id, content):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.post(
            f"{BASE_URL}/channels/{cid}/messages", headers=headers(),
            json={"content": content, "message_reference": {"message_id": str(message_id), "channel_id": str(cid)}},
            timeout=10
        )
        if r.status_code == 200:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to send message"
        elif r.status_code == 404:
            return False, "Channel or message not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def edit_message(channel_id, message_id, content):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.patch(f"{BASE_URL}/channels/{cid}/messages/{message_id}", headers=headers(), json={"content": content}, timeout=10)
        if r.status_code == 200:
            return True, None
        elif r.status_code == 403:
            return False, "Can only edit own messages"
        elif r.status_code == 404:
            return False, "Message not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def delete_message(channel_id, message_id):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.delete(f"{BASE_URL}/channels/{cid}/messages/{message_id}", headers=headers(), timeout=10)
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to delete this message"
        elif r.status_code == 404:
            return False, "Message not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def add_reaction(channel_id, message_id, emoji):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.put(
            f"{BASE_URL}/channels/{cid}/messages/{message_id}/reactions/{requests.utils.quote(emoji)}/@me",
            headers=headers(), timeout=10
        )
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to add reactions"
        elif r.status_code == 404:
            return False, "Message not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def get_messages(channel_id, limit=10):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.get(f"{BASE_URL}/channels/{cid}/messages?limit={limit}", headers=headers(), timeout=10)
        if r.status_code == 200:
            msgs = []
            for m in r.json():
                msg = {
                    "message_id": m["id"],
                    "author": m["author"]["username"],
                    "author_id": m["author"]["id"],
                    "content": m.get("content", ""),
                    "timestamp": m["timestamp"],
                    "is_bot": m["author"].get("bot", False)
                }
                if m.get("attachments"):
                    msg["attachments"] = [a["url"] for a in m["attachments"]]
                if m.get("embeds"):
                    msg["has_embeds"] = True
                if m.get("message_reference"):
                    msg["reply_to"] = m["message_reference"].get("message_id")
                msgs.append(msg)
            return True, msgs
        elif r.status_code == 403:
            return False, "No permission to read messages"
        elif r.status_code == 404:
            return False, "Channel not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def get_latest_message_id(channel_id, offset=0):
    success, data = get_messages(channel_id, offset + 5)
    if success and data and len(data) > offset:
        return data[offset]["message_id"], None
    elif success and data:
        return data[-1]["message_id"], None
    elif success:
        return None, "No messages in channel"
    return None, data

def react_latest(channel_id, emoji, offset=0):
    msg_id, err = get_latest_message_id(channel_id, offset)
    if not msg_id:
        return False, err or "No messages found"
    return add_reaction(channel_id, msg_id, emoji)

def reply_latest(channel_id, content, offset=0):
    msg_id, err = get_latest_message_id(channel_id, offset)
    if not msg_id:
        return False, err or "No messages found"
    return reply_to_message(channel_id, msg_id, content)

def delete_latest(channel_id, offset=0):
    msg_id, err = get_latest_message_id(channel_id, offset)
    if not msg_id:
        return False, err or "No messages found"
    return delete_message(channel_id, msg_id)

def change_nickname(guild_id, nickname):
    try:
        r = requests.patch(
            f"{BASE_URL}/guilds/{guild_id}/members/@me",
            headers=headers(), json={"nick": nickname}, timeout=10
        )
        if r.status_code == 200:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to change nickname"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def create_channel(guild_id, name, channel_type=0, parent_id=None):
    global LAST_CREATED_ID
    try:
        payload = {"name": name, "type": channel_type}
        if parent_id:
            payload["parent_id"] = str(parent_id)
        r = requests.post(
            f"{BASE_URL}/guilds/{guild_id}/channels",
            headers=headers(), json=payload, timeout=15
        )
        if r.status_code in [200, 201]:
            ch = r.json()
            LAST_CREATED_ID = ch["id"]
            return True, {
                "channel_id": ch["id"],
                "name": ch["name"],
                "type": ch["type"],
                "parent_id": ch.get("parent_id")
            }
        elif r.status_code == 403:
            return False, "No permission to create channels (need MANAGE_CHANNELS)"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def move_channel_to_category(channel_id, category_id):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.patch(
            f"{BASE_URL}/channels/{cid}",
            headers=headers(),
            json={"parent_id": str(category_id)},
            timeout=10
        )
        if r.status_code == 200:
            ch = r.json()
            return True, {
                "channel_id": ch["id"],
                "name": ch["name"],
                "parent_id": ch.get("parent_id")
            }
        elif r.status_code == 403:
            return False, "No permission to move channel (need MANAGE_CHANNELS)"
        elif r.status_code == 404:
            return False, "Channel or category not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)


PERMISSIONS = {
    "view_channel": 1 << 10,
    "send_messages": 1 << 11,
    "send_tts_messages": 1 << 12,
    "manage_messages": 1 << 13,
    "embed_links": 1 << 14,
    "attach_files": 1 << 15,
    "read_message_history": 1 << 16,
    "mention_everyone": 1 << 17,
    "use_external_emojis": 1 << 18,
    "add_reactions": 1 << 6,
    "connect": 1 << 20,
    "speak": 1 << 21,
    "mute_members": 1 << 22,
    "deafen_members": 1 << 23,
    "move_members": 1 << 24,
    "use_vad": 1 << 25,
    "manage_channels": 1 << 4,
    "manage_roles": 1 << 28,
    "manage_webhooks": 1 << 29,
    "create_invite": 1 << 0,
    "kick_members": 1 << 1,
    "ban_members": 1 << 2,
    "administrator": 1 << 3,
    "use_slash_commands": 1 << 31,
    "request_to_speak": 1 << 32,
    "manage_threads": 1 << 34,
    "send_messages_in_threads": 1 << 38,
}

def calculate_permissions(perm_list):
    total = 0
    for perm in perm_list:
        perm_lower = perm.lower().replace(" ", "_")
        if perm_lower in PERMISSIONS:
            total |= PERMISSIONS[perm_lower]
    return str(total)

def set_channel_permissions(channel_id, target_id, target_type, allow_perms=None, deny_perms=None):
    try:
        cid = resolve_channel_id(channel_id)
        allow = calculate_permissions(allow_perms or [])
        deny = calculate_permissions(deny_perms or [])
        perm_type = 0 if target_type == "role" else 1
        r = requests.put(
            f"{BASE_URL}/channels/{cid}/permissions/{target_id}",
            headers=headers(),
            json={"allow": allow, "deny": deny, "type": perm_type},
            timeout=10
        )
        if r.status_code == 204:
            return True, {
                "channel_id": cid,
                "target_id": target_id,
                "target_type": target_type,
                "allow": allow_perms or [],
                "deny": deny_perms or []
            }
        elif r.status_code == 403:
            return False, "No permission to manage channel permissions (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "Channel or target not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def delete_channel_permission(channel_id, target_id):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.delete(
            f"{BASE_URL}/channels/{cid}/permissions/{target_id}",
            headers=headers(), timeout=10
        )
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to manage channel permissions"
        elif r.status_code == 404:
            return False, "Permission override not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def create_role(guild_id, name, color=0, permissions=None, hoist=False, mentionable=False):
    try:
        perm_value = calculate_permissions(permissions or [])
        payload = {
            "name": name,
            "color": color,
            "permissions": perm_value,
            "hoist": hoist,
            "mentionable": mentionable
        }
        r = requests.post(
            f"{BASE_URL}/guilds/{guild_id}/roles",
            headers=headers(), json=payload, timeout=10
        )
        if r.status_code == 200:
            role = r.json()
            return True, {
                "role_id": role["id"],
                "name": role["name"],
                "color": role.get("color", 0),
                "permissions": role.get("permissions"),
                "hoist": role.get("hoist", False),
                "mentionable": role.get("mentionable", False)
            }
        elif r.status_code == 403:
            return False, "No permission to create roles (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def edit_role(guild_id, role_id, name=None, color=None, permissions=None, hoist=None, mentionable=None):
    try:
        payload = {}
        if name is not None:
            payload["name"] = name
        if color is not None:
            payload["color"] = color
        if permissions is not None:
            payload["permissions"] = calculate_permissions(permissions)
        if hoist is not None:
            payload["hoist"] = hoist
        if mentionable is not None:
            payload["mentionable"] = mentionable
        r = requests.patch(
            f"{BASE_URL}/guilds/{guild_id}/roles/{role_id}",
            headers=headers(), json=payload, timeout=10
        )
        if r.status_code == 200:
            role = r.json()
            return True, {
                "role_id": role["id"],
                "name": role["name"],
                "color": role.get("color", 0),
                "permissions": role.get("permissions")
            }
        elif r.status_code == 403:
            return False, "No permission to edit roles (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "Role not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def delete_role(guild_id, role_id):
    try:
        r = requests.delete(
            f"{BASE_URL}/guilds/{guild_id}/roles/{role_id}",
            headers=headers(), timeout=10
        )
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to delete roles (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "Role not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def list_roles(guild_id):
    try:
        r = requests.get(f"{BASE_URL}/guilds/{guild_id}/roles", headers=headers(), timeout=10)
        if r.status_code == 200:
            roles = []
            for role in r.json():
                roles.append({
                    "role_id": role["id"],
                    "name": role["name"],
                    "color": role.get("color", 0),
                    "color_hex": f"#{role.get('color', 0):06X}" if role.get("color") else "#000000",
                    "position": role.get("position", 0),
                    "hoist": role.get("hoist", False),
                    "mentionable": role.get("mentionable", False),
                    "permissions": role.get("permissions", "0")
                })
            roles.sort(key=lambda x: x["position"], reverse=True)
            return True, roles
        elif r.status_code == 403:
            return False, "No permission to view roles"
        elif r.status_code == 404:
            return False, "Server not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def assign_role_to_member(guild_id, user_id, role_id):
    try:
        r = requests.put(
            f"{BASE_URL}/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers=headers(), timeout=10
        )
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to assign roles (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "User or role not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def remove_role_from_member(guild_id, user_id, role_id):
    try:
        r = requests.delete(
            f"{BASE_URL}/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers=headers(), timeout=10
        )
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to remove roles (need MANAGE_ROLES)"
        elif r.status_code == 404:
            return False, "User or role not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def delete_channel(channel_id):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.delete(f"{BASE_URL}/channels/{cid}", headers=headers(), timeout=10)
        if r.status_code == 200:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to delete channels (need MANAGE_CHANNELS)"
        elif r.status_code == 404:
            return False, "Channel not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def create_webhook(channel_id, name):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.post(
            f"{BASE_URL}/channels/{cid}/webhooks",
            headers=headers(), json={"name": name}, timeout=10
        )
        if r.status_code in [200, 201]:
            wh = r.json()
            return True, {
                "webhook_id": wh["id"],
                "webhook_url": f"https://discord.com/api/webhooks/{wh['id']}/{wh['token']}",
                "name": wh["name"],
                "channel_id": wh["channel_id"]
            }
        elif r.status_code == 403:
            return False, "No permission to create webhooks (need MANAGE_WEBHOOKS)"
        elif r.status_code == 404:
            return False, "Channel not found"
        return False, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return False, str(e)

def delete_webhook(webhook_id):
    try:
        r = requests.delete(f"{BASE_URL}/webhooks/{webhook_id}", headers=headers(), timeout=10)
        if r.status_code == 204:
            return True, None
        elif r.status_code == 403:
            return False, "No permission to delete webhooks (need MANAGE_WEBHOOKS)"
        elif r.status_code == 404:
            return False, "Webhook not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def list_webhooks(channel_id):
    try:
        cid = resolve_channel_id(channel_id)
        r = requests.get(f"{BASE_URL}/channels/{cid}/webhooks", headers=headers(), timeout=10)
        if r.status_code == 200:
            whs = []
            for wh in r.json():
                whs.append({
                    "webhook_id": wh["id"],
                    "name": wh["name"],
                    "channel_id": wh["channel_id"],
                    "webhook_url": f"https://discord.com/api/webhooks/{wh['id']}/{wh.get('token', 'NO_TOKEN')}"
                })
            return True, whs
        elif r.status_code == 403:
            return False, "No permission to view webhooks (need MANAGE_WEBHOOKS)"
        elif r.status_code == 404:
            return False, "Channel not found"
        return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)

def check_condition(condition):
    if condition == "has_status":
        status = get_custom_status()
        return status is not None and status.get("text")
    elif condition == "no_status":
        status = get_custom_status()
        return status is None or not status.get("text")
    elif condition.startswith("status_contains:"):
        text = condition.split(":", 1)[1]
        status = get_custom_status()
        if status and status.get("text"):
            return text.lower() in status["text"].lower()
        return False
    elif condition == "always":
        return True
    return False

def execute_single_action(act, guilds_info=None):
    at = act.get("type", "")

    if at == "send_message":
        cid = act.get("channel_id")
        if not cid:
            return {"action": at, "success": False, "error": "No channel_id"}
        success, error = send_message(cid, act.get("content", ""))
        r = {"action": at, "success": success, "channel_id": resolve_channel_id(cid)}
        if error:
            r["error"] = error
        return r

    elif at == "set_custom_status":
        success, error = set_custom_status(text=act.get("text", ""))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "clear_custom_status":
        success, error = clear_custom_status()
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "wait":
        time.sleep(act.get("seconds", 1))
        return {"action": "wait", "success": True}

    elif at == "add_reaction":
        success, error = add_reaction(act.get("channel_id"), act.get("message_id"), act.get("emoji", "👍"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "react_latest":
        success, error = react_latest(act.get("channel_id"), act.get("emoji", "👍"), act.get("offset", 0))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "reply_latest":
        success, error = reply_latest(act.get("channel_id"), act.get("content", ""), act.get("offset", 0))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "delete_latest":
        success, error = delete_latest(act.get("channel_id"), act.get("offset", 0))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "delete_message":
        success, error = delete_message(act.get("channel_id"), act.get("message_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "edit_message":
        success, error = edit_message(act.get("channel_id"), act.get("message_id"), act.get("content", ""))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "reply_to_message":
        success, error = reply_to_message(act.get("channel_id"), act.get("message_id"), act.get("content", ""))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "get_messages":
        success, data = get_messages(act.get("channel_id"), act.get("limit", 10))
        if success:
            return {"action": at, "success": True, "messages": data}
        return {"action": at, "success": False, "error": data}

    elif at == "search_message":
        success, data = search_message(act.get("channel_id"), act.get("query", ""), act.get("limit", 20))
        if success:
            return {"action": at, "success": True, "results": data}
        return {"action": at, "success": False, "error": data}

    elif at == "list_channels":
        success, data = list_channels(act.get("guild_id"))
        if success:
            return {"action": at, "success": True, "channels": data}
        return {"action": at, "success": False, "error": data}

    elif at == "list_categories":
        success, data = list_categories(act.get("guild_id"))
        if success:
            return {"action": at, "success": True, "categories": data}
        return {"action": at, "success": False, "error": data}

    elif at == "get_server_info":
        success, data = get_server_info(act.get("guild_id"))
        if success:
            return {"action": at, "success": True, "server": data}
        return {"action": at, "success": False, "error": data}

    elif at == "get_user_info":
        success, data = get_user_info(act.get("guild_id"), act.get("user_id"))
        if success:
            return {"action": at, "success": True, "user": data}
        return {"action": at, "success": False, "error": data}

    elif at == "change_nickname":
        success, error = change_nickname(act.get("guild_id"), act.get("nickname", ""))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "create_channel":
        success, data = create_channel(
            act.get("guild_id"),
            act.get("name", "new-channel"),
            act.get("channel_type", 0),
            act.get("parent_id")
        )
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "move_channel_to_category":
        success, data = move_channel_to_category(act.get("channel_id"), act.get("category_id"))
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "set_channel_permissions":
        success, data = set_channel_permissions(
            act.get("channel_id"),
            act.get("target_id"),
            act.get("target_type", "role"),
            act.get("allow", []),
            act.get("deny", [])
        )
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "delete_channel_permission":
        success, error = delete_channel_permission(act.get("channel_id"), act.get("target_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "create_role":
        success, data = create_role(
            act.get("guild_id"),
            act.get("name", "New Role"),
            act.get("color", 0),
            act.get("permissions", []),
            act.get("hoist", False),
            act.get("mentionable", False)
        )
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "edit_role":
        success, data = edit_role(
            act.get("guild_id"),
            act.get("role_id"),
            act.get("name"),
            act.get("color"),
            act.get("permissions"),
            act.get("hoist"),
            act.get("mentionable")
        )
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "delete_role":
        success, error = delete_role(act.get("guild_id"), act.get("role_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "list_roles":
        success, data = list_roles(act.get("guild_id"))
        if success:
            return {"action": at, "success": True, "roles": data}
        return {"action": at, "success": False, "error": data}

    elif at == "assign_role":
        success, error = assign_role_to_member(act.get("guild_id"), act.get("user_id"), act.get("role_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "remove_role":
        success, error = remove_role_from_member(act.get("guild_id"), act.get("user_id"), act.get("role_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "delete_channel":
        success, error = delete_channel(act.get("channel_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "create_webhook":
        success, data = create_webhook(act.get("channel_id"), act.get("name", "Webhook"))
        if success:
            return {"action": at, "success": True, "data": data}
        return {"action": at, "success": False, "error": data}

    elif at == "delete_webhook":
        success, error = delete_webhook(act.get("webhook_id"))
        r = {"action": at, "success": success}
        if error:
            r["error"] = error
        return r

    elif at == "list_webhooks":
        success, data = list_webhooks(act.get("channel_id"))
        if success:
            return {"action": at, "success": True, "webhooks": data}
        return {"action": at, "success": False, "error": data}

    elif at == "loop":
        times = min(act.get("times", 1), 50)
        loop_actions = act.get("actions", [])
        loop_results = []
        for i in range(times):
            for la in loop_actions:
                lr = execute_single_action(la, guilds_info)
                loop_results.append(lr)
                if la.get("type") != "wait":
                    time.sleep(0.3)
        return {"action": "loop", "success": True, "iterations": times, "results": loop_results}

    elif at == "if":
        condition = act.get("condition", "always")
        result = check_condition(condition)
        chosen = act.get("then", []) if result else act.get("else", [])
        if_results = []
        for ca in chosen:
            cr = execute_single_action(ca, guilds_info)
            if_results.append(cr)
            if ca.get("type") != "wait":
                time.sleep(0.3)
        return {"action": "if", "success": True, "condition": condition, "result": result, "results": if_results}

    return {"action": at, "success": False, "error": f"Unknown action: {at}"}

def execute_actions(actions, guilds_info=None):
    results = []
    for act in actions:
        at = act.get("type", "")
        try:
            r = execute_single_action(act, guilds_info)
            results.append(r)
            if at not in ["wait", "loop", "if"]:
                time.sleep(0.5)
        except Exception as e:
            results.append({"action": at, "success": False, "error": str(e)})
    return results