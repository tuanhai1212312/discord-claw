# main.py

import json
import time
import threading
import traceback
import requests
import brain
import action
import websocket

tokens = brain.load_tokens()
DISCORD_USER_TOKEN = tokens.get("DISCORD_USER_TOKEN", "")
WEBHOOK_URL = tokens.get("WEBHOOK_URL", "")

WEBHOOK_CHANNEL_ID = None
WEBHOOK_GUILD_ID = None
GUILDS_INFO = []
ACCOUNT_INFO = {}
BOT_USER_ID = None


def log(msg):
    print(f"[Discord Claw] {msg}")


def get_webhook_info():
    global WEBHOOK_CHANNEL_ID, WEBHOOK_GUILD_ID
    try:
        r = requests.get(WEBHOOK_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            WEBHOOK_CHANNEL_ID = data.get("channel_id")
            WEBHOOK_GUILD_ID = data.get("guild_id")
    except Exception as e:
        log(f"Webhook error: {e}")


def check_token(token):
    h = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=h, timeout=10)
    if r.status_code == 200:
        data = r.json()
        username = data.get("username")
        discriminator = data.get("discriminator")
        user_id = data.get("id")
        if discriminator and discriminator != "0":
            return f"{username}#{discriminator}", user_id
        return username, user_id
    return None, None


def initialize():
    global GUILDS_INFO, ACCOUNT_INFO, BOT_USER_ID

    print("Starting Discord Claw..")

    action.init(DISCORD_USER_TOKEN, WEBHOOK_URL)

    account_name, user_id = check_token(DISCORD_USER_TOKEN)
    if not account_name:
        log("Invalid token!")
        return False

    BOT_USER_ID = user_id

    get_webhook_info()
    if not WEBHOOK_CHANNEL_ID:
        log("Could not get webhook channel!")
        return False

    ACCOUNT_INFO = action.get_account_info()
    custom_status = action.get_custom_status()
    ACCOUNT_INFO["custom_status"] = custom_status

    GUILDS_INFO = action.get_full_guilds_info(BOT_USER_ID)

    brain.set_account_info(ACCOUNT_INFO)
    brain.set_guilds_info(GUILDS_INFO)
    action.set_account_info(ACCOUNT_INFO)
    brain.build_system_prompt()

    print("Started Discord Claw!")
    return True


