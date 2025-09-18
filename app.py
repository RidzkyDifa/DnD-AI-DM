import streamlit as st
import random
from db import init_db, add_message, get_messages, reset_chat, save_character, load_character
from openrouter_client import ask_openrouter

st.set_page_config(page_title="DnD AI DM", page_icon="🐉", layout="wide")

# Init DB
init_db()

# load karakter terakhir
char_data = load_character()

if char_data:
    (_, name, race, char_class, level, ac, current_hp, max_hp, temp_hp,
     stats, current_armor, current_weapon, inventory, coin, _) = char_data
    # convert string back to dict/list
    import ast
    stats = ast.literal_eval(stats)
    inventory = ast.literal_eval(inventory)
else:
    name, race, char_class, current_armor, current_weapon = "", "", "", "", ""
    level, ac, current_hp, max_hp, temp_hp, coin = 1, 0, 10, 10, 0, 0
    stats, inventory = {"STR":8,"DEX":8,"CON":8,"INT":8,"WIS":8,"CHA":8}, []

# ================= Sidebar ==============
st.sidebar.header("📝 Character Sheet")

# Character Basic Info
name = st.sidebar.text_input("Nama Karakter", "")

cols = st.sidebar.columns(2)
race = cols[0].text_input("🧝 Ras", "")
char_class = cols[1].text_input("⚔️ Class", "")

#Character Info 
cols = st.sidebar.columns(2)
ac = cols[1].number_input("🛡️ Armor Class (AC)", min_value=0, step=1)
level = cols[0].number_input("Level", min_value=1, step=1, value=1)

cols = st.sidebar.columns(3)
current_hp = cols[0].number_input("❤️ Current HP", min_value=0, step=1, value=10)
max_hp = cols[1].number_input("Max HP", min_value=1, step=1, value=10)
temp_hp = cols[2].number_input("Temp HP", min_value=0, step=1, value= 0)

# Abilities
st.sidebar.subheader("📜 Ability Score")

if "stats" not in st.session_state:
    st.session_state.stats = {
        "STR": 8,
        "DEX": 8,
        "CON": 8,
        "INT": 8,
        "WIS": 8,
        "CHA": 8
    }

stats_order = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

cols = st.sidebar.columns(6)  # bikin 6 kolom sejajar
new_stats = {}
total_points = 0

for i, stat in enumerate(stats_order):
    with cols[i]:
        st.markdown(f"<div style='text-align:center; font-weight:bold;'>{stat}</div>", unsafe_allow_html=True)
        val = st.number_input(
            stat,
            min_value=8,
            max_value=16,
            value=st.session_state.stats.get(stat, 8),
            step=1,
            label_visibility="collapsed",  # biar label ga double
        )
        new_stats[stat] = val
        total_points += val

    # Validasi total points

if total_points > 75:
    st.sidebar.error("Total Ability Score tidak boleh lebih dari 76!")
else:
    st.session_state.stats = new_stats
    st.sidebar.success(f"Total Ability Score: {total_points}")

# ================== Inventory ================
st.sidebar.markdown("---")

# Coin
st.sidebar.subheader("💰 Coin")
if "coin" not in st.session_state:
    st.session_state.coin = {"gold": 0, "silver": 0}

cols = st.sidebar.columns(2)
gold = cols[0].number_input("Gold", min_value=0, value=st.session_state.coin.get("gold", 0), step=1)
silver = cols[1].number_input("Silver", min_value=0, value=st.session_state.coin.get("silver", 0), step=1)
st.session_state.coin = {"gold": gold, "silver": silver}

# Armor and Weapons
st.sidebar.subheader("🛡️ Armor & ⚔️ Weapons")

    # Session state untuk armor & weapons
if "armor" not in st.session_state:
    st.session_state.armor = []
if "weapons" not in st.session_state: 
    st.session_state.weapons = []

    # Input nama armor & weapon yang sedang dipakai
cols = st.sidebar.columns(2)
current_armor = cols[0].text_input("Armor yang dipakai", "")
current_weapon = cols[1].text_input("Weapon yang dipakai", "")
if current_armor and current_armor not in st.session_state.armor:
    st.session_state.armor.append(current_armor)


# Tas
st.sidebar.subheader("🎒 Inventory")

    # Session state untuk inventory
if "inventory" not in st.session_state:
    st.session_state.inventory = []

    # Input nama item & jumlah
cols = st.sidebar.columns(2)
new_item = cols[0].text_input("Tambah Item", "")
new_qty = cols[1].number_input("Jumlah", min_value=1, value=1, step=1)

    # Tombol tambah
if st.sidebar.button("➕ Tambah Item"):
    if new_item:
        # Cek apakah item sudah ada
        found = False
        for item in st.session_state.inventory:
            if item["name"].lower() == new_item.lower():
                item["qty"] += new_qty
                found = True
                break
        if not found:
            st.session_state.inventory.append({"name": new_item, "qty": new_qty})
    else:
        st.sidebar.error("Nama item tidak boleh kosong!")
    st.rerun()

    # Tampilkan inventory
