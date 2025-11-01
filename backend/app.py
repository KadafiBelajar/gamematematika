import traceback
import json
import os
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from question_gen import generate_question
from grader import check_answer, generate_limit_explanation

# Deteksi apakah running di Vercel
is_vercel = os.environ.get('VERCEL', '0') == '1'
if is_vercel:
    # Di Vercel, dari root project (working directory di root saat runtime dari api/)
    template_folder = 'templates'
    static_folder = 'static'
else:
    # Di local, path relatif dari backend/
    template_folder = '../templates'
    static_folder = '../static'

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = "kunci-rahasia-yang-sangat-aman-dan-unik"

# --- Rute Navigasi Utama ---

@app.route("/")
def index():
    """Menampilkan halaman utama."""
    return render_template("index.html")

@app.route("/stages")
def stage_select():
    """Menampilkan halaman pemilihan stage."""
    dev_mode_on = session.get('dev_mode', False)
    return render_template("stage_select.html", dev_mode_on=dev_mode_on)

@app.route("/levels/<stage_name>")
def level_select(stage_name):
    """Menampilkan grid level untuk stage apa pun (limit, turunan, integral)."""

    # Inisialisasi progres di session jika belum ada.
    if 'progress' not in session:
        # Struktur: session['progress'] = {'nama_stage': level_tertinggi_terbuka}
        session['progress'] = {'limit': 1, 'turunan': 1, 'integral': 1}
        session.modified = True

    # Ambil level tertinggi yang sudah terbuka untuk stage ini.
    unlocked_until = session['progress'].get(stage_name, 1)
    
    # Siapkan data untuk dikirim ke template HTML.
    levels_data = []
    for i in range(1, 16):
        state = 'unlocked' if i <= unlocked_until else 'locked'
        levels_data.append({'number': i, 'state': state})
    
    dev_mode_on = session.get('dev_mode', False)
    return render_template("level_select.html", levels=levels_data, stage_name=stage_name, dev_mode_on=dev_mode_on)

@app.route("/main/<stage_name>/<int:level_num>")
def main_game(stage_name, level_num):
    """Halaman permainan utama untuk level yang spesifik."""
    # Cek apakah level yang diakses sudah terbuka untuk mencegah akses via URL.
    unlocked_until = session.get('progress', {}).get(stage_name, 1)
    if level_num > unlocked_until:
        # Jika belum, lempar kembali ke halaman pemilihan level.
        return redirect(url_for('level_select', stage_name=stage_name))
        
    # Kirim info stage dan level ke template agar bisa digunakan oleh JavaScript.
    return render_template("main.html", stage_name=stage_name, level_num=level_num)

@app.route("/learn")
def learn():
    return render_template("learn.html")

# --- API (Endpoints yang dipanggil oleh JavaScript) ---

@app.route("/api/question")
def api_get_question():
    """API untuk mendapatkan soal berdasarkan level dari query parameter."""
    level = request.args.get('level', 1, type=int)
    stage = request.args.get('stage') or request.args.get('stage_name') or session.get('current_stage')
    if not stage:
        # Fallback: gunakan 'limit' agar tidak error
        stage = 'limit'
    print(f"--- Menerima permintaan untuk soal level: {level} ---")
    try:
        # Simpan stage saat ini di session agar konsisten selama level
        session['current_stage'] = stage
        session.modified = True
        question = generate_question(stage, level)
        print(f"Berhasil membuat soal ID: {question['id']} untuk level {level}")
        
        # Gunakan kunci session yang tetap untuk mencegah penumpukan data.
        session_data = {
            "id": question["id"],
            "answer": question["answer"],
            "params": question["params"]
        }
        session['current_question'] = session_data
        session.modified = True

        # Siapkan data yang akan dikirim ke pengguna.
        # Siapkan opsi tampilan LaTeX untuk UI, tanpa mengubah nilai asli untuk penilaian
        try:
            from sympy import sympify, latex as sympy_latex
            options_display = []
            for opt in question["options"]:
                try:
                    opt_latex = sympy_latex(sympify(opt))
                    options_display.append(opt_latex)
                except Exception:
                    options_display.append(str(opt))
        except Exception:
            options_display = [str(opt) for opt in question["options"]]

        question_for_user = {
            "id": question["id"],
            "latex": question["latex"],
            "options": question["options"],            # nilai yang akan dikirim kembali saat submit
            "options_display": options_display          # string LaTeX untuk ditampilkan
        }
        
        return jsonify(question_for_user)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"!!! GAGAL membuat soal untuk level {level} !!!")
        print(error_trace)
        return jsonify({
            "error": "Terjadi kesalahan di server saat membuat soal.",
            "detail": str(e)
        }), 500