def collect_action_data(ar):
    data_parts = []
    error_parts = []

    for a in ar:
        at = a.get("action", "")

        if not a.get("success") and a.get("error"):
            error_parts.append(f"{at}: {a['error']}")

        if at == "get_messages" and a.get("success") and a.get("messages"):
            txt = "[MESSAGES]:\n"
            for m in a["messages"]:
                bot_tag = " [BOT]" if m.get("is_bot") else ""
                reply_tag = f" (reply_to:{m.get('reply_to')})" if m.get("reply_to") else ""
                attach = f" | attachments:{','.join(m.get('attachments', []))}" if m.get("attachments") else ""
                txt += f"msg_id:{m['message_id']} | author:{m['author']}({m['author_id']}){bot_tag}{reply_tag} | {m['content']}{attach} | {m['timestamp']}\n"
            data_parts.append(txt)

        elif at == "search_message" and a.get("success") and a.get("results"):
            if isinstance(a["results"], list):
                txt = "[SEARCH RESULTS]:\n"
                for m in a["results"]:
                    txt += f"msg_id:{m['message_id']} | author:{m['author']}({m['author_id']}) | {m['content']} | {m['timestamp']}\n"
                data_parts.append(txt)
            else:
                data_parts.append(f"[SEARCH]: {a['results']}")

        elif at == "list_channels" and a.get("success") and a.get("channels"):
            txt = "[CHANNELS]:\n"
            for ch in a["channels"]:
                txt += f"channel_id:{ch['channel_id']} | name:{ch['name']} | type:{ch['type']} | parent:{ch.get('parent_id','none')}\n"
            data_parts.append(txt)

        elif at == "list_categories" and a.get("success") and a.get("categories"):
            txt = "[CATEGORIES]:\n"
            for c in a["categories"]:
                txt += f"category_id:{c['category_id']} | name:{c['name']} | position:{c.get('position',0)}\n"
            data_parts.append(txt)

        elif at == "list_roles" and a.get("success") and a.get("roles"):
            txt = "[ROLES]:\n"
            for r in a["roles"]:
                txt += f"role_id:{r['role_id']} | name:{r['name']} | color:{r.get('color_hex','#000000')} | hoist:{r.get('hoist')} | mentionable:{r.get('mentionable')} | position:{r.get('position',0)}\n"
            data_parts.append(txt)

        elif at == "get_server_info" and a.get("success") and a.get("server"):
            s = a["server"]
            txt = f"[SERVER INFO]:\n"
            txt += f"name:{s.get('name')} | guild_id:{s.get('guild_id')} | owner_id:{s.get('owner_id')}\n"
            txt += f"members:{s.get('member_count')} | online:{s.get('online_count')}\n"
            txt += f"channels:{s.get('channel_count')} | text:{s.get('text_channels')} | voice:{s.get('voice_channels')}\n"
            txt += f"boost_level:{s.get('boost_level')} | boost_count:{s.get('boost_count')}\n"
            txt += f"created:{s.get('created_at')} | description:{s.get('description')}\n"
            if s.get("roles"):
                for r in s["roles"]:
                    txt += f"role_id:{r['role_id']} | name:{r['name']} | position:{r.get('position',0)}\n"
            data_parts.append(txt)

        elif at == "get_user_info" and a.get("success") and a.get("user"):
            u = a["user"]
            txt = f"[USER INFO]:\n"
            txt += f"user_id:{u.get('user_id')} | username:{u.get('username')} | display:{u.get('display_name')} | nick:{u.get('nickname')}\n"
            txt += f"is_bot:{u.get('is_bot')} | joined:{u.get('joined_server')} | created:{u.get('account_created')}\n"
            txt += f"roles:{u.get('roles')}\n"
            data_parts.append(txt)

        elif at == "create_channel" and a.get("success") and a.get("data"):
            d = a["data"]
            data_parts.append(f"[CREATED CHANNEL]: channel_id:{d['channel_id']} | name:{d['name']} | type:{d['type']} | parent:{d.get('parent_id','none')}")

        elif at == "create_role" and a.get("success") and a.get("data"):
            d = a["data"]
            data_parts.append(f"[CREATED ROLE]: role_id:{d['role_id']} | name:{d['name']} | color:{d.get('color')} | hoist:{d.get('hoist')} | mentionable:{d.get('mentionable')}")

        elif at == "create_webhook" and a.get("success") and a.get("data"):
            d = a["data"]
            data_parts.append(f"[CREATED WEBHOOK]: webhook_id:{d['webhook_id']} | name:{d['name']} | url:{d['webhook_url']}")

        elif at == "list_webhooks" and a.get("success") and a.get("webhooks"):
            txt = "[WEBHOOKS]:\n"
            for wh in a["webhooks"]:
                txt += f"webhook_id:{wh['webhook_id']} | name:{wh['name']} | url:{wh['webhook_url']}\n"
            data_parts.append(txt)

    return data_parts, error_parts


