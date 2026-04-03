# 🤖 DiscordClaw AI

> Trợ lý tự động hóa Discord thông minh — điều khiển tài khoản Discord của bạn bằng ngôn ngữ tự nhiên, powered by Groq AI ⚡

---

## ✨ Giới thiệu

**DiscordClaw AI** là một công cụ tự động hóa Discord mạnh mẽ, cho phép bạn điều khiển tài khoản Discord thông qua chat tự nhiên bằng tiếng Việt hoặc tiếng Anh. Chỉ cần nhắn tin như đang nói chuyện, AI sẽ hiểu và thực hiện mọi thứ cho bạn! 🎉

---

## 🚀 Tính năng nổi bật

### 💬 Quản lý tin nhắn
- Gửi tin nhắn đến bất kỳ kênh nào
- Reply tin nhắn cụ thể hoặc tin nhắn mới nhất
- Chỉnh sửa và xóa tin nhắn
- Tìm kiếm tin nhắn theo nội dung
- React emoji vào tin nhắn bất kỳ
- Đọc lịch sử tin nhắn

### 🎭 Quản lý Role
- Tạo role mới với màu sắc, quyền hạn tùy chỉnh
- Chỉnh sửa role hiện có
- Xóa role
- Gán / gỡ role cho thành viên
- Xem danh sách tất cả role trong server

### 📁 Quản lý kênh
- Tạo kênh text, voice, announcement, category
- Tạo kênh bên trong category
- Di chuyển kênh vào category
- Xóa kênh
- Thiết lập quyền riêng cho từng kênh
- Ẩn kênh khỏi @everyone
- Tạo kênh chỉ đọc, kênh private

### 🔗 Webhook
- Tạo webhook trong bất kỳ kênh nào
- Xóa webhook
- Xem danh sách webhook

### 👤 Tài khoản
- Xem thông tin tài khoản
- Đổi nickname trong server
- Đặt / xóa custom status
- Xem thông tin server, thành viên

### ⚙️ Tự động hóa nâng cao
- Lặp hành động nhiều lần (loop)
- Điều kiện if / else
- Chờ giữa các hành động (wait)
- Kết hợp nhiều hành động cùng lúc
- Bộ nhớ vĩnh viễn (nhớ thông tin qua các cuộc trò chuyện)

---

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- Tài khoản Discord (user token)
- API key từ Groq (miễn phí)
- Webhook Discord

### Thư viện cần cài

pip install requests websocket-client

---

## ⚙️ Cài đặt

### Bước 1 — Clone hoặc tải về dự án

Tải toàn bộ các file về cùng một thư mục:
- main.py
- brain.py
- action.py
- token.txt (tạo mới theo hướng dẫn bên dưới)

### Bước 2 — Tạo file token.txt

Tạo file token.txt trong cùng thư mục với nội dung:

DISCORD_USER_TOKEN=token_discord_của_bạn
GROQ_API_KEY=api_key_groq_của_bạn
WEBHOOK_URL=url_webhook_discord_của_bạn

### Bước 3 — Lấy các thông tin cần thiết

**Discord User Token:**
1. Mở Discord trên trình duyệt
2. Nhấn F12 → Console
3. Dán vào: window.webpackChunkdiscord_app.push([[''], {}, e => { m = []; for (let c in e.c) m.push(e.c[c]); }]); m.filter(m => m?.exports?.default?.getToken).map(m => m.exports.default.getToken())[0]
4. Copy token hiện ra

**Groq API Key:**
1. Truy cập console.groq.com
2. Đăng ký tài khoản miễn phí
3. Vào API Keys → Create API Key
4. Copy key

**Discord Webhook URL:**
1. Vào server Discord của bạn
2. Chọn kênh muốn bot nhận lệnh
3. Cài đặt kênh → Integrations → Webhooks → New Webhook
4. Copy Webhook URL

### Bước 4 — Chạy chương trình

python main.py

---

## 💡 Hướng dẫn sử dụng

Sau khi chạy, nhắn tin vào kênh Discord chứa webhook là bot sẽ phản hồi và thực hiện lệnh!

### 🗣️ Cách ra lệnh

Bạn có thể nói chuyện hoàn toàn tự nhiên bằng tiếng Việt hoặc tiếng Anh. Không cần nhớ cú pháp đặc biệt!

---

## 📖 Ví dụ sử dụng chi tiết

### 📨 Gửi tin nhắn

"gửi hello mọi người vào kênh general"
"nhắn 'server sẽ bảo trì lúc 10pm' vào kênh thông-báo"
"gửi @everyone vào kênh announcements kèm thông báo họp nhóm"

### ✏️ Chỉnh sửa & xóa tin nhắn

"sửa tin nhắn xin chào của tôi thành tạm biệt trong general"
"xóa tin nhắn mới nhất của tôi trong spam"
"tìm tin nhắn có chứa 'test' trong general và xóa nó"

### 👍 React tin nhắn

"react ❤️ vào tin nhắn mới nhất trong general"
"react 🎉 vào tin nhắn thứ 2 từ trên xuống trong chat"
"tìm tin nhắn của Hải và react 👍 vào đó"

### 🎭 Tạo và quản lý Role

"tạo role Moderator màu xanh lá có quyền quản lý tin nhắn, hiện trong danh sách thành viên"
"tạo role VIP màu vàng, có thể được mention"
"đổi màu role Admin thành đỏ"
"xóa role Test"
"gán role Member cho user 123456789"
"gỡ role Muted khỏi user 987654321"
"cho tôi xem danh sách tất cả role trong server"

### 📁 Tạo và quản lý kênh

