import os
import re
import sys
import msvcrt
from datetime import datetime
from tabulate import tabulate

data_pasien = []

def _umur_from_tgl(tgl: str, today=None) -> int:
    if today is None:
        today = datetime.now()
    lahir = datetime.strptime(tgl, '%Y-%m-%d')
    u = today.year - lahir.year
    if (today.month, today.day) < (lahir.month, lahir.day):
        u -= 1
    return u


def _init_data_pasien():
    today = datetime.now()
    _tgl_daftar = today.strftime('%Y-%m-%d')
    data = [
        {'no_rm': 'RM001', 'nama': 'Andi Pratama', 'tanggal_lahir': '1990-03-15', 'jenis_kelamin': 'Laki-laki',
         'alamat': 'Jl. Merdeka No.1, Jakarta', 'no_telepon': '081234567890', 'golongan_darah': 'A',
         'penyakit': 'Flu', 'keluhan': 'Demam ringan dan batuk', 'tanggal_daftar': _tgl_daftar},
        {'no_rm': 'RM002', 'nama': 'Siti Rahayu', 'tanggal_lahir': '1995-07-22', 'jenis_kelamin': 'Perempuan',
         'alamat': 'Jl. Mawar No.5, Bandung', 'no_telepon': '082345678901', 'golongan_darah': 'B',
         'penyakit': 'Demam', 'keluhan': 'Suhu tubuh 38 derajat', 'tanggal_daftar': _tgl_daftar},
        {'no_rm': 'RM003', 'nama': 'Budi Santoso', 'tanggal_lahir': '1980-11-08', 'jenis_kelamin': 'Laki-laki',
         'alamat': 'Jl. Sudirman No.10, Surabaya', 'no_telepon': '083456789012', 'golongan_darah': 'O',
         'penyakit': 'Hipertensi', 'keluhan': 'Tekanan darah 150/90', 'tanggal_daftar': _tgl_daftar},
        {'no_rm': 'RM004', 'nama': 'Dewi Lestari', 'tanggal_lahir': '2000-01-30', 'jenis_kelamin': 'Perempuan',
         'alamat': 'Jl. Kenanga No.3, Yogyakarta', 'no_telepon': '084567890123', 'golongan_darah': 'AB',
         'penyakit': 'Maag', 'keluhan': 'Nyeri ulu hati', 'tanggal_daftar': _tgl_daftar},
        {'no_rm': 'RM005', 'nama': 'Rizky Maulana', 'tanggal_lahir': '1988-09-12', 'jenis_kelamin': 'Laki-laki',
         'alamat': 'Jl. Melati No.7, Medan', 'no_telepon': '085678901234', 'golongan_darah': 'A',
         'penyakit': 'Diabetes', 'keluhan': 'Kadar gula darah tinggi', 'tanggal_daftar': _tgl_daftar},
    ]
    for p in data:
        p['umur'] = _umur_from_tgl(p['tanggal_lahir'], today)
    return data


data_pasien = _init_data_pasien()
PASSWORD = '123456'


def cek_password(pw: str) -> bool:
    return pw == PASSWORD


def input_password(prompt='  Masukkan Password: ') -> str:
    print(prompt, end='', flush=True)
    chars = []
    while True:
        ch = msvcrt.getwch()
        if ch in ('\r', '\n'):
            print()
            break
        elif ch == '\x08':
            if chars:
                chars.pop()
                print('\b \b', end='', flush=True)
        elif ch == '\x03':
            print()
            raise KeyboardInterrupt
        else:
            chars.append(ch)
            print('*', end='', flush=True)
    return ''.join(chars)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def hr(w=65, ch='-'):
    print(ch * w)


def header(title: str, w=65):
    print('\n' + '=' * w)
    print(title.center(w))
    print('=' * w)


def ok(msg):
    print(f'\n  [OK] {msg}')


def err(msg):
    print(f'\n  [!]  {msg}')


def info(msg):
    print(f'\n  [i]  {msg}')


def pause():
    input('\n  Tekan Enter untuk melanjutkan...')


def confirm(prompt='  Yakin? (y/n): ') -> bool:
    return input(prompt).strip().lower() == 'y'


