# Dars Jadvallari / Class Schedules

Bu papkada har bir guruh uchun dars jadvali rasmlari saqlanadi.

## Fayl nomlash qoidalari

Har bir guruh uchun jadval rasmi quyidagi formatda nomlanishi kerak:

```
{GURUH_NOMI}.jpg
```

Misol:
- `EK-1-25.jpg` - Iqtisodiyot, 1-kurs, 2025-yil guruhi
- `HQ-1-24.jpg` - Yurisprudensiya, 1-kurs, 2024-yil guruhi
- `CS-1-25.jpg` - Kiberxavfsizlik, 1-kurs, 2025-yil guruhi

## Rasm formatları

- JPG (.jpg)
- PNG (.png)

## Jadval qo'shish

1. Guruh uchun jadval rasmini tayyorlang
2. Rasmni to'g'ri nom bilan bu papkaga joylashtiring
3. Bot avtomatik ravishda fayldan rasmni yuklaydi yoki database'dan file_id ni oladi

## Admin orqali yuklash

Admin panel orqali ham jadval qo'shish mumkin:
1. Bot admin panel'iga kiring
2. "Jadval yuklash" tugmasini bosing
3. Fakultet, kurs, yo'nalish va guruhni tanlang
4. Jadval rasmini yuboring
5. Bot avtomatik ravishda database'ga saqlaydi

## Database tuzilishi

Jadvallar `schedules` jadvalida saqlanadi:
- `faculty` - Fakultet nomi
- `direction` - Yo'nalish nomi (Yurisprudensiya uchun bo'sh yoki fakultet nomi)
- `course` - Kurs (1-kurs, 2-kurs, 3-kurs)
- `group_name` - Guruh nomi (EK-1-25, HQ-1-24, va h.k.)
- `image_id` - Telegram file_id (rasm Telegram'da saqlanadi)

## Guruhlar ro'yxati

### Biznes va innovatsion ta'lim

#### 1-kurs (2025)
- Psixologiya: PS-1-25
- Moliya: ML-1-25
- Dasturiy injiniring: DI-1-25
- Iqtisodiyot: EK-1-25, EK-2-25, EK-3-25, EK-4-25, EK-1-25r, EK-2-25r, EK-3-25r
- XIM: XIM-1-25, XIM-2-25, XIM-3-25, XIM-4-25, XIM-1-25r, XIM-2-25r, XIM-3-25r
- Bank ishi: BK-1-25
- Menejment: MN-1-25, MN-2-25
- Buxgalteriya: BH-1-25
- Boshlang'ich ta'lim: BT-1-25
- Xorijiy til: XT-1-25, XT-2-25, XT-1-25r
- Koreys tili: KR-1-25
- Kiberxavfsizlik: CS-1-25, CS-2-25, CS-3-25, CS-1-25r, CS-2-25r

#### 2-kurs (2024)
- Xorijiy til: XT-1-24, XT-2-24, XT-3-24, XT-1-24r
- AT: AT-1-24
- Iqtisodiyot: EK-1-24, EK-2-24, MEK-1-24, EK-1-24r, EK-2-24r
- Bank ishi: BK-1-24
- Kiberxavfsizlik: CS-1-24, CS-1-24r
- Dasturiy injiniring: DI-1-24
- Koreys tili: KR-1-24
- Boshlang'ich ta'lim: BT-1-24
- Psixologiya: PS-1-24
- XIM: XIM-1-24, XIM-2-24, XIM-1-24r, XIM-2-24r
- Menejment: MN-1-24

#### 3-kurs (2023)
- Xorijiy til: XT-1-23
- Iqtisodiyot: EK-1-23
- Kiberxavfsizlik: CS-1-23

### Yurisprudensiya

#### 1-kurs (2025)
HQ-1-25 dan HQ-30-25 gacha (30 ta guruh)
HQ-1-25r dan HQ-9-25r gacha (9 ta guruh)

#### 2-kurs (2024)
HQ-1-24 dan HQ-22-24 gacha (22 ta guruh)
HQ-1-24r dan HQ-6-24r gacha (6 ta guruh)

#### 3-kurs (2023)
HQ-1-23 dan HQ-6-23 gacha (6 ta guruh)

## Eslatma

Jadval rasmlarini bot ishga tushirilgandan keyin admin panel orqali yuklash tavsiya etiladi, chunki rasmlar Telegram file_id formatida database'da saqlanadi va keyingi yuborishlarda qayta yuklashni talab qilmaydi.
