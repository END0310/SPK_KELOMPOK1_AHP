from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import mysql.connector
import os
import json
from datetime import datetime

app = Flask(__name__, template_folder='template')
app.secret_key = 'spk_ahp_secret_key_2026'

FIXED_KRITERIA = ['Tingkat Kerusakan', 'Dampak terhadap Akademik', 'Frekuensi Penggunaan', 'Biaya Perbaikan']

# ===== KONFIGURASI MySQL =====
# Sesuaikan dengan kredensial MySQL Anda
DB_CONFIG = {
    'host':     'localhost',
    'port':     3306,
    'user':     'root',
    'password': '',          # ganti dengan password MySQL Anda
    'database': 'spk_ahp',
    'charset':  'utf8mb4',
    'autocommit': True,
}


# ===== DATABASE MySQL =====
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def init_db():
    """Buat database dan tabel jika belum ada."""
    # Koneksi tanpa nama database dulu, untuk CREATE DATABASE
    cfg_no_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
    conn = mysql.connector.connect(**cfg_no_db)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE `{DB_CONFIG['database']}`")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            created_at  DATETIME     NOT NULL,
            k           INT          NOT NULL,
            a           INT          NOT NULL,
            nama_kriteria TEXT        NOT NULL,
            weights     TEXT         NOT NULL,
            ranking     TEXT         NOT NULL,
            CR          DOUBLE       NOT NULL,
            total_score DOUBLE       NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediksi (
            id                  INT AUTO_INCREMENT PRIMARY KEY,
            banyak_alternatif   INT  NOT NULL,
            nama_alternatif     TEXT NOT NULL,
            bobot_alternatif    TEXT NOT NULL,
            hasil_keputusan     TEXT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    cursor.close()
    conn.close()


def save_analysis(k, a, nama_kriteria, weights, ranking, CR, total_score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO analysis_history
           (created_at, k, a, nama_kriteria, weights, ranking, CR, total_score)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), k, a,
         json.dumps(nama_kriteria, ensure_ascii=False),
         json.dumps(weights, ensure_ascii=False),
         json.dumps(ranking, ensure_ascii=False),
         float(CR), float(total_score))
    )
    cursor.close()
    conn.close()