def inp(label: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    val = input(f'  {label}{suffix}: ').strip()
    return val if val else default


def pilih_jk(current: str = '') -> str:
    label = f' (saat ini: {current})' if current else ''
    hint = ', Enter=tetap' if current else ''
    while True:
        print(f'  Jenis Kelamin{label}:')
        print('    1. Laki-laki')
        print('    2. Perempuan')
        pilih = input(f'  Pilih (1/2{hint}): ').strip()
        if pilih == '1':
            return 'Laki-laki'
        if pilih == '2':
            return 'Perempuan'
        if current and pilih == '':
            return current
        err('Jenis kelamin tidak boleh kosong. Pilih 1 atau 2.')


def validasi_tanggal(tgl: str) -> bool:
    try:
        t = datetime.strptime(tgl, '%Y-%m-%d')
        return t.date() <= datetime.now().date()
    except ValueError:
        return False


def validasi_golongan_darah(gol: str) -> bool:
    return gol.upper() in ('A', 'B', 'AB', 'O')


def validasi_nama(nama: str) -> bool:
    return bool(nama) and all(c.isalpha() or c in (' ', '.', "'", '-') for c in nama)


def validasi_telepon(telepon: str) -> bool:
    return telepon.isdigit() and 10 <= len(telepon) <= 15


def cari_pasien_by_rm(no_rm: str):
    for p in data_pasien:
        if p['no_rm'].lower() == no_rm.lower():
            return p
    return None


def rm_tersedia(no_rm: str, kecuali=None) -> bool:
    for p in data_pasien:
        if p['no_rm'].lower() == no_rm.lower():
            if kecuali and p['no_rm'].lower() == kecuali.lower():
                continue
            return False
    return True


def generate_no_rm() -> str:
    if not data_pasien:
        return 'RM001'
    nomor_list = []
    for p in data_pasien:
        try:
            nomor_list.append(int(p['no_rm'][2:]))
        except (ValueError, IndexError):
            pass
    max_no = max(nomor_list) if nomor_list else 0
    return f'RM{max_no + 1:03d}'


def hitung_umur(tgl_lahir: str) -> int:
    return _umur_from_tgl(tgl_lahir)


# Generic input validation function
def input_validated(label: str, validator, error_msg: str, allow_empty=False, default=''):
    """Generic input with validation loop."""
    while True:
        val = inp(label, default)
        if not val and not allow_empty:
            err(f'{label.strip()} tidak boleh kosong.')
        elif val and not validator(val):
            err(error_msg)
        else:
            return val


def login():
    cls()
    header('LOGIN — SISTEM MANAJEMEN PASIEN RUMAH SAKIT')
    print('  Password default: 123456\n')
    for attempt in range(3):
        pw = input_password('  Masukkan Password: ')
        if cek_password(pw):
            ok('Login berhasil! Selamat datang.')
            pause()
            return
        remaining = 2 - attempt
        if remaining > 0:
            err(f'Password salah. {remaining} percobaan tersisa.')
        else:
            err('Terlalu banyak percobaan. Program keluar.')
            sys.exit(1)


def pasien_lihat_semua():
    header('DAFTAR PASIEN')
    if not data_pasien:
        info('Belum ada data pasien.')
        pause()
        return
    table = [[i, p['no_rm'], p['nama'], p['jenis_kelamin'],
              p['golongan_darah'] or '-', p['penyakit'] or '-', p['no_telepon']]
             for i, p in enumerate(data_pasien, 1)]
    print()
    print(tabulate(table, headers=['No', 'No RM', 'Nama', 'JK', 'Gol. Darah', 'Penyakit', 'No Telepon'],
                   tablefmt='rounded_outline'))
    print(f'\n  Total: {len(data_pasien)} pasien')
    pause()


def pasien_tambah():
    header('TAMBAH PASIEN')
    no_rm = generate_no_rm()
    info(f'No. Rekam Medis otomatis: {no_rm}')

    nama = input_validated('Nama Lengkap              ', validasi_nama,
                          'Nama tidak valid. Tidak boleh mengandung angka atau karakter khusus.')

    tgl = input_validated('Tanggal Lahir (YYYY-MM-DD)', validasi_tanggal,
                         'Format tidak valid. Gunakan YYYY-MM-DD (contoh: 1990-03-15).')

    umur = hitung_umur(tgl)
    info(f'Umur otomatis: {umur} tahun')
    jk = pilih_jk()

    alamat = inp('Alamat                    ')
    if not alamat:
        err('Alamat tidak boleh kosong.')
        pause()
        return

    telepon = input_validated('No. Telepon (10-15 digit)  ', validasi_telepon,
                             'No. telepon tidak valid. Harus angka, minimal 10 digit, maksimal 15 digit.')

    gol = input_validated('Golongan Darah (A/B/AB/O) ', validasi_golongan_darah,
                         'Golongan darah tidak valid. Pilihan: A, B, AB, O.', allow_empty=True)
    gol = gol.upper() if gol else ''

    penyakit = inp('Penyakit / Diagnosa       ')
    keluhan = inp('Catatan Keluhan           ')
    tgl_daftar = datetime.now().strftime('%Y-%m-%d')

    print()
    hr()
    print('  Ringkasan data yang akan disimpan:')
    print(tabulate([
        ['No. Rekam Medis', no_rm], ['Nama', nama], ['Tanggal Lahir', tgl],
        ['Umur', f'{umur} tahun'], ['Jenis Kelamin', jk], ['Alamat', alamat],
        ['No. Telepon', telepon], ['Golongan Darah', gol or '-'],
        ['Penyakit', penyakit or '-'], ['Catatan Keluhan', keluhan or '-'],
        ['Tanggal Daftar', tgl_daftar]], headers=['Field', 'Data'], tablefmt='rounded_outline'))
    print()
    if not confirm('  Simpan data pasien ini? (y/n): '):
        info('Dibatalkan. Data tidak disimpan.')
        pause()
        return

    data_pasien.append({
        'no_rm': no_rm, 'nama': nama, 'tanggal_lahir': tgl, 'umur': umur,
        'jenis_kelamin': jk, 'alamat': alamat, 'no_telepon': telepon,
        'golongan_darah': gol, 'penyakit': penyakit, 'keluhan': keluhan,
        'tanggal_daftar': tgl_daftar})
    ok(f'Pasien "{nama}" ({no_rm}) berhasil ditambahkan.')
    pause()


def pasien_edit():
    header('EDIT PASIEN')
    no_rm = inp('No. RM pasien yang diedit')
    p = cari_pasien_by_rm(no_rm)
    if not p:
        err('Pasien tidak ditemukan.')
        pause()
        return

    print(f'\n  Mengedit: {p["nama"]} ({p["no_rm"]})')
    info('Tekan Enter untuk tidak mengubah nilai.\n')

    # Validasi No. RM
    while True:
        no_rm_baru = inp('No. RM          ', p['no_rm'])
        if not re.fullmatch(r'RM\d+', no_rm_baru.upper()):
            err('Format No. RM tidak valid. Gunakan format RMxxx (contoh: RM001).')
            continue
        no_rm_baru = no_rm_baru.upper()
        if no_rm_baru.lower() != p['no_rm'].lower() and not rm_tersedia(no_rm_baru, kecuali=p['no_rm']):
            err(f'No. RM "{no_rm_baru}" sudah digunakan.')
            continue
        p['no_rm'] = no_rm_baru
        break

    p['nama'] = input_validated('Nama            ', validasi_nama,
                                'Nama tidak valid. Tidak boleh mengandung angka atau karakter khusus.',
                                default=p['nama'])

    # Validasi tanggal lahir
    while True:
        tgl_baru = inp('Tanggal Lahir   ', p['tanggal_lahir'])
        try:
            tgl_parsed = datetime.strptime(tgl_baru, '%Y-%m-%d')
        except ValueError:
            err('Format tanggal tidak valid. Gunakan format YYYY-MM-DD (contoh: 1990-03-15).')
            continue
        if tgl_parsed.date() > datetime.now().date():
            err('Tanggal lahir tidak boleh di masa depan.')
            continue
        p['tanggal_lahir'] = tgl_baru
        p['umur'] = hitung_umur(tgl_baru)
        break

    p['jenis_kelamin'] = pilih_jk(p['jenis_kelamin'])
    p['alamat'] = inp('Alamat          ', p['alamat'])

    p['no_telepon'] = input_validated('No. Telepon     ', validasi_telepon,
                                     'No. telepon tidak valid. Harus angka, minimal 10 digit, maksimal 15 digit.',
                                     default=p['no_telepon'])

    gol_baru = input_validated('Gol. Darah      ', validasi_golongan_darah,
                               'Golongan darah tidak valid. Pilihan: A, B, AB, O.',
                               allow_empty=True, default=p['golongan_darah'] or '')
    p['golongan_darah'] = gol_baru.upper() if gol_baru else ''

    p['penyakit'] = inp('Penyakit        ', p['penyakit'] or '')
    p['keluhan'] = inp('Catatan Keluhan ', p['keluhan'] or '')

    ok(f'Data pasien "{p["nama"]}" berhasil diupdate.')
    pause()


def pasien_hapus():
    header('HAPUS PASIEN')
    no_rm = inp('No. RM pasien yang dihapus')
    p = cari_pasien_by_rm(no_rm)
    if not p:
        err('Pasien tidak ditemukan.')
        pause()
        return

    print(f'  Akan menghapus: {p["nama"]} ({p["no_rm"]})')
    if confirm():
        data_pasien.remove(p)
        ok(f'Data pasien "{p["nama"]}" berhasil dihapus.')
    else:
        info('Dibatalkan.')
    pause()


def pasien_cari():
    header('CARI PASIEN')
    keyword = inp('Kata kunci (nama / no RM / penyakit / keluhan)').lower()
    hasil = [p for p in data_pasien if
             keyword in p['nama'].lower() or keyword in p['no_rm'].lower() or
             keyword in (p['penyakit'] or '').lower() or keyword in (p['keluhan'] or '').lower()]
    if not hasil:
        err(f'Tidak ada hasil untuk "{keyword}".')
        pause()
        return

    table = [[p['no_rm'], p['nama'], p['jenis_kelamin'], p['penyakit'] or '-', p['no_telepon']] for p in hasil]
    print(f'\n  {len(hasil)} hasil ditemukan:\n')
    print(tabulate(table, headers=['No RM', 'Nama', 'JK', 'Penyakit', 'No Telepon'], tablefmt='rounded_outline'))
    pause()


def pasien_detail():
    header('DETAIL PASIEN')
    no_rm = inp('No. RM pasien')
    p = cari_pasien_by_rm(no_rm)
    if not p:
        err('Pasien tidak ditemukan.')
        pause()
        return

    rows = [
        ['No. Rekam Medis', p['no_rm']], ['Nama', p['nama']], ['Tanggal Lahir', p['tanggal_lahir']],
        ['Umur', f"{p.get('umur', hitung_umur(p['tanggal_lahir']))} tahun"], ['Jenis Kelamin', p['jenis_kelamin']],
        ['Alamat', p['alamat']], ['No. Telepon', p['no_telepon']], ['Golongan Darah', p['golongan_darah'] or '-'],
        ['Penyakit', p['penyakit'] or '-'], ['Catatan Keluhan', p['keluhan'] or '-'],
        ['Tanggal Daftar', p.get('tanggal_daftar', '-')]]
    print()
    print(tabulate(rows, headers=['Field', 'Data'], tablefmt='rounded_outline'))
    pause()


def tampil_statistik():
    header('STATISTIK PASIEN')
    total = len(data_pasien)
    laki = sum(1 for p in data_pasien if p['jenis_kelamin'] == 'Laki-laki')
    perempuan = total - laki

    print()
    print(tabulate([['Total Pasien', total], ['Laki-laki', laki], ['Perempuan', perempuan]],
                   headers=['Keterangan', 'Jumlah'], tablefmt='rounded_outline'))

    # Rekap penyakit dengan loop manual
    rekap = {}
    for p in data_pasien:
        key = p['penyakit'] or 'Tidak Diketahui'
        rekap[key] = rekap.get(key, 0) + 1
    print('\n  Rekap Penyakit:')
    print(tabulate([[nama, jml, '█' * min(jml, 20)] for nama, jml in sorted(rekap.items(), key=lambda x: -x[1])],
                   headers=['Penyakit', 'Jumlah', 'Grafik'], tablefmt='rounded_outline'))

    # Rekap golongan darah dengan loop manual
    gol = {}
    for p in data_pasien:
        key = p['golongan_darah'] or '?'
        gol[key] = gol.get(key, 0) + 1
    print('\n  Rekap Golongan Darah:')
    print(tabulate(sorted(gol.items()), headers=['Gol. Darah', 'Jumlah'], tablefmt='rounded_outline'))
    pause()


def menu_pasien():
    options = {
        '1': ('Lihat Semua Pasien', pasien_lihat_semua),
        '2': ('Tambah Pasien', pasien_tambah),
        '3': ('Edit Pasien', pasien_edit),
        '4': ('Hapus Pasien', pasien_hapus),
        '5': ('Cari Pasien', pasien_cari),
        '6': ('Detail Pasien', pasien_detail),
    }
    while True:
        cls()
        header('MENU PASIEN')
        for k, (label, _) in options.items():
            print(f'    {k}. {label}')
        print('    0. Kembali ke Menu Utama')
        hr()
        pilih = input('  Pilih (0-6): ').strip()
        if pilih == '0':
            break
        elif pilih in options:
            cls()
            options[pilih][1]()
        else:
            err('Pilihan tidak valid.')
            pause()


def main_menu():
    options = {'1': ('Manajemen Pasien', menu_pasien), '2': ('Statistik', tampil_statistik)}
    while True:
        cls()
        print('\n' + '=' * 60)
        print('SISTEM MANAJEMEN PASIEN RUMAH SAKIT'.center(60))
        print('=' * 60)
        for k, (label, _) in options.items():
            print(f'    {k}. {label}')
        print('    0. Keluar')
        hr()
        pilih = input('  Pilih menu (0-2): ').strip()
        if pilih == '0':
            cls()
            print('\n  Terima kasih! Sampai jumpa.\n')
            sys.exit(0)
        elif pilih in options:
            cls()
            options[pilih][1]()
        else:
            err('Pilihan tidak valid.')
            pause()


if __name__ == '__main__':
    login()
    main_menu()
