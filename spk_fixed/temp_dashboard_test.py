from App import app

with app.test_client() as client:
    data = {
        'k': '3',
        'a': '3',
        'CR': '0.0234',
        'weights': '[0.2, 0.3, 0.5]',
        'kriteria_nama_0': 'Harga',
        'kriteria_nama_1': 'Kualitas',
        'kriteria_nama_2': 'Layanan',
        'rank_nama_0': 'A',
        'rank_skor_0': '0.5',
        'rank_nama_1': 'B',
        'rank_skor_1': '0.3',
        'rank_nama_2': 'C',
        'rank_skor_2': '0.2'
    }
    resp = client.post('/dashboard', data=data)
    html = resp.data.decode('utf-8')
    print('status', resp.status_code)
    print('labels=', 'const rankingLabels =' in html)
    print('scores=', 'const rankingScores =' in html)
    print(html[html.index('const rankingLabels ='):html.index('const rankingLabels =')+120])
    print(html[html.index('const rankingScores ='):html.index('const rankingScores =')+120])
