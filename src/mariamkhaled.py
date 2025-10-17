#!/usr/bin/env python3
# MariamKhaled mini-CLI v0.1
# Multilingual (ar/fr/en) simple assistant for Termux

import os, json, sys, time

STATE_PATH = os.path.expanduser("~/.mksys_state.json")

# default state
state = {
    "language": "ar",   # ar / fr / en
    "energy": 100,
    "notes": [],
    "fines": []
}

def load_state():
    global state
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        save_state()

def save_state():
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# strings
STR = {
    "ar": {
        "welcome": "مرحبا بالرئيس خالد 👑 — مريمخالد جاهزة. اختر خيار:",
        "menu": "[1] طاقة  [2] بحث عن عمل  [3] متابعة مخالفات  [4] أوامر الملكة  [5] إعدادات اللغة  [0] خروج",
        "energy": "مؤشر الطاقة الحالي: {}%",
        "prompt": "أدخِل رقم الخيار: ",
        "goodbye": "تم. بأمان يا سيدي 👑",
        "lang_set": "اختر اللغة: 1) العربية 2) Français 3) English",
        "lang_done": "تم تغيير اللغة إلى {}",
        "add_note": "اكتب ملاحظة ثم Enter (فارغ للإلغاء): ",
        "note_saved": "تم حفظ الملاحظة."
    },
    "fr": {
        "welcome": "Bonjour Président Khaled 👑 — MariamKhaled prête. Choisissez:",
        "menu": "[1] Énergie  [2] Recherche d'emploi  [3] Suivi PV  [4] Commandes royales  [5] Langue  [0] Quitter",
        "energy": "Niveau d'énergie actuel : {}%",
        "prompt": "Entrez le numéro : ",
        "goodbye": "Terminé, Sire 👑",
        "lang_set": "Choisissez la langue: 1) العربية 2) Français 3) English",
        "lang_done": "Langue changée en {}",
        "add_note": "Écrivez une note puis Enter (vide pour annuler): ",
        "note_saved": "Note enregistrée."
    },
    "en": {
        "welcome": "Welcome King Khaled 👑 — MariamKhaled ready. Choose:",
        "menu": "[1] Energy  [2] Job search  [3] Fines monitor  [4] Royal commands  [5] Language  [0] Exit",
        "energy": "Current energy level: {}%",
        "prompt": "Enter choice number: ",
        "goodbye": "Done, Your Highness 👑",
        "lang_set": "Pick language: 1) العربية 2) Français 3) English",
        "lang_done": "Language set to {}",
        "add_note": "Type a note then Enter (empty to cancel): ",
        "note_saved": "Note saved."
    }
}

def t(k):
    return STR[state.get("language", "ar")][k]

def show_menu():
    print("\n" + t("welcome"))
    print(t("menu"))

def option_energy():
    print(t("energy").format(state["energy"]))
    # small action: recharge or decrease
    print("1) +10  2) -10  3) back")
    c = input("> ").strip()
    if c == "1":
        state["energy"] = min(100, state["energy"] + 10)
        save_state()
        print(t("energy").format(state["energy"]))
    elif c == "2":
        state["energy"] = max(0, state["energy"] - 10)
        save_state()
        print(t("energy").format(state["energy"]))

def option_job():
    # placeholder: store a job search note
    note = input(t("add_note"))
    if note.strip():
        state["notes"].append({"time": int(time.time()), "text": note})
        save_state()
        print(t("note_saved"))

def option_fines():
    # simple viewer/adder
    print("Fines tracker — list and add (simple).")
    if state["fines"]:
        for i,f in enumerate(state["fines"],1):
            print(f"{i}) Plate: {f.get('plate')} Date: {f.get('date')} Paid:{f.get('paid')}")
    print("a) Add fine  b) Back")
    c = input("> ").strip()
    if c.lower() == "a":
        plate = input("Plate: ").strip()
        date = input("Date (DD/MM/YYYY): ").strip()
        state["fines"].append({"plate": plate, "date": date, "paid": False})
        save_state()
        print("Saved.")

def option_royal():
    print("Royal commands:")
    print("1) Show status  2) Export state  3) Clear notes  4) Back")
    c = input("> ").strip()
    if c == "1":
        print(json.dumps(state, ensure_ascii=False, indent=2))
    elif c == "2":
        p = os.path.expanduser("~/mksys_export.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print("Exported to", p)
    elif c == "3":
        state["notes"] = []
        save_state()
        print("Notes cleared.")

def option_lang():
    print(t("lang_set"))
    c = input("> ").strip()
    if c == "1":
        state["language"] = "ar"
    elif c == "2":
        state["language"] = "fr"
    elif c == "3":
        state["language"] = "en"
    save_state()
    print(t("lang_done").format(state["language"]))

def main():
    load_state()
    while True:
        show_menu()
        choice = input(t("prompt")).strip()
        if choice == "0":
            print(t("goodbye"))
            break
        elif choice == "1":
            option_energy()
        elif choice == "2":
            option_job()
        elif choice == "3":
            option_fines()
        elif choice == "4":
            option_royal()
        elif choice == "5":
            option_lang()
        else:
            print("…")

if __name__ == "__main__":
    main()