@app.route("/api/answer", methods=["POST"])
def api_handle_answer():
    """API untuk memvalidasi jawaban (tidak langsung unlock level)."""
    data = request.get_json()
    question_id = data.get("question_id")
    user_answer = data.get("answer")
    stage_name = data.get("stage_name")
    level_num = int(data.get("level_num"))

    question_data = session.get('current_question')

    # Verifikasi ID soal
    if question_data is None or question_data.get('id') != question_id:
        return jsonify({"error": "Sesi soal tidak ditemukan atau sudah kedaluwarsa."}), 400

    correct_answer = question_data['answer']
    is_correct = check_answer(user_answer, correct_answer)
    
    session.pop('current_question', None)

    # PENTING: Jangan unlock level di sini!
    # Unlock hanya terjadi saat boss HP = 0 (di endpoint /api/level-complete)
    
    response = {
        "correct": is_correct,
        "canonical_answer": correct_answer
    }
    return jsonify(response)

@app.route("/api/level-complete", methods=["POST"])
def api_level_complete():
    """
    API baru untuk unlock level berikutnya.
    Dipanggil oleh JavaScript saat Boss HP <= 0.
    """
    data = request.get_json()
    stage_name = data.get("stage_name")
    level_num = int(data.get("level_num"))
    
    print(f"=== LEVEL COMPLETE: Stage={stage_name}, Level={level_num} ===")
    
    # Inisialisasi progress jika belum ada
    if 'progress' not in session:
        session['progress'] = {'limit': 1, 'turunan': 1, 'integral': 1}
    
    unlocked_until = session['progress'].get(stage_name, 1)
    
    # Unlock level berikutnya hanya jika:
    # 1. Level yang diselesaikan adalah level tertinggi yang terbuka
    # 2. Belum mencapai level maksimal (15)
    if level_num == unlocked_until and level_num < 15:
        session['progress'][stage_name] = unlocked_until + 1
        session.modified = True
        print(f">>> Level {level_num + 1} UNLOCKED! <<<")
        return jsonify({
            "success": True,
            "message": f"Level {level_num + 1} telah terbuka!",
            "next_level": level_num + 1
        })
    else:
        print(f">>> No new level unlocked (already unlocked or max level) <<<")
        return jsonify({
            "success": True,
            "message": "Level diselesaikan!",
            "next_level": None
        })

# --- Developer Endpoint ---

@app.route("/api/dev/toggle-dev-mode", methods=["POST"])
def toggle_dev_mode():
    """Toggle Developer Mode: backup progress asli atau kembalikan."""
    # Cek status dev mode saat ini
    dev_mode_on = session.get('dev_mode', False)
    
    if not dev_mode_on:
        # Nyalakan dev mode: backup progress asli
        if 'progress' not in session:
            session['progress'] = {'limit': 1, 'turunan': 1, 'integral': 1}
        
        # Simpan progress asli
        session['real_progress'] = session['progress'].copy()
        
        # Unlock semua level
        session['progress'] = {'limit': 15, 'turunan': 15, 'integral': 15}
        session['dev_mode'] = True
        session.modified = True
        
        return jsonify({"message": "Developer Mode diaktifkan! Semua level terbuka.", "dev_mode": True})
    else:
        # Matikan dev mode: kembalikan progress asli
        if 'real_progress' in session:
            session['progress'] = session['real_progress'].copy()
            session.pop('real_progress', None)
        else:
            # Fallback jika real_progress tidak ada
            session['progress'] = {'limit': 1, 'turunan': 1, 'integral': 1}
        
        session['dev_mode'] = False
        session.modified = True
        
        return jsonify({"message": "Developer Mode dinonaktifkan! Progress dikembalikan.", "dev_mode": False})


if __name__ == "__main__":
    app.run(debug=True)