"tạo kênh bot-spam trong category Gaming"
"tạo category Staff với các kênh staff-chat và staff-logs bên trong"
"chuyển kênh general vào category Main"
"xóa kênh test"
"tạo kênh voice Phòng họp trong category Meeting"

### 🔒 Phân quyền kênh

"làm kênh announcements chỉ đọc cho mọi người"
"ẩn kênh staff-only khỏi tất cả mọi người, chỉ role Staff mới thấy"
"cho role Mod quyền manage messages trong kênh general"
"reset quyền của @everyone trong kênh vip"

### 🔍 Tìm kiếm thông tin

"cho tôi xem 10 tin nhắn gần nhất trong general"
"xem thông tin server này"
"xem thông tin user 123456789"
"liệt kê tất cả kênh trong server"
"tài khoản của tôi tên gì, tạo từ bao giờ"

### 👤 Tài khoản cá nhân

"đặt status là đang bận học bài"
"xóa custom status"
"đổi nickname thành ProGamer trong server này"
"nếu đang có status thì xóa, không thì đặt là online"

### 🔗 Webhook

"tạo webhook tên Logger trong kênh logs"
"xem danh sách webhook trong kênh noti"
"xóa webhook 123456789"

### 🔁 Tự động hóa

"spam 3 lần 'hello' vào general mỗi 5 giây"
"gửi thông báo bảo trì vào 3 kênh: general, noti, và chat"
"tạo 5 role màu khác nhau: Red, Blue, Green, Yellow, Purple"

### 🏗️ Setup server hoàn chỉnh

"setup server mới với:
- Role Admin màu đỏ có full quyền
- Role Mod màu xanh có quyền kick và ban
- Role Member màu trắng quyền cơ bản
- Category Information với kênh rules và announcements
- Category General với kênh chat và voice
- Kênh staff-only chỉ Admin và Mod thấy được"

---

## 🧠 Tính năng bộ nhớ

DiscordClaw AI có bộ nhớ vĩnh viễn — nó sẽ ghi nhớ những thông tin quan trọng qua các cuộc trò chuyện:

- "nhớ rằng kênh general của tôi dùng để chat"
- "ghi nhớ user 123456 là admin của server"
- Bot tự động nhớ các thông tin quan trọng khi thực hiện tác vụ

Bộ nhớ này **không bị xóa** khi clear chat history.

---

## 🧹 Lệnh đặc biệt

!clearchat — Xóa lịch sử cuộc trò chuyện với AI (bộ nhớ vĩnh viễn vẫn giữ nguyên)

---

## 🏗️ Cấu trúc dự án

DiscordClaw/
├── main.py        — Điểm khởi động, WebSocket Gateway, xử lý tin nhắn
├── brain.py       — AI engine, system prompt, giao tiếp với Groq API
├── action.py      — Thực thi các lệnh Discord API
└── token.txt      — Cấu hình token và API key (không chia sẻ file này!)

### Luồng hoạt động

User nhắn tin
→ main.py nhận qua WebSocket Gateway
→ brain.py phân tích bằng Groq AI (Llama 4)
→ action.py thực thi lệnh Discord API
→ AI tổng hợp kết quả
→ Webhook gửi reply cho user

---

## ⚡ Model AI

DiscordClaw sử dụng **meta-llama/llama-4-scout-17b-16e-instruct** từ Groq — một trong những model nhanh nhất hiện tại với:
- Tốc độ phản hồi cực nhanh (thường dưới 2 giây)
- Hiểu tiếng Việt tốt
- Context window lớn
- Miễn phí với Groq API

---

## ⚠️ Lưu ý quan trọng

- **Bảo mật:** Không bao giờ chia sẻ file token.txt hoặc Discord user token của bạn với bất kỳ ai
- **Sử dụng có trách nhiệm:** Không spam quá mức, tránh vi phạm quy tắc server
- **Rate limit:** Bot tự động thêm delay giữa các hành động để tránh bị Discord giới hạn
- **Quyền hạn:** Một số tính năng yêu cầu bạn có quyền tương ứng trong server (Manage Channels, Manage Roles, v.v.)

---

## 🐛 Xử lý lỗi thường gặp

**Bot không phản hồi:**
→ Kiểm tra DISCORD_USER_TOKEN còn hợp lệ không
→ Kiểm tra WEBHOOK_URL đúng chưa
→ Đảm bảo nhắn vào đúng kênh chứa webhook

**Lỗi 403 Forbidden:**
→ Tài khoản không có quyền thực hiện hành động đó
→ Cần được cấp quyền tương ứng trong server

**Lỗi 404 Not Found:**
→ Channel ID hoặc Message ID không tồn tại
→ Thử dùng lệnh tự nhiên thay vì cung cấp ID thủ công

**AI không hiểu lệnh:**
→ Thử diễn đạt lại rõ ràng hơn
→ Dùng !clearchat để reset context nếu AI bị nhầm lẫn

**Groq API lỗi:**
→ Kiểm tra GROQ_API_KEY còn hợp lệ
→ Kiểm tra quota tại console.groq.com

---

## 📊 Giới hạn

- Lịch sử chat: tối đa 40 tin nhắn gần nhất
- Loop action: tối đa 50 lần lặp
- Tin nhắn Discord: tối đa 2000 ký tự (tự động chia nhỏ nếu dài hơn)
- Timeout API: 60 giây

---

## 🤝 Đóng góp

Mọi ý kiến đóng góp và cải tiến đều được chào đón! Hãy thoải mái fork và tùy chỉnh theo nhu cầu của bạn.

---

## 📜 License

Dự án này được phát hành cho mục đích học tập và cá nhân.

---

Được tạo với ❤️ — DiscordClaw AI - TuanHai