# Golden Space

**Skill untuk AI agent yang mengatur proporsi, whitespace, hierarki visual,
dan pembuatan SVG yang rapi serta tetap mudah diedit.**

[English](README.md) · [Instruksi skill](skills/golden-space/SKILL.md) · [Lisensi MIT](LICENSE)

![Contoh komposisi Golden Space](skills/golden-space/assets/starter.svg)

Skill ini membantu agent mengambil keputusan desain untuk poster, diagram,
ilustrasi, ikon, dan studi layout. Cakupannya meliputi golden ratio, jarak,
tipografi, warna, alignment, ritme, dan keseimbangan optis.

Golden ratio dipakai sebagai pilihan proporsi sesuai kebutuhan konten. Agent
diminta membandingkannya dengan komposisi lain. Tidak ada persentase whitespace
yang wajib, spiral dekoratif wajib, atau gaya visual yang harus selalu ditiru.

## Pasang

Dengan [Skills CLI](https://github.com/vercel-labs/skills) dan versi Node.js yang didukung:

```sh
npx skills add guardyanz/golden-space --skill golden-space
```

Pilih agent tujuan di installer. Untuk pemasangan manual, clone repo lalu salin
**seluruh folder** `skills/golden-space` ke direktori skill milik agent. Folder
referensi, aset, dan skrip harus tetap bersama `SKILL.md`. Untuk mencoba tanpa
memasang, minta agent membaca file tersebut dan mengikutinya untuk tugas saat ini.

Formatnya mengikuti [Agent Skills](https://agentskills.io/specification). Cara
memanggil dan lokasi pemasangan mengikuti masing-masing agent. Pemeriksa SVG
membutuhkan Python 3.10+ tanpa paket tambahan; instruksi skill tetap bisa dipakai
tanpa Python.

## Contoh pemakaian

Di Codex:

```text
Gunakan $golden-space untuk membuat poster pameran keramik berukuran 1200 x 742.
Bandingkan golden ratio dengan rule of thirds, pilih yang cocok untuk konten.
Buat SVG lengkap dengan teks editable, objek terpisah, dan grup yang jelas.
Gunakan warna netral hangat dan whitespace yang lega.
```

```text
Gunakan $golden-space untuk merapikan SVG ini. Pertahankan teks dan identitas
visualnya, benahi grouping dan ID objek, lalu periksa dependensi eksternal.
Jelaskan jika ada perubahan yang memengaruhi tampilan.
```

Pada agent lain, pilih skill melalui cara pemanggilan yang didukung atau rujuk
langsung `SKILL.md`.

## Makna SVG editable

- Objek tetap berupa geometri vektor dengan bagian yang bisa dipilih terpisah.
- Teks pada master tetap berupa `<text>` / `<tspan>`, bukan outline.
- Grup dan ID objek jelas, dengan struktur yang dangkal.
- Tidak memakai bitmap tersembunyi, script, aset eksternal, atau efek filter pada master portabel.
- Salinan outline untuk distribusi, bila diperlukan, dibuat sebagai file terpisah.

Tampilan font bisa berbeda antar komputer. SVG yang lolos pemeriksaan struktur
masih perlu dirender dan diuji di editor tujuan sebelum diklaim kompatibel.
Pemeriksa ini tidak menilai keindahan, geometri, atau seluruh aspek aksesibilitas,
dan bukan sanitizer keamanan.

## Isi repo dan pemeriksaan

Tersedia [aturan komposisi](skills/golden-space/references/composition.md),
[kontrak SVG](skills/golden-space/references/svg-contract.md), tiga contoh SVG
original, [skenario evaluasi](evals/scenarios.md), serta pemeriksa struktur:

```sh
python skills/golden-space/scripts/check_svg.py desain.svg
python skills/golden-space/scripts/check_svg.py --strict --json desain.svg
python -m unittest discover -s tests -v
```

Mode biasa gagal jika ada error. `--strict` juga gagal pada warning yang perlu
ditinjau. Dokumentasi teknis dan batasan lengkap tersedia pada [README Inggris](README.md).
Seluruh instruksi, skrip, dan contoh SVG dalam repo ini menggunakan lisensi MIT.