def save_prediksi(banyak_alternatif, nama_alternatif, bobot_alternatif, hasil_keputusan):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO prediksi
           (banyak_alternatif, nama_alternatif, bobot_alternatif, hasil_keputusan)
           VALUES (%s, %s, %s, %s)''',
        (banyak_alternatif,
         json.dumps(nama_alternatif, ensure_ascii=False),
         json.dumps(bobot_alternatif, ensure_ascii=False),
         json.dumps(hasil_keputusan, ensure_ascii=False))
    )
    cursor.close()
    conn.close()


# ===== HELPER =====
def parse_pairwise_value(value):
    """
    Menerima input berupa:
      - Bilangan bulat      : "3"   → 3.0
      - Desimal             : "2.5" → 2.5
      - Pecahan biasa       : "1/3" → 0.333...
      - Pecahan terbalik    : "1/5" → 0.2
    """
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value == '':
            return None
        if '/' in value:
            parts = value.split('/')
            if len(parts) == 2:
                try:
                    num = float(parts[0].strip())
                    den = float(parts[1].strip())
                    if den == 0:
                        raise ValueError(f"Pembagian dengan nol: {value}")
                    return num / den
                except ValueError:
                    raise ValueError(f"Format pecahan tidak valid: '{value}'")
            raise ValueError(f"Format pecahan tidak valid: '{value}'")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Nilai tidak valid: '{value}'")
    return float(value)


def ahp_weights(matrix):
    n = len(matrix)
    col_sums = matrix.sum(axis=0)
    norm_matrix = matrix / col_sums
    weights = norm_matrix.mean(axis=1)
    weighted_sum = matrix @ weights
    lambda_max = float(np.mean(weighted_sum / weights))
    CI = (lambda_max - n) / (n - 1)
    RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_dict.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0
    return weights, CR


def build_fixed_matrix():
    mat = np.zeros((4, 4))
    mat[0] = [1,    1/2,  3,    4  ]
    mat[1] = [2,    1,    3,    3  ]
    mat[2] = [1/3,  1/3,  1,    3  ]
    mat[3] = [1/4,  1/3,  1/3,  1  ]
    return mat


# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/alternatif_input', methods=['GET', 'POST'])
def alternatif_input():
    if request.method == 'POST':
        try:
            a = int(request.form['alternatif'])
            if not (2 <= a <= 20):
                return render_template('alternatif_input.html', error="Alternatif harus antara 2-20!")
            nama_alt = [request.form.get(f'alt_{i}', '').strip() for i in range(a)]
            if any(not n for n in nama_alt):
                return render_template('alternatif_input.html', a=a,
                                       error="Semua alternatif harus diberi nama!")
            session['a'] = a
            session['nama_alt'] = nama_alt
            return redirect(url_for('alternatif_matrix'))
        except (ValueError, KeyError):
            return render_template('alternatif_input.html', error="Input tidak valid!")
    return render_template('alternatif_input.html')


@app.route('/alternatif_matrix', methods=['GET', 'POST'])
def alternatif_matrix():
    a = session.get('a')
    nama_alt = session.get('nama_alt')
    if not a or not nama_alt or len(nama_alt) != a:
        return redirect(url_for('alternatif_input'))

    mat_k = build_fixed_matrix()
    weights_k, CR_k = ahp_weights(mat_k)
    k = len(FIXED_KRITERIA)

    if request.method == 'POST':
        # Simpan input mentah agar bisa prefill saat error
        raw_inputs = {}
        for c in range(k):
            for i in range(a):
                for j in range(i + 1, a):
                    key = f'alt_m_{c}_{i}_{j}'
                    raw_inputs[key] = request.form.get(key, '').strip()

        try:
            alternative_priority = []
            alt_cr_list = []

            for c in range(k):
                mat = np.zeros((a, a))
                for i in range(a):
                    mat[i][i] = 1.0
                for i in range(a):
                    for j in range(i + 1, a):
                        field_name = f'alt_m_{c}_{i}_{j}'
                        raw = raw_inputs.get(field_name, '')
                        if not raw:
                            raise ValueError(
                                f"Nilai perbandingan '{FIXED_KRITERIA[c]}' "
                                f"baris {i+1} vs {j+1} harus diisi!")
                        val = parse_pairwise_value(raw)
                        if val is None or val <= 0:
                            raise ValueError(
                                f"Nilai tidak valid pada '{FIXED_KRITERIA[c]}' "
                                f"({nama_alt[i]} vs {nama_alt[j]}): '{raw}'")
                        mat[i][j] = val
                        mat[j][i] = 1.0 / val

                alt_w, alt_cr = ahp_weights(mat)
                alternative_priority.append(alt_w)
                alt_cr_list.append(round(float(alt_cr), 6))

            alternative_priority = np.vstack(alternative_priority)
            final_scores = np.dot(alternative_priority.T, weights_k)
            final_scores = np.clip(final_scores, 0.0, None)
            total = np.sum(final_scores)
            if total > 0:
                final_scores = final_scores / total

            ranking_index = np.argsort(-final_scores)
            ranking = [(nama_alt[i], round(float(final_scores[i]), 6)) for i in ranking_index]
            total_score = round(float(np.sum(final_scores)), 6)

            try:
                save_analysis(k=k, a=a, nama_kriteria=FIXED_KRITERIA,
                              weights=weights_k.tolist(), ranking=ranking,
                              CR=float(CR_k), total_score=total_score)
                save_prediksi(banyak_alternatif=a, nama_alternatif=nama_alt,
                              bobot_alternatif=final_scores.tolist(),
                              hasil_keputusan=ranking)
            except Exception as db_err:
                print(f"[WARNING] DB error: {db_err}")

            session['hasil_ranking'] = ranking
            session['hasil_weights'] = [round(w, 6) for w in weights_k.tolist()]
            session['hasil_CR'] = round(float(CR_k), 6)
            session['hasil_nama_kriteria'] = FIXED_KRITERIA
            session['hasil_total_score'] = total_score
            session['alt_cr_list'] = alt_cr_list
            session['hasil_a'] = a
            session['hasil_k'] = k

            return redirect(url_for('hasil_view'))

        except ValueError as ve:
            return render_template('alternatif_matrix.html',
                                   a=a, nama_alt=nama_alt, k=k,
                                   nama_kriteria=FIXED_KRITERIA,
                                   weights=weights_k.tolist(), CR=CR_k,
                                   raw_inputs=raw_inputs,
                                   error=f"❌ {str(ve)}")
        except Exception as e:
            return render_template('alternatif_matrix.html',
                                   a=a, nama_alt=nama_alt, k=k,
                                   nama_kriteria=FIXED_KRITERIA,
                                   weights=weights_k.tolist(), CR=CR_k,
                                   raw_inputs={},
                                   error=f"❌ Terjadi kesalahan: {str(e)}")

    return render_template('alternatif_matrix.html',
                           a=a, nama_alt=nama_alt, k=k,
                           nama_kriteria=FIXED_KRITERIA,
                           weights=weights_k.tolist(), CR=CR_k,
                           raw_inputs={})


@app.route('/hasil')
def hasil_view():
    ranking = session.get('hasil_ranking', [])
    weights = session.get('hasil_weights', [])
    CR = session.get('hasil_CR', 0.0)
    nama_kriteria = session.get('hasil_nama_kriteria', [])
    total_score = session.get('hasil_total_score', 0.0)
    if not ranking:
        return redirect(url_for('alternatif_input'))
    return render_template('hasil.html',
                           ranking=ranking, weights=weights,
                           CR=CR, nama_kriteria=nama_kriteria,
                           total_score=total_score)


@app.route('/dashboard')
def dashboard_view():
    ranking = session.get('hasil_ranking', [])
    weights = session.get('hasil_weights', [])
    CR = session.get('hasil_CR', 0.0)
    nama_kriteria = session.get('hasil_nama_kriteria', [])
    total_score = session.get('hasil_total_score', 0.0)
    alt_cr_list = session.get('alt_cr_list', [])
    k = session.get('hasil_k', len(nama_kriteria))
    a = session.get('hasil_a', len(ranking))

    ranking_labels = [item[0] for item in ranking]
    ranking_scores = [item[1] for item in ranking]

    return render_template('dashboard.html',
                           k=k, a=a, CR=CR,
                           weights=weights,
                           ranking=ranking,
                           nama_kriteria=nama_kriteria,
                           total_score=total_score,
                           ranking_labels=ranking_labels,
                           ranking_scores=ranking_scores,
                           alt_cr_list=alt_cr_list)


@app.route('/history')
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM analysis_history ORDER BY id DESC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        history_data = []
        for row in rows:
            try:
                history_data.append({
                    'id':           row['id'],
                    'created_at':   str(row['created_at']),
                    'k':            row['k'],
                    'a':            row['a'],
                    'nama_kriteria': json.loads(row['nama_kriteria']),
                    'weights':      json.loads(row['weights']),
                    'ranking':      json.loads(row['ranking']),
                    'CR':           row['CR'],
                    'total_score':  row['total_score'],
                })
            except Exception:
                continue
        return render_template('history.html', history=history_data)
    except Exception as db_err:
        return render_template('history.html', history=[],
                               error=f"❌ {str(db_err)}")


@app.route('/prediksi')
def prediksi():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM prediksi ORDER BY id DESC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        data = []
        for row in rows:
            try:
                data.append({
                    'id':               row['id'],
                    'banyak_alternatif': row['banyak_alternatif'],
                    'nama_alternatif':  json.loads(row['nama_alternatif']),
                    'bobot_alternatif': json.loads(row['bobot_alternatif']),
                    'hasil_keputusan':  json.loads(row['hasil_keputusan']),
                })
            except Exception:
                continue
        return render_template('prediksi.html', data=data)
    except Exception as e:
        return render_template('prediksi.html', data=[], error=f"❌ {str(e)}")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