def process_message(author_name, author_id, content, webhook_id, is_bot):
    global GUILDS_INFO, ACCOUNT_INFO

    try:
        if is_bot or webhook_id:
            return

        if not content.strip():
            return

        if content.strip() == "!clearchat":
            brain.clear_chat_history()
            action.send_webhook_message("🧹 Chat cleared! Memory kept.")
            return

        print(f"[USER] : {content}")
        log("Thinking...")

        result = brain.think(content, author_name)

        reply = result.get("reply", "...")
        actions = result.get("actions", [])
        needs_result = result.get("needs_result", False)
        tokens_used = result.get("tokens_used", 0)

        if actions:
            log("Actioning..")
            ar = action.execute_actions(actions, GUILDS_INFO)
            data_parts, error_parts = collect_action_data(ar)

            if needs_result and (data_parts or error_parts):
                feedback = ""
                if data_parts:
                    feedback += "[ACTION RESULTS]:\n" + "\n".join(data_parts)
                if error_parts:
                    feedback += "\n[ERRORS]:\n" + "\n".join(error_parts)

                result2 = brain.think(feedback, "System")
                reply2 = result2.get("reply", "")
                actions2 = result2.get("actions", [])
                tokens_used += result2.get("tokens_used", 0)

                if actions2:
                    ar2 = action.execute_actions(actions2, GUILDS_INFO)
                    _, error_parts2 = collect_action_data(ar2)
                    reply = reply2 if reply2 else reply
                    if error_parts2:
                        err_feedback = "[ERRORS]:\n" + "\n".join(error_parts2)
                        result3 = brain.think(err_feedback, "System")
                        tokens_used += result3.get("tokens_used", 0)
                        if result3.get("reply"):
                            reply = result3["reply"]
                else:
                    reply = reply2 if reply2 else reply

                log(f"Need Result | Reply : {reply[:80]}{'...' if len(reply) > 80 else ''} | Token used : {tokens_used}")

            else:
                if error_parts:
                    err_feedback = "[ERRORS]: " + "; ".join(error_parts)
                    retry = brain.think(err_feedback, "System")
                    tokens_used += retry.get("tokens_used", 0)
                    if retry.get("reply"):
                        reply = retry["reply"]
                    retry_actions = retry.get("actions", [])
                    if retry_actions:
                        action.execute_actions(retry_actions, GUILDS_INFO)

                log(f"Action : {len(actions)}/{len(actions)} | Reply : {reply[:80]}{'...' if len(reply) > 80 else ''} | Token used : {tokens_used}")
        else:
            log(f"Action : 0/0 | Reply : {reply[:80]}{'...' if len(reply) > 80 else ''} | Token used : {tokens_used}")

        if reply:
            if len(reply) > 2000:
                for i in range(0, len(reply), 1990):
                    action.send_webhook_message(reply[i:i + 1990])
                    time.sleep(0.5)
            else:
                action.send_webhook_message(reply)

    except Exception as e:
        log(f"ERROR: {e}")
        traceback.print_exc()
        try:
            action.send_webhook_message(f"❌ Error: {e}")
        except:
            pass


class Gateway:
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.ws = None
        self.heartbeat_interval = None
        self.sequence = None
        self.running = True
        self.session_id = None

    def start(self):
        while self.running:
            try:
                self.ws = websocket.WebSocket()
                self.ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                hello = json.loads(self.ws.recv())
                self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000
                t = threading.Thread(target=self._heartbeat, daemon=True)
                t.start()
                self._identify()
                while self.running:
                    raw = self.ws.recv()
                    if raw:
                        data = json.loads(raw)
                        if data.get("s"):
                            self.sequence = data["s"]
                        self._handle(data)
            except Exception as e:
                if self.running:
                    log(f"Gateway error: {e}")
                    time.sleep(5)

    def _heartbeat(self):
        while self.running:
            try:
                time.sleep(self.heartbeat_interval)
                if self.ws and self.running:
                    self.ws.send(json.dumps({"op": 1, "d": self.sequence}))
            except:
                break

    def _identify(self):
        self.ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {"os": "windows", "browser": "Chrome", "device": ""},
                "presence": {"activities": [], "status": "online", "since": 0, "afk": False}
            }
        }))

    def _handle(self, data):
        op = data.get("op")
        t = data.get("t")
        d = data.get("d")

        if op in [7, 9]:
            try:
                self.ws.close()
            except:
                pass
            return

        if not d:
            return

        if t == "READY":
            self.session_id = d.get("session_id")

        elif t == "MESSAGE_CREATE":
            channel_id = d.get("channel_id", "")
            if channel_id != WEBHOOK_CHANNEL_ID:
                return
            author = d.get("author", {})
            threading.Thread(
                target=process_message,
                args=(
                    author.get("username", "Unknown"),
                    author.get("id", ""),
                    d.get("content", ""),
                    d.get("webhook_id"),
                    author.get("bot", False)
                ),
                daemon=True
            ).start()

    def stop(self):
        self.running = False
        try:
            if self.ws:
                self.ws.close()
        except:
            pass


if __name__ == "__main__":
    if not initialize():
        exit(1)

    gw = Gateway(DISCORD_USER_TOKEN, BOT_USER_ID)
    try:
        gw.start()
    except KeyboardInterrupt:
        print("\nStopped.")
        gw.stop()