if st.session_state.inventory:
    for i, item in enumerate(st.session_state.inventory):
        item_col = st.sidebar.columns([4, 1])
        qty_text = f" {item['qty']}" if item["qty"] > 1 else ""
        item_col[0].markdown(f"- {item['name']}{qty_text}")
        if item_col[1].button("❌", key=f"del_{i}"):
            st.session_state.inventory.pop(i)
            st.sidebar.warning(f'Item \"{item['name']}\" dihapus!')
            st.rerun()
            
# ================== Roll Dice =================
st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Dice Roller")

    # Bikin 2 kolom untuk dadu 1 dan dadu 2
col1, col2 = st.sidebar.columns(2)

with col1:
    dice_type1 = st.selectbox("Dadu 1", ["d3", "d4", "d6", "d8", "d10", "d12", "d20"], key="dice1")
    num_dice1 = st.number_input("Jumlah", min_value=1, max_value=10, value=1, step=1, key="num1")

with col2:
    dice_type2 = st.selectbox("Dadu 2", ["-", "d3", "d4", "d6", "d8", "d10", "d12", "d20"], key="dice2")
    num_dice2 = st.number_input("Jumlah", min_value=0, max_value=10, value=0, step=1, key="num2")

    # Tombol roll di tengah
btn_col = st.sidebar.columns([1, 2, 1])
with btn_col[1]:
    if st.button("🎲 Roll!"):
        results = []
        total = 0

        # Roll dadu 1
        sides1 = int(dice_type1[1:])
        rolls1 = [random.randint(1, sides1) for _ in range(num_dice1)]
        results.append(f"{num_dice1}{dice_type1}: {rolls1}")
        total += sum(rolls1)

        # Roll dadu 2
        if dice_type2 != "-" and num_dice2 > 0:
            sides2 = int(dice_type2[1:])
            rolls2 = [random.randint(1, sides2) for _ in range(num_dice2)]
            results.append(f"{num_dice2}{dice_type2}: {rolls2}")
            total += sum(rolls2)

        st.session_state.last_roll = f"Saya roll {', '.join(results)} (Total: {total})"

    # Hasil terakhir ditampilkan di bawah
if "last_roll" in st.session_state:
    st.sidebar.success(st.session_state.last_roll)


# =============== Setting ============

# Tombol reset chat
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Settings")
if st.sidebar.button("🔄 Reset Chat"):
    reset_chat()
    st.rerun()


# ============= Main Chat ==============

st.title("🐉 Petualangan Lost Mine of Phandelver ⚔️")
st.write("AI Dungeon Master")

# Ambil chat history
messages = get_messages()

# Kalau chat masih kosong → kasih prompt awal ke DM
if not messages:
    initial_prompt = (
        "Kamu akan menjadi game master untuk game DnD. "
        "Adventure ini berkisah pada serial *Lost Mine of Phandelver*. "
        "Ikuti standar permainan DnD. Permainan menggunakan bahasa Indonesia, "
        "namun untuk nama skill/ability gunakan bahasa Inggris dengan deskripsi dalam bahasa Indonesia. "
        "Saya akan bermain solo, jadi kamu yang akan menggerakkan cerita, NPC, dan dunia. "
        "Untuk roll dadu, ikuti hasil roll yang saya berikan."
    )
    add_message("system", initial_prompt)

# Tombol mulai petualangan
if st.button("🚀 Mulai Petualangan"):
    if name:
        # simpan character ke DB
        save_character({
            "name": name,
            "race": race,
            "char_class": char_class,
            "level": level,
            "ac": ac,
            "current_hp": current_hp,
            "max_hp": max_hp,
            "temp_hp": temp_hp,
            "stats": st.session_state.stats,
            "armor": current_armor,
            "weapon": current_weapon,
            "inventory": st.session_state.inventory,
            "coin": st.session_state.coin
        })
        # bikin deskripsi karakter
        char_summary = (
            f"Nama: {name}, Ras: {race}, Class: {char_class}, "
            f"Level: {level}, AC: {ac}, HP: {current_hp}/{max_hp}, Temp HP: {temp_hp}. "
            f"Ability Scores: {st.session_state.stats}. "
            f"Armor: {current_armor}, Weapon: {current_weapon}. "
            f"Inventory: {st.session_state.inventory}, Coin: {st.session_state.coin}."
        )

        # kasih tau AI soal karakter
        add_message("system", f"Detail karakter pemain:\n{char_summary}")

        # greeting DM
        greeting = (
            f"✨ Selamat datang {name} sang {race} {char_class}! ✨\n\n"
            "Kisah *Lost Mine of Phandelver* kini dimulai...\n"
            "Kamu sedang berada di jalan menuju kota kecil **Phandalin**, "
            "tempat dimana petualangan besar akan dimulai."
        )
        add_message("assistant", greeting)
        st.rerun()
    else:
        st.warning("⚠️ Isi dulu nama karakter sebelum mulai!")

# Tampilkan chat dengan format roleplay
for role, content in messages:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant"):
            st.markdown(content)

# Input user
if user_input := st.chat_input("Aksi kamu apa?"):
    add_message("user", user_input)

    full_messages = [{"role": r, "content": c} for r, c in get_messages()]

    with st.chat_message("assistant"):
        with st.spinner("DM sedang berpikir... 🎲"):
            response = ask_openrouter(full_messages)

    add_message("assistant", response)
    st.rerun